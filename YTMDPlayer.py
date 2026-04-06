import os
import sys
import shutil
import logging
import platform
import subprocess

from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication

from core.application import SingletonApplication
from core.main_window import MainWindow

NAME = "Youtube-Music-Desktop-Player"
DISPLAY_NAME = "YouTube Music Desktop Player"
VERSION = "1.26.0"
AUTHOR = "deeffest"
WEBSITE = "deeffest.pythonanywhere.com"
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
HOME_DIR = os.path.join(os.path.expanduser("~"), NAME)

UNIQUE_KEY = f"{AUTHOR}.{NAME}"
ACCENT = QColor(255, 41, 41)
ACCENT_DISABLED_DARK = QColor(60, 60, 60)
ACCENT_DISABLED_LIGHT = QColor(200, 200, 200)


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

    from logging.handlers import RotatingFileHandler

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


def init_app_settings():
    app_settings = QSettings(AUTHOR, NAME)
    if app_settings.value("opengl_enviroment") is None:
        app_settings.setValue("opengl_enviroment", "Auto")
    if app_settings.value("light_theme") is None:
        app_settings.setValue("light_theme", 0)
    return app_settings


def setup_opengl_environment(app_settings):
    setting = app_settings.value("opengl_enviroment")
    if setting == "Desktop":
        os.environ["QT_OPENGL"] = "desktop"
    elif setting == "Angle":
        os.environ["QT_OPENGL"] = "angle"
    elif setting == "Software":
        os.environ["QT_OPENGL"] = "software"
    else:
        os.environ.pop("QT_OPENGL", None)
    return setting


def set_app_palette(app, theme_setting):
    app.setStyle("Fusion")
    palette = QPalette()

    if theme_setting == 0:
        palette.setColor(QPalette.Window, QColor(39, 39, 39))
        palette.setColor(QPalette.Base, QColor(32, 32, 32))
        palette.setColor(QPalette.AlternateBase, QColor(43, 43, 43))
        palette.setColor(QPalette.ToolTipBase, QColor(31, 31, 31))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.ToolTipText, QColor(202, 202, 202))
        palette.setColor(QPalette.BrightText, QColor(255, 41, 41))
        palette.setColor(QPalette.Button, QColor(50, 50, 50))
        palette.setColor(QPalette.Light, QColor(55, 55, 55))
        palette.setColor(QPalette.Mid, QColor(45, 45, 45))
        palette.setColor(QPalette.Dark, QColor(30, 30, 30))
        palette.setColor(QPalette.Link, ACCENT)
        palette.setColor(QPalette.Highlight, ACCENT)
        palette.setColor(QPalette.HighlightedText, Qt.white)
        palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(109, 109, 109))
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(109, 109, 109))
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(109, 109, 109))
        palette.setColor(QPalette.Disabled, QPalette.Base, QColor(28, 28, 28))
        palette.setColor(QPalette.Disabled, QPalette.Highlight, ACCENT_DISABLED_LIGHT)
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
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(233, 233, 233))
        palette.setColor(QPalette.ToolTipBase, QColor(245, 245, 245))
        palette.setColor(QPalette.WindowText, QColor(30, 30, 30))
        palette.setColor(QPalette.Text, QColor(30, 30, 30))
        palette.setColor(QPalette.ButtonText, QColor(30, 30, 30))
        palette.setColor(QPalette.ToolTipText, QColor(53, 53, 53))
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Button, QColor(225, 225, 225))
        palette.setColor(QPalette.Light, QColor(255, 255, 255))
        palette.setColor(QPalette.Mid, QColor(200, 200, 200))
        palette.setColor(QPalette.Dark, QColor(160, 160, 160))
        palette.setColor(QPalette.Link, ACCENT)
        palette.setColor(QPalette.Highlight, ACCENT)
        palette.setColor(QPalette.HighlightedText, Qt.white)
        palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(160, 160, 160))
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(160, 160, 160))
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(160, 160, 160))
        palette.setColor(QPalette.Disabled, QPalette.Base, QColor(235, 235, 235))
        palette.setColor(QPalette.Disabled, QPalette.Highlight, ACCENT_DISABLED_LIGHT)
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

    app_settings = init_app_settings()
    opengl_setting = setup_opengl_environment(app_settings)
    theme_setting = int(app_settings.value("light_theme"))

    app = SingletonApplication(sys.argv, UNIQUE_KEY)
    app.setApplicationName(NAME)
    app.setApplicationVersion(VERSION)
    app.setOrganizationName(AUTHOR)
    app.setOrganizationDomain(WEBSITE)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    set_app_palette(app, theme_setting)

    # https://stackoverflow.com/q/76724700/20546833
    if platform.system() == "Windows":
        sw_dir = os.path.expanduser(
            f"~/AppData/Local/{AUTHOR}/{NAME}/QtWebEngine/Default/Service Worker"
        )
    else:
        sw_dir = os.path.expanduser(
            f"~/.local/share/{AUTHOR}/{NAME}/QtWebEngine/Default/Service Worker"
        )
    try:
        shutil.rmtree(sw_dir)
    except Exception as e:
        logging.error(f"Failed to remove Service Worker: {str(e)}")

    window = MainWindow(
        app_settings,
        opengl_setting,
        theme_setting,
        app_info=[NAME, DISPLAY_NAME, VERSION, AUTHOR, WEBSITE, CURRENT_DIR, HOME_DIR],
    )
    app.aboutToQuit.connect(window.app_quit)
    window.show()

    sys.exit(app.exec_())


def check_glx():
    if "--child" in sys.argv:
        app = QApplication([])  # noqa: F841
        sys.exit(0)

    env = os.environ.copy()
    env["LD_PRELOAD"] = os.path.join(CURRENT_DIR, "core", "glx", "abort_override.so")

    result = subprocess.run(
        [sys.executable, sys.argv[0], "--child"], stdout=subprocess.DEVNULL, env=env
    )
    return result.returncode == 0


if __name__ == "__main__":
    if not platform.system() == "Windows" and not check_glx():
        os.environ["QT_XCB_GL_INTEGRATION"] = "none"

    main()
