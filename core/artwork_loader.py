import logging
from typing import TYPE_CHECKING

import requests
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QThread, Signal, Qt

if TYPE_CHECKING:
    from core.main_window import MainWindow


class ArtworkLoader(QThread):
    artwork_loaded = Signal(QPixmap)

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
                60,
                60,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            self.artwork_loaded.emit(resized_pixmap)
        except Exception as e:
            logging.error(f"Failed to load artwork: {str(e)}")
            self.artwork_loaded.emit(QPixmap())

    def stop(self):
        self.terminate()
        self.wait()
