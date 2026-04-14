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


def open_url(url):
    if platform.system() == "Windows":
        os.startfile(url)
        return

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


def clean_up_url(url):
    parsed = urlparse(str(url))
    if parsed.netloc != "music.youtube.com":
        return url

    params = dict(
        param.split("=", 1) for param in parsed.query.split("&") if "=" in param
    )

    if parsed.path == "/watch" and "v" in params:
        return f"https://music.youtube.com/watch?v={params['v']}"

    if parsed.path == "/playlist" and "list" in params:
        return f"https://music.youtube.com/playlist?list={params['list']}"

    return f"https://{parsed.netloc}{parsed.path}"


def get_geometry(width, height, position="center", margin=0):
    rect = QApplication.primaryScreen().availableGeometry()

    positions = {
        "center": (rect.center().x() - width // 2, rect.center().y() - height // 2),
        "bottom_right": (
            rect.right() - width - margin,
            rect.bottom() - height - margin,
        ),
        "bottom_left": (rect.left() + margin, rect.bottom() - height - margin),
        "top_right": (rect.right() - width - margin, rect.top() + margin),
        "top_left": (rect.left() + margin, rect.top() + margin),
    }

    x, y = positions[position]
    return QRect(x, y, width, height)
