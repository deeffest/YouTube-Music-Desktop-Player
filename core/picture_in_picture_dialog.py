import logging
import platform
from typing import TYPE_CHECKING

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QDesktopWidget
from qfluentwidgets import ToolTipFilter, ToolTipPosition

from core.artwork_loader import ArtworkLoader
from core.helpers import get_taskbar_position, recolor_icon
from core.ui.ui_picture_in_picture_dialog import Ui_PictureInPictureDialog

if TYPE_CHECKING:
    from core.main_window import MainWindow


class PictureInPictureDialog(QDialog, Ui_PictureInPictureDialog):
    def __init__(self, last_win_geo, parent=None):
        super().__init__(parent)
        self.window: "MainWindow" = parent
        self.last_win_geo = last_win_geo
        self.artwork_loader_thread = None

        self.configure_window()
        self.configure_ui_elements()

    def configure_window(self):
        if platform.system() == "Windows":
            from pywinstyles import apply_style  # type: ignore

            theme = self.window.theme_setting
            color = "dark" if theme == 0 else "light"

            try:
                apply_style(self, color)
            except Exception as e:
                logging.error(f"Failed to apply dark style: + {str(e)}")

        self.setupUi(self)
        flags = Qt.Window | Qt.WindowCloseButtonHint
        if self.window.pip_is_always_on_top_setting == 1:
            flags |= Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.setWindowIcon(
            QIcon(f"{self.window.icon_folder}/picture_in_picture-titlebar.png")
        )
        if self.window.save_last_pos_of_mp_setting == 1:
            self.setGeometry(self.window.geometry_of_mp_setting)
        else:
            screen_geometry = QDesktopWidget().screenGeometry()
            taskbar_position = get_taskbar_position()
            x = screen_geometry.width() - self.width() - 30
            y = screen_geometry.height() - self.height() - 30
            if taskbar_position == "Right":
                x = screen_geometry.width() - self.width() - 93
            elif taskbar_position == "Bottom":
                y = screen_geometry.height() - self.height() - 71
            self.setGeometry(x, y, self.width(), self.height())
        self.setFixedSize(self.size())
        self.setWindowOpacity(self.window.pip_opacity_setting)

    def configure_ui_elements(self):
        self.dislike_button.clicked.connect(self.window.dislike)
        self.previous_button.clicked.connect(self.window.previous)
        self.play_pause_button.clicked.connect(self.window.play_pause)
        self.next_button.clicked.connect(self.window.next)
        self.like_button.clicked.connect(self.window.like)

        self.dislike_button.installEventFilter(
            ToolTipFilter(self.dislike_button, 300, ToolTipPosition.TOP)
        )
        self.previous_button.installEventFilter(
            ToolTipFilter(self.previous_button, 300, ToolTipPosition.TOP)
        )
        self.play_pause_button.installEventFilter(
            ToolTipFilter(self.play_pause_button, 300, ToolTipPosition.TOP)
        )
        self.next_button.installEventFilter(
            ToolTipFilter(self.next_button, 300, ToolTipPosition.TOP)
        )
        self.like_button.installEventFilter(
            ToolTipFilter(self.like_button, 300, ToolTipPosition.TOP)
        )

        self.dislike_button.setIcon(
            recolor_icon(
                f"{self.window.icon_folder}/dislike.png", self.window.theme_setting
            )
        )
        self.previous_button.setIcon(
            recolor_icon(
                f"{self.window.icon_folder}/previous-filled.png",
                self.window.theme_setting,
            )
        )
        self.play_pause_button.setIcon(
            recolor_icon(
                f"{self.window.icon_folder}/play-filled.png", self.window.theme_setting
            )
        )
        self.next_button.setIcon(
            recolor_icon(
                f"{self.window.icon_folder}/next-filled.png", self.window.theme_setting
            )
        )
        self.like_button.setIcon(
            recolor_icon(
                f"{self.window.icon_folder}/like.png", self.window.theme_setting
            )
        )

        if self.window.theme_setting == 1:
            self.artist_label.setStyleSheet("color: gray")
            self.BodyLabel.setStyleSheet("color: gray")
            self.BodyLabel_2.setStyleSheet("color: gray")

    def load_artwork(self, url):
        self.stop_running_threads()

        self.artwork_loader_thread = ArtworkLoader(url, self.window)
        self.artwork_loader_thread.artwork_loaded.connect(self.on_artwork_loaded)
        self.artwork_loader_thread.start()

    def on_artwork_loaded(self, pixmap):
        self.artwork_loader_thread = None
        self.artwork_label.setPixmap(pixmap)

    def save_geometry_of_mp(self):
        if self.window.save_last_pos_of_mp_setting == 1:
            self.window.geometry_of_mp_setting = self.geometry()
            self.window.settings_.setValue(
                "geometry_of_mp", self.window.geometry_of_mp_setting
            )

    def stop_running_threads(self):
        if (
            self.artwork_loader_thread is not None
            and self.artwork_loader_thread.isRunning()
        ):
            self.artwork_loader_thread.stop()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event):
        self.save_geometry_of_mp()
        self.stop_running_threads()

        self.window.show()
        self.window.activateWindow()
        self.window.setGeometry(self.last_win_geo)

        if self.window.system_tray_icon:
            self.window.system_tray_icon.show()

        self.window.picture_in_picture_dialog = None
        event.accept()
