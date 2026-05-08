import os
import sys
import socket
import logging
import platform
from logging.handlers import RotatingFileHandler

from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QPalette, QColor

from core.main_window import MainWindow
from core.application import SingletonApplication

NAME = "Youtube-Music-Desktop-Player"
DISPLAY_NAME = "YouTube Music Desktop Player"
VERSION = "1.27.0-rc1"
AUTHOR = "deeffest"
WEBSITE = "deeffest.pythonanywhere.com"
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
HOME_DIR = os.path.join(os.path.expanduser("~"), NAME)

UNIQUE_KEY = f"{AUTHOR}.{NAME}"
ACCENT_COLOR = QColor(255, 41, 41)
DEBUG = not getattr(sys, "frozen", False)


def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", 0))
        return s.getsockname()[1]


def init_app_settings():
    app_settings = QSettings(AUTHOR, NAME)
    if app_settings.value("light_theme") is None:
        app_settings.setValue("light_theme", 0)
    if app_settings.value("disable_frame_rate_limit") is None:
        app_settings.setValue("disable_frame_rate_limit", 0)
    return app_settings


def hide_home_folder():
    try:
        os.makedirs(HOME_DIR, exist_ok=True)
        if platform.system() == "Windows":
            import ctypes

            ctypes.windll.kernel32.SetFileAttributesW(HOME_DIR, 0x02)
        else:
            parent_dir = os.path.dirname(HOME_DIR)
            hidden_file = os.path.join(parent_dir, ".hidden")
            name = os.path.basename(HOME_DIR)

            existing = []
            if os.path.exists(hidden_file):
                with open(hidden_file, "r") as f:
                    existing = f.read().splitlines()

            if name not in existing:
                with open(hidden_file, "a") as f:
                    f.write(name + "\n")
    except Exception as e:
        print(f"Failed to hide home folder: {str(e)}")


def init_logging():
    logging.getLogger().handlers.clear()

    log_dir = os.path.join(HOME_DIR, "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = os.path.join(log_dir, "app.log")

    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    rotating_handler.setLevel(logging.INFO)
    rotating_handler.setFormatter(
        logging.Formatter(
            "[%(asctime)s] %(name)s - %(levelname)s - %(filename)s:"
            "%(lineno)d - %(message)s"
        )
    )

    logging.basicConfig(
        level=logging.INFO, handlers=[rotating_handler, logging.StreamHandler()]
    )


def ensure_desktop_icon():
    if platform.system() == "Linux":
        try:
            icon_path = os.path.join(CURRENT_DIR, "resources", "icons", "logo.png")
            content = (
                f"[Desktop Entry]\nType=Application\nName={NAME}"
                f"\nIcon={icon_path}\nNoDisplay=true\nStartupWMClass={NAME}\n"
            )
            desktop_path = os.path.expanduser(
                f"~/.local/share/applications/{NAME}.desktop"
            )

            if os.path.exists(desktop_path):
                with open(desktop_path, "r") as f:
                    if f.read() == content:
                        return

            os.makedirs(os.path.dirname(desktop_path), exist_ok=True)
            with open(desktop_path, "w") as f:
                f.write(content)

            os.system("update-desktop-database ~/.local/share/applications 2>/dev/null")
        except Exception as e:
            print(f"Failed to ensure desktop icon: {e}")


def set_app_palette(app, theme_setting):
    palette = QPalette()

    if theme_setting == 0:
        palette.setColor(QPalette.ColorRole.Window, QColor(39, 39, 39))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(32, 32, 32))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(43, 43, 43))
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(110, 110, 110))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 41, 41))
        palette.setColor(QPalette.ColorRole.Button, QColor(50, 50, 50))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Light, QColor(55, 55, 55))
        palette.setColor(QPalette.ColorRole.Midlight, QColor(52, 52, 52))
        palette.setColor(QPalette.ColorRole.Mid, QColor(45, 45, 45))
        palette.setColor(QPalette.ColorRole.Dark, QColor(30, 30, 30))
        palette.setColor(QPalette.ColorRole.Shadow, QColor(10, 10, 10))
        palette.setColor(QPalette.ColorRole.Highlight, ACCENT_COLOR)
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Accent, ACCENT_COLOR)
        palette.setColor(QPalette.ColorRole.Link, ACCENT_COLOR)
        palette.setColor(QPalette.ColorRole.LinkVisited, ACCENT_COLOR)
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(31, 31, 31))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(202, 202, 202))

        palette.setColor(
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.WindowText,
            QColor(109, 109, 109),
        )
        palette.setColor(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(109, 109, 109)
        )
        palette.setColor(
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.PlaceholderText,
            QColor(70, 70, 70),
        )
        palette.setColor(
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.ButtonText,
            QColor(109, 109, 109),
        )
        palette.setColor(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, QColor(28, 28, 28)
        )
        palette.setColor(
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.Highlight,
            QColor(60, 60, 60),
        )

        style_sheet = """
            QToolTip {
                color: rgb(202, 202, 202);
                background-color: rgb(31, 31, 31);
                border: 1px solid rgb(202, 202, 202);
                padding: 2px;
            }

            QFrame#ToolBar {
                border: none;
                border-bottom: 1px solid rgb(12, 12, 13);
            }
        """
    else:
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(30, 30, 30))
        palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(233, 233, 233))
        palette.setColor(QPalette.ColorRole.Text, QColor(30, 30, 30))
        palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(160, 160, 160))
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Button, QColor(225, 225, 225))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(30, 30, 30))
        palette.setColor(QPalette.ColorRole.Light, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Midlight, QColor(227, 227, 227))
        palette.setColor(QPalette.ColorRole.Mid, QColor(200, 200, 200))
        palette.setColor(QPalette.ColorRole.Dark, QColor(160, 160, 160))
        palette.setColor(QPalette.ColorRole.Shadow, QColor(100, 100, 100))
        palette.setColor(QPalette.ColorRole.Highlight, ACCENT_COLOR)
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Accent, ACCENT_COLOR)
        palette.setColor(QPalette.ColorRole.Link, ACCENT_COLOR)
        palette.setColor(QPalette.ColorRole.LinkVisited, ACCENT_COLOR)
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(245, 245, 245))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(53, 53, 53))

        palette.setColor(
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.WindowText,
            QColor(160, 160, 160),
        )
        palette.setColor(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(160, 160, 160)
        )
        palette.setColor(
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.PlaceholderText,
            QColor(200, 200, 200),
        )
        palette.setColor(
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.ButtonText,
            QColor(160, 160, 160),
        )
        palette.setColor(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, QColor(235, 235, 235)
        )
        palette.setColor(
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.Highlight,
            QColor(200, 200, 200),
        )

        style_sheet = """
            QToolTip {
                color: rgb(53, 53, 53);
                background-color: rgb(245, 245, 245);
                border: 1px solid rgb(180, 180, 180);
                padding: 2px;
            }

            QFrame#ToolBar {
                border: none;
                border-bottom: 1px solid rgb(204, 204, 204);
            }
        """

    app.setPalette(palette)
    app.setStyleSheet(style_sheet)


def main():
    hide_home_folder()
    init_logging()
    ensure_desktop_icon()

    app_settings = init_app_settings()
    light_theme_setting = int(app_settings.value("light_theme"))
    disable_frame_rate_limit_setting = int(
        app_settings.value("disable_frame_rate_limit")
    )

    os.environ.pop("QTWEBENGINE_CHROMIUM_FLAGS", None)
    os.environ.pop("QTWEBENGINE_REMOTE_DEBUGGING", None)

    if disable_frame_rate_limit_setting == 1:
        os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-frame-rate-limit"
    if DEBUG:
        os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = str(find_free_port())

    app = SingletonApplication(sys.argv, UNIQUE_KEY)
    app.setApplicationName(NAME)
    app.setApplicationVersion(VERSION)
    app.setOrganizationName(AUTHOR)
    app.setOrganizationDomain(WEBSITE)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)
    app.setDesktopFileName(NAME)

    app.setStyle("Fusion")
    if light_theme_setting == 0:
        app.styleHints().setColorScheme(Qt.ColorScheme.Dark)
    else:
        app.styleHints().setColorScheme(Qt.ColorScheme.Light)
    set_app_palette(app, light_theme_setting)

    window = MainWindow(
        app_settings,
        light_theme_setting,
        disable_frame_rate_limit_setting,
        app_info=[NAME, DISPLAY_NAME, VERSION, AUTHOR, WEBSITE, CURRENT_DIR, HOME_DIR],
    )
    app.aboutToQuit.connect(window.app_quit)
    window.show_window()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
