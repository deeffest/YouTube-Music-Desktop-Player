# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'comments_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.9.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_CommentsDialog(object):
    def setupUi(self, CommentsDialog):
        if not CommentsDialog.objectName():
            CommentsDialog.setObjectName(u"CommentsDialog")
        CommentsDialog.resize(450, 700)
        self.verticalLayout_2 = QVBoxLayout(CommentsDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(CommentsDialog)

        QMetaObject.connectSlotsByName(CommentsDialog)
    # setupUi

    def retranslateUi(self, CommentsDialog):
        CommentsDialog.setWindowTitle(QCoreApplication.translate("CommentsDialog", u"Comments", None))
    # retranslateUi

