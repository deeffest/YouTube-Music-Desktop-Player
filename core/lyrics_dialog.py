import os
import re
import bisect
import logging
from typing import TYPE_CHECKING

import requests
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QThread, QSize, pyqtSignal
from PyQt5.QtWidgets import QDialog, QLabel, QFileDialog
from qfluentwidgets5 import SplashScreen, Action, RoundMenu
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from core.helpers import recolor_icon, open_url
from core.ui.ui_lyrics_dialog import Ui_LyricsDialog

if TYPE_CHECKING:
    from core.main_window import MainWindow


class LoadLyricsThread(QThread):
    load_lyrics_success = pyqtSignal(list)
    load_lyrics_failed = pyqtSignal()
    load_lyrics_error = pyqtSignal(str)

    def __init__(self, title, artist, duration, cache_dir, video_id, parent=None):
        super().__init__(parent)
        self.title = title
        self.artist = artist
        self.duration = duration
        self.cache_dir = cache_dir
        self.video_id = video_id

    def run(self):
        cache_path = os.path.join(self.cache_dir, "lyrics", f"{self.video_id}.lrc")
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)

        files = sorted(
            [
                os.path.join(self.cache_dir, "lyrics", f)
                for f in os.listdir(os.path.join(self.cache_dir, "lyrics"))
                if f.endswith(".lrc")
            ],
            key=os.path.getmtime,
        )
        while len(files) >= 100:
            os.remove(files.pop(0))

        def parse(lrc):
            pattern = re.compile(r"\[(\d+):(\d+(?:\.\d+)?)\](.*)")
            lines = []
            for raw in lrc.splitlines():
                m = pattern.match(raw.strip())
                if m:
                    t = int(m.group(1)) * 60 + float(m.group(2))
                    lines.append((t, m.group(3).strip()))
            return lines

        if os.path.exists(cache_path):
            with open(cache_path, encoding="utf-8") as f:
                lrc = f.read()
            lines = parse(lrc)
            if lines:
                self.load_lyrics_success.emit(lines)
                return

        session = requests.Session()
        retry = Retry(total=2, backoff_factor=0.3)
        session.mount("https://", HTTPAdapter(max_retries=retry))

        try:
            resp = session.get(
                "https://lrclib.net/api/get",
                params={
                    "track_name": self.title,
                    "artist_name": self.artist,
                    "duration": self.duration,
                },
                timeout=15,
            )
            data = resp.json() if resp.status_code == 200 else {}
            lrc = data.get("syncedLyrics", "")
            lines = parse(lrc) if lrc else []

            if lines:
                with open(cache_path, "w", encoding="utf-8") as f:
                    f.write(lrc)
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
        self.timestamps = []
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
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)

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
        self.main_menu.setActionVisible(self.reload_lyrics_action, False)
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
            self.window.title,
            self.window.artist,
            self.window.duration,
            self.window.cache_dir,
            self.window.video_id,
            self,
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
        self.timestamps = [t for t, _ in lines]
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
        self.main_menu.setActionVisible(self.reload_lyrics_action, True)

        self.verticalLayout_4.addWidget(self.create_label(msg, "red"))

    def on_load_lyrics_finished(self):
        if not self.is_lyrics_loading:
            self.splash_screen.hide()

    def create_actions(self):
        self.reload_lyrics_action = Action("Reload lyrics")
        self.reload_lyrics_action.setIcon(
            recolor_icon(
                f"{self.window.icon_folder}/reload.png",
                self.window.light_theme_setting,
            )
        )
        self.reload_lyrics_action.triggered.connect(self.load_lyrics)

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
        self.main_menu.addAction(self.reload_lyrics_action)
        self.main_menu.setActionVisible(self.reload_lyrics_action, False)
        self.main_menu.addSeparator()
        self.main_menu.addAction(self.save_lyrics_as_action)
        self.main_menu.addAction(self.powered_by_lrclib_action)

    def sync_lyrics_to_time(self, current_time):
        if not self.lines:
            return

        seconds = float(current_time)
        idx = bisect.bisect_right(self.timestamps, seconds) - 1

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
