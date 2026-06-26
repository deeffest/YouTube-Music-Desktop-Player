from typing import TYPE_CHECKING

from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineContextMenuData

if TYPE_CHECKING:
    from core.main_window import MainWindow


class WebEngineView(QWebEngineView):
    def __init__(self, parent=None):
        super(WebEngineView, self).__init__(parent)
        self.window: "MainWindow" = parent

    def contextMenuEvent(self, event):
        context_data = self.page().contextMenuData()
        flags = context_data.editFlags()

        if context_data.isContentEditable() and self.page().selectedText():
            self.window.edit_menu.actions()[0].setEnabled(
                flags & QWebEngineContextMenuData.CanCopy
            )
            self.window.edit_menu.actions()[1].setEnabled(
                flags & QWebEngineContextMenuData.CanPaste
            )
            self.window.edit_menu.exec(event.globalPos())
        elif context_data.isContentEditable():
            self.window.paste_menu.actions()[0].setEnabled(
                flags & QWebEngineContextMenuData.CanPaste
            )
            self.window.paste_menu.exec(event.globalPos())
        elif self.page().selectedText():
            self.window.copy_menu.actions()[0].setEnabled(
                flags & QWebEngineContextMenuData.CanCopy
            )
            self.window.copy_menu.exec(event.globalPos())
        else:
            self.window.main_menu.exec(event.globalPos())

        event.accept()
