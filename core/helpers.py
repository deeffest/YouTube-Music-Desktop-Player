import os
import platform
import subprocess
from urllib.parse import urlparse

from PySide6.QtCore import QRect, Qt
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QColor, QIcon, QPixmap, QPainter


def str_to_bool(value):
    return str(value).lower() == "true"


def copy_text(text):
    QApplication.clipboard().setText(text)


def is_valid_ytmusic_url(url):
    parsed = urlparse(str(url))
    return parsed.scheme == "https" and parsed.netloc == "music.youtube.com"


def get_geometry(width, height):
    rect = QApplication.primaryScreen().availableGeometry()
    x = rect.center().x() - width // 2
    y = rect.center().y() - height // 2
    return QRect(x, y, width, height)


def open_url(url):
    if not url:
        return

    if platform.system() == "Windows":
        os.startfile(url)
    else:
        env = os.environ.copy()
        for var in ("LD_LIBRARY_PATH", "LD_PRELOAD"):
            env.pop(var, None)

        subprocess.Popen(["xdg-open", url], env=env)


def recolor_icon(icon, color):
    pixmap = QPixmap(icon)

    if color == 1:
        result = QPixmap(pixmap.size())
        result.fill(Qt.GlobalColor.transparent)
        painter = QPainter(result)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(result.rect(), QColor(0, 0, 0))
        painter.end()
        pixmap = result

    return QIcon(pixmap)
