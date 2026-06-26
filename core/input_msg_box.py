from PyQt5.QtCore import QTimer
from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit


class InputMessageBox(MessageBoxBase):
    def __init__(self, msg, text=None, parent=None):
        super().__init__(parent)
        self.title_label = SubtitleLabel(self)
        self.title_label.setText(msg)

        self.line_edit = LineEdit(self)
        self.line_edit.setClearButtonEnabled(True)

        def set_focus_input():
            self.line_edit.setFocus()
            self.line_edit.selectAll()

        QTimer.singleShot(0, set_focus_input)

        self.line_edit.returnPressed.connect(self.yesButton.click)
        self.line_edit.textChanged.connect(self.on_text_changed)

        self.viewLayout.addWidget(self.title_label)
        self.viewLayout.addWidget(self.line_edit)

        self.widget.setMinimumWidth(400)
        self.yesButton.setDisabled(True)
        if text:
            self.line_edit.setText(text)

    def on_text_changed(self, text):
        self.yesButton.setEnabled(bool(text))
