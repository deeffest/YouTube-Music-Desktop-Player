from typing import TYPE_CHECKING

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog

from core.ui.ui_lyrics_dialog import Ui_LyricsDialog

if TYPE_CHECKING:
    from main_window import MainWindow


class LyricsDialog(QDialog, Ui_LyricsDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window: "MainWindow" = parent

        self.configure_window()
        self.configure_ui_elements()

    def configure_window(self):
        self.setupUi(self)
        self.setWindowTitle(f"Lyrics │ {self.window.title}")
        self.setWindowIcon(QIcon(f"{self.window.icon_folder}/lyrics-colored.png"))

    def configure_ui_elements(self):
        pass
