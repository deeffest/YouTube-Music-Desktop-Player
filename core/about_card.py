from typing import TYPE_CHECKING

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from qfluentwidgets import AvatarWidget, BodyLabel, CaptionLabel

if TYPE_CHECKING:
    from core.main_window import MainWindow


class AboutCard(QWidget):
    def __init__(self, logo, name, version, parent=None):
        super().__init__(parent=parent)
        self.window: "MainWindow" = parent

        self.logo_widget = AvatarWidget(logo, self)
        self.logo_widget.setRadius(24)

        self.name_widget = BodyLabel(name, self)
        self.version_widget = CaptionLabel(version, self)

        gray = "lightgray" if self.window.light_theme_setting == 0 else "gray"
        self.version_widget.setStyleSheet(f"color: {gray}")

        self.name_widget.setFixedHeight(self.name_widget.fontMetrics().height())
        self.version_widget.setFixedHeight(self.version_widget.fontMetrics().height())

        text_layout = QVBoxLayout()
        text_layout.setSpacing(0)
        text_layout.setContentsMargins(0, 0, 30, 0)
        text_layout.addWidget(self.name_widget)
        text_layout.addWidget(self.version_widget)

        root_layout = QHBoxLayout(self)
        root_layout.setContentsMargins(0, 6, 0, 6)
        root_layout.setSpacing(12)
        root_layout.addWidget(self.logo_widget)
        root_layout.addLayout(text_layout)
