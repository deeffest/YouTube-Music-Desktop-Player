import logging
from typing import TYPE_CHECKING

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal, Qt

if TYPE_CHECKING:
    from core.main_window import MainWindow


class ArtworkLoader(QThread):
    artwork_loaded = pyqtSignal(QPixmap)

    def __init__(self, url, parent=None):
        super().__init__(parent)
        self.window: "MainWindow" = parent
        self.url = url

    def run(self):
        try:
            response = requests.get(
                self.url,
                timeout=10,
            )
            response.raise_for_status()

            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            resized_pixmap = pixmap.scaled(
                60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )

            self.artwork_loaded.emit(resized_pixmap)
        except Exception as e:
            logging.error(f"Failed to load artwork: {str(e)}")
            self.artwork_loaded.emit(QPixmap())

    def stop(self):
        self.terminate()
        self.wait()
