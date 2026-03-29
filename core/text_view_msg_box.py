from qfluentwidgets import MessageBoxBase, SubtitleLabel, TextEdit


class TextViewMessageBox(MessageBoxBase):
    def __init__(self, msg, text, parent=None):
        super().__init__(parent)
        self.title_label = SubtitleLabel(self)
        self.title_label.setText(msg)

        self.text_edit = TextEdit(self)
        self.text_edit.setText(text)
        self.text_edit.setReadOnly(True)

        self.viewLayout.addWidget(self.title_label)
        self.viewLayout.addWidget(self.text_edit)

        self.widget.setMinimumWidth(400)
        self.widget.setMinimumHeight(550)
