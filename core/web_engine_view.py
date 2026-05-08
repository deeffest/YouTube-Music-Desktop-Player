from typing import TYPE_CHECKING

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineContextMenuRequest

if TYPE_CHECKING:
    from core.main_window import MainWindow


class WebEngineView(QWebEngineView):
    def __init__(self, parent=None):
        super(WebEngineView, self).__init__(parent)
        self.window: "MainWindow" = parent

    def contextMenuEvent(self, event):
        request = self.lastContextMenuRequest()
        flags = request.editFlags()

        if request.isContentEditable() and request.selectedText():
            self.window.edit_menu.actions()[0].setEnabled(
                bool(flags & QWebEngineContextMenuRequest.EditFlag.CanCopy)
            )
            self.window.edit_menu.actions()[1].setEnabled(
                bool(flags & QWebEngineContextMenuRequest.EditFlag.CanPaste)
            )
            self.window.edit_menu.exec(event.globalPos())

        elif request.isContentEditable():
            self.window.paste_menu.actions()[0].setEnabled(
                bool(flags & QWebEngineContextMenuRequest.EditFlag.CanPaste)
            )
            self.window.paste_menu.exec(event.globalPos())

        elif request.selectedText():
            self.window.copy_menu.actions()[0].setEnabled(
                bool(flags & QWebEngineContextMenuRequest.EditFlag.CanCopy)
            )
            self.window.copy_menu.exec(event.globalPos())

        else:
            self.window.main_menu.exec(event.globalPos())

        request.setAccepted(True)
