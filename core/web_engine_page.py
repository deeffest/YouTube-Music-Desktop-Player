import re
import logging
from typing import TYPE_CHECKING

from PySide6.QtWebEngineCore import QWebEnginePage
from qfluentwidgets import MessageBox

from core.input_msg_box import InputMessageBox

if TYPE_CHECKING:
    from core.main_window import MainWindow


class WebEnginePage(QWebEnginePage):
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)
        self.window: "MainWindow" = parent

    def acceptNavigationRequest(self, url, type, isMainFrame):
        url_str = url.toString()

        patterns = [
            r"^https://music\.youtube\.com/.*$",
            r"^https://accounts\.google\..*/.*$",
            r"^https://accounts\.youtube\.com/.*$",
            r"^https://www\.youtube\.com/signin.*action_handle_signin.*$",
            r"^https://www\.google\.com/recaptcha.*$",
            r"^https://consent\.youtube\.com/.*$",
            r"^https://www\.google\.com/tools/feedback/.*$",
            r"^https://gds\.google\.com/web/landing.*$",
            r"^https://www\.google\.com/sorry/.*$",
        ]

        for pattern in patterns:
            if re.match(pattern, url_str):
                return True

        return False

    def javaScriptAlert(self, securityOrigin, msg):
        msg_box = MessageBox(
            f"JavaScript alert - {securityOrigin.toString()}", msg, self.window
        )
        msg_box.cancelButton.hide()
        msg_box.exec()

    def javaScriptConfirm(self, securityOrigin, msg):
        msg_box = MessageBox(
            f"JavaScript confirm - {securityOrigin.toString()}", msg, self.window
        )
        return msg_box.exec()

    def javaScriptPrompt(self, securityOrigin, msg, defaultValue):
        input_dialog = InputMessageBox(msg, defaultValue, self.window)
        if input_dialog.exec():
            return (True, input_dialog.line_edit.text())
        else:
            return (False, "")

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        if level == QWebEnginePage.JavaScriptConsoleMessageLevel.InfoMessageLevel:
            logging.info(
                f"JavaScript Console Info: {message} (Level: {level}, "
                f"Line: {lineNumber}, Source: {sourceID})"
            )
        elif level == QWebEnginePage.JavaScriptConsoleMessageLevel.WarningMessageLevel:
            logging.warning(
                f"JavaScript Console Warning: {message} (Level: {level}, "
                f"Line: {lineNumber}, Source: {sourceID})"
            )
        elif level == QWebEnginePage.JavaScriptConsoleMessageLevel.ErrorMessageLevel:
            logging.error(
                f"JavaScript Console Error: {message} (Level: {level}, "
                f"Line: {lineNumber}, Source: {sourceID})"
            )
