import re
import logging
from typing import TYPE_CHECKING

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QUrl, Qt, QSize
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from qfluentwidgets import SplashScreen

from core.ui.ui_comments_dialog import Ui_CommentsDialog

if TYPE_CHECKING:
    from main_window import MainWindow


class WebEnginePage(QWebEnginePage):
    def __init__(self, profile, parent):
        super().__init__(profile, parent)

    def acceptNavigationRequest(self, url, type, isMainFrame):
        url_str = url.toString()
        if re.match(r"^https://m\.youtube\.com/watch\?v=", url_str):
            return True
        return False

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        if level == QWebEnginePage.JavaScriptConsoleMessageLevel.ErrorMessageLevel:
            logging.error(
                f"JavaScript Console Error: {message} "
                f"(Line: {lineNumber}, Source: {sourceID})"
            )
        else:
            print(
                f"JavaScript Console Message: {message} "
                f"(Line: {lineNumber}, Source: {sourceID})"
            )


class WebEngineView(QWebEngineView):
    def __init__(self, parent):
        super().__init__(parent)

    def contextMenuEvent(self, event):
        event.accept()


class CommentsDialog(QDialog, Ui_CommentsDialog):
    def __init__(self, video_id, parent=None):
        super().__init__(parent)
        self.window: "MainWindow" = parent
        self.video_id = video_id

        self.configure_window()
        self.setup_web_engine()
        self.configure_ui_elements()
        self.show_splash_screen()

    def configure_window(self):
        self.setupUi(self)
        self.setWindowTitle(f"Comments │ {self.window.title}")
        self.setWindowIcon(QIcon(f"{self.window.icon_folder}/comments-colored.png"))
        self.setMaximumWidth(548)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

    def setup_web_engine(self):
        self.webpage = WebEnginePage(self.window.webprofile, self)

        self.webview = WebEngineView(self)
        self.webview.setPage(self.webpage)
        self.webview.loadFinished.connect(self.on_load_finished)
        self.webview.load(QUrl(f"https://m.youtube.com/watch?v={self.video_id}"))

    def configure_ui_elements(self):
        self.verticalLayout.addWidget(self.webview)

    def show_splash_screen(self):
        self.splash_screen = SplashScreen(
            self.windowIcon(), self.webview, enableTitleBar=False
        )
        self.splash_screen.setIconSize(QSize(102, 102))

    def on_load_finished(self):
        if self.splash_screen is not None:
            self.close_splash_screen()

    def close_splash_screen(self):
        self.splash_screen.deleteLater()
        self.splash_screen = None

    def closeEvent(self, event):
        self.webpage.deleteLater()
        event.accept()
