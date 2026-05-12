import os
import re
import logging
from typing import TYPE_CHECKING

import requests
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QThread, QSize, Signal
from PySide6.QtWidgets import QDialog, QLabel, QFileDialog
from qfluentwidgets import SplashScreen, Action, RoundMenu

from core.helpers import recolor_icon, open_url
from core.ui.ui_lyrics_dialog import Ui_LyricsDialog

if TYPE_CHECKING:
    from core.main_window import MainWindow


class LoadLyricsThread(QThread):
    load_lyrics_success = Signal(list)
    load_lyrics_failed = Signal()
    load_lyrics_error = Signal(str)

    def __init__(self, title, artist, duration, parent=None):
        super().__init__(parent)
        self.title = title
        self.artist = artist
        self.duration = duration

    def run(self):
        try:
            resp = requests.get(
                "https://lrclib.net/api/get",
                params={
                    "track_name": self.title,
                    "artist_name": self.artist,
                    "duration": self.duration,
                },
                timeout=10,
            )
            data = resp.json() if resp.status_code == 200 else {}
            lrc = data.get("syncedLyrics", "")

            def parse(lrc):
                pattern = re.compile(r"\[(\d+):(\d+(?:\.\d+)?)\](.*)")
                lines = []
                for raw in lrc.splitlines():
                    m = pattern.match(raw.strip())
                    if m:
                        t = int(m.group(1)) * 60 + float(m.group(2))
                        lines.append((t, m.group(3).strip()))
                return lines

            lines = parse(lrc) if lrc else []
            if lines:
                self.load_lyrics_success.emit(lines)
            else:
                self.load_lyrics_failed.emit()
        except Exception as e:
            logging.error(f"Failed to load lyrics: {str(e)}")
            self.load_lyrics_error.emit(str(e))

    def stop(self):
        self.terminate()
        self.wait()


class LyricsDialog(QDialog, Ui_LyricsDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window: "MainWindow" = parent

        self.lines = []
        self.labels = []
        self.current_index = -1
        self.load_lyrics_thread = None
        self.is_lyrics_loading = False

        self.configure_window()
        self.configure_ui_elements()
        self.create_actions()
        self.create_context_menus()
        self.load_lyrics()

    def configure_window(self):
        self.setupUi(self)
        self.setWindowTitle(f"Lyrics │ {self.window.title}")
        self.setWindowIcon(QIcon(f"{self.window.icon_folder}/lyrics-colored.png"))

        self.splash_screen = SplashScreen(
            self.windowIcon(), self.scrollArea, enableTitleBar=False
        )
        self.splash_screen.setIconSize(QSize(102, 102))

    def configure_ui_elements(self):
        self.verticalLayout_4.setAlignment(Qt.AlignmentFlag.AlignTop)

    def load_lyrics(self):
        self.lines = []
        self.labels = []
        self.current_index = -1
        self.is_lyrics_loading = True
        self.save_lyrics_as_action.setEnabled(False)

        while self.verticalLayout_4.count():
            item = self.verticalLayout_4.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.splash_screen.show()

        title = self.window.title
        self.setWindowTitle(f"Lyrics │ {title}")

        if not title:
            return

        if self.load_lyrics_thread and self.load_lyrics_thread.isRunning():
            self.load_lyrics_thread.stop()

        self.load_lyrics_thread = LoadLyricsThread(
            self.window.title, self.window.artist, self.window.duration, self
        )
        self.load_lyrics_thread.load_lyrics_success.connect(self.on_load_lyrics_success)
        self.load_lyrics_thread.load_lyrics_failed.connect(self.on_load_lyrics_failed)
        self.load_lyrics_thread.load_lyrics_error.connect(self.on_load_lyrics_error)
        self.load_lyrics_thread.finished.connect(self.on_load_lyrics_finished)
        self.load_lyrics_thread.start()

    def on_load_lyrics_success(self, lines):
        self.is_lyrics_loading = False
        self.save_lyrics_as_action.setEnabled(True)

        self.lines = lines
        for _, text in lines:
            label = self.create_label(text)
            self.labels.append(label)
            self.verticalLayout_4.addWidget(label)

        self.scrollArea.verticalScrollBar().rangeChanged.connect(self.on_range_changed)

    def on_range_changed(self, min, max):
        if max > 0:
            self.scrollArea.verticalScrollBar().rangeChanged.disconnect(
                self.on_range_changed
            )
            self.sync_lyrics_to_time(self.window.current_time)

    def on_load_lyrics_failed(self):
        self.is_lyrics_loading = False

        self.verticalLayout_4.addWidget(self.create_label("Lyrics not found :("))

    def on_load_lyrics_error(self, msg):
        self.is_lyrics_loading = False

        self.verticalLayout_4.addWidget(self.create_label(msg, "red"))

    def on_load_lyrics_finished(self):
        if not self.is_lyrics_loading:
            self.splash_screen.hide()

    def create_actions(self):
        self.save_lyrics_as_action = Action("Save lyrics as...")
        self.save_lyrics_as_action.setIcon(
            recolor_icon(
                f"{self.window.icon_folder}/save_as.png",
                self.window.light_theme_setting,
            )
        )
        self.save_lyrics_as_action.setEnabled(False)
        self.save_lyrics_as_action.triggered.connect(self.save_lyrics_as)

        self.powered_by_lrclib_action = Action("Powered by lrclib.net")
        self.powered_by_lrclib_action.setIcon(
            QIcon(f"{self.window.icon_folder}/lrclib.png")
        )
        self.powered_by_lrclib_action.triggered.connect(
            lambda: open_url("https://lrclib.net")
        )

    def save_lyrics_as(self):
        if not self.lines:
            return

        save_lyrics_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save lyrics as...",
            f"{self.window.last_save_lyrics_path_setting}/"
            f"{self.window.title or 'Unknown'}.lrc",
            "LRC Files (*.lrc);;Text Files (*.txt);;All Files (*)",
        )
        if not save_lyrics_path:
            return

        self.window.last_save_lyrics_path_setting = os.path.dirname(save_lyrics_path)
        self.window.settings_.setValue(
            "last_save_lyrics_path", self.window.last_save_lyrics_path_setting
        )

        try:
            with open(save_lyrics_path, "w", encoding="utf-8") as f:
                for t, text in self.lines:
                    minutes = int(t // 60)
                    seconds = t % 60
                    f.write(f"[{minutes:02d}:{seconds:05.2f}]{text}\n")
        except Exception as e:
            logging.error(f"Failed to save lyrics: {str(e)}")

    def create_context_menus(self):
        self.main_menu = RoundMenu()
        self.main_menu.addAction(self.save_lyrics_as_action)
        self.main_menu.addAction(self.powered_by_lrclib_action)

    def sync_lyrics_to_time(self, current_time):
        if not self.lines:
            return

        def to_seconds(time_str):
            try:
                parts = time_str.strip().split(":")
                return (
                    int(parts[0]) * 60 + float(parts[1])
                    if len(parts) == 2
                    else float(parts[0])
                )
            except Exception:
                return 0.0

        seconds = to_seconds(current_time) + 1.0
        idx = -1
        for i, (t, _) in enumerate(self.lines):
            if t <= seconds:
                idx = i
            else:
                break

        if idx == self.current_index:
            return

        self.current_index = idx
        active_color = "black" if self.window.light_theme_setting == 1 else "white"

        for i, label in enumerate(self.labels):
            color = active_color if i == idx else "gray"
            label.setStyleSheet(f"font-family: Arial; font-size: 16pt; color: {color};")

        self.scroll_to_active_label()

    def create_label(self, text, color="gray"):
        label = QLabel(text or "♪", self.widget)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setWordWrap(True)
        label.setStyleSheet(f"font-family: Arial; font-size: 16pt; color: {color};")
        return label

    def scroll_to_active_label(self):
        if 0 <= self.current_index < len(self.labels):
            label = self.labels[self.current_index]
            pos = label.mapTo(self.scrollAreaWidgetContents, label.rect().center())
            viewport_half = self.scrollArea.viewport().height() // 2
            self.scrollArea.verticalScrollBar().setValue(pos.y() - viewport_half)

    def contextMenuEvent(self, event):
        self.main_menu.exec(event.globalPos())

    def closeEvent(self, event):
        if self.load_lyrics_thread and self.load_lyrics_thread.isRunning():
            self.load_lyrics_thread.stop()

        self.window.lyrics_dialog = None
        event.accept()
