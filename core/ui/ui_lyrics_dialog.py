# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'lyrics_dialog.ui'
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

class Ui_LyricsDialog(object):
    def setupUi(self, LyricsDialog):
        if not LyricsDialog.objectName():
            LyricsDialog.setObjectName(u"LyricsDialog")
        LyricsDialog.resize(380, 580)
        self.verticalLayout_2 = QVBoxLayout(LyricsDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(LyricsDialog)

        QMetaObject.connectSlotsByName(LyricsDialog)
    # setupUi

    def retranslateUi(self, LyricsDialog):
        LyricsDialog.setWindowTitle(QCoreApplication.translate("LyricsDialog", u"Lyrics", None))
    # retranslateUi

