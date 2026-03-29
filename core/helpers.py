import os
import platform
import subprocess
from urllib.parse import urlparse

from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QColor, QIcon, QPixmap, QPainter
from PyQt5.QtWidgets import QDesktopWidget, QApplication

if platform.system() == "Windows":
    import win32api  # type: ignore
    import win32gui  # type: ignore


def str_to_bool(value):
    return str(value).lower() == "true"


def copy_text(text):
    QApplication.clipboard().setText(text)


def is_valid_ytmusic_url(url):
    parsed = urlparse(str(url))
    return parsed.scheme == "https" and parsed.netloc == "music.youtube.com"


def get_centered_geometry(width, height):
    screen_geometry = QDesktopWidget().screenGeometry()
    x = (screen_geometry.width() - width) // 2
    y = (screen_geometry.height() - height) // 2
    return QRect(x, y, width, height)


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
        result.fill(Qt.transparent)
        painter = QPainter(result)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
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


def get_taskbar_position():
    position = "Unknown"

    if platform.system() == "Windows":
        screen_width = win32api.GetSystemMetrics(0)
        screen_height = win32api.GetSystemMetrics(1)

        taskbar = win32gui.FindWindow("Shell_TrayWnd", None)
        rect = win32gui.GetWindowRect(taskbar)

        taskbar_left, taskbar_top, taskbar_right, taskbar_bottom = rect

        if taskbar_top == 0 and taskbar_left == 0 and taskbar_right == screen_width:
            position = "Top"
        elif (
            taskbar_bottom == screen_height
            and taskbar_left == 0
            and taskbar_right == screen_width
        ):
            position = "Bottom"
        elif taskbar_left == 0 and taskbar_top == 0 and taskbar_bottom == screen_height:
            position = "Left"
        elif (
            taskbar_right == screen_width
            and taskbar_top == 0
            and taskbar_bottom == screen_height
        ):
            position = "Right"

    return position
