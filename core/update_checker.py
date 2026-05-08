import logging
from typing import TYPE_CHECKING

import requests
from PySide6.QtCore import QThread, Signal

if TYPE_CHECKING:
    from core.main_window import MainWindow


class UpdateChecker(QThread):
    update_checked = Signal(str, str, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.window: "MainWindow" = parent

    def run(self):
        try:
            response = requests.get(
                f"https://api.github.com/repos/{self.window.author}/"
                f"{self.window.name}/releases/latest",
                timeout=10,
            )
            response.raise_for_status()

            data = response.json()
            last_version = data["tag_name"]
            title = data.get("name")
            whats_new = data.get("body")
            last_release_url = data.get("html_url")

            self.update_checked.emit(last_version, title, whats_new, last_release_url)
        except Exception as e:
            logging.error(f"Failed to check for updates: {str(e)}")

    def stop(self):
        self.terminate()
        self.wait()
