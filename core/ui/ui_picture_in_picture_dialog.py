# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'picture_in_picture_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from qfluentwidgets import (BodyLabel, StrongBodyLabel, TransparentToolButton)

class Ui_PictureInPictureDialog(object):
    def setupUi(self, PictureInPictureDialog):
        if not PictureInPictureDialog.objectName():
            PictureInPictureDialog.setObjectName(u"PictureInPictureDialog")
        PictureInPictureDialog.resize(360, 150)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PictureInPictureDialog.sizePolicy().hasHeightForWidth())
        PictureInPictureDialog.setSizePolicy(sizePolicy)
        PictureInPictureDialog.setMinimumSize(QSize(360, 150))
        PictureInPictureDialog.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(PictureInPictureDialog)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 18, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(12)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(16, -1, 16, 6)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")

        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.title_label = StrongBodyLabel(PictureInPictureDialog)
        self.title_label.setObjectName(u"title_label")

        self.verticalLayout_2.addWidget(self.title_label)

        self.artist_label = BodyLabel(PictureInPictureDialog)
        self.artist_label.setObjectName(u"artist_label")
        self.artist_label.setStyleSheet(u"QLabel {\n"
"	color: lightgray;\n"
"	font-size: 13px;\n"
"}")

        self.verticalLayout_2.addWidget(self.artist_label)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.artwork_label = QLabel(PictureInPictureDialog)
        self.artwork_label.setObjectName(u"artwork_label")
        self.artwork_label.setMinimumSize(QSize(60, 60))
        self.artwork_label.setMaximumSize(QSize(60, 60))
        self.artwork_label.setScaledContents(False)
        self.artwork_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.artwork_label)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(16, 3, 16, 18)
        self.BodyLabel = BodyLabel(PictureInPictureDialog)
        self.BodyLabel.setObjectName(u"BodyLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.BodyLabel.sizePolicy().hasHeightForWidth())
        self.BodyLabel.setSizePolicy(sizePolicy1)
        self.BodyLabel.setMinimumSize(QSize(32, 0))
        self.BodyLabel.setMaximumSize(QSize(16777215, 16777215))
        self.BodyLabel.setStyleSheet(u"FluentLabelBase {\n"
"    color: black;\n"
"}\n"
"\n"
"HyperlinkLabel {\n"
"    color: #009faa;\n"
"    border: none;\n"
"    background-color: transparent;\n"
"    text-align: left;\n"
"    padding: 0;\n"
"    margin: 0;\n"
"}\n"
"\n"
"HyperlinkLabel[underline=true] {\n"
"    text-decoration: underline;\n"
"}\n"
"\n"
"HyperlinkLabel[underline=false] {\n"
"    text-decoration: none;\n"
"}\n"
"\n"
"HyperlinkLabel:hover {\n"
"    color: #007780;\n"
"}\n"
"\n"
"HyperlinkLabel:pressed {\n"
"    color: #00a7b3;\n"
"}\n"
"FluentLabelBase{color:lightgray}")

        self.horizontalLayout_3.addWidget(self.BodyLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.dislike_button = TransparentToolButton(PictureInPictureDialog)
        self.dislike_button.setObjectName(u"dislike_button")
        self.dislike_button.setMinimumSize(QSize(40, 40))
        self.dislike_button.setMaximumSize(QSize(40, 40))
        self.dislike_button.setIconSize(QSize(20, 20))

        self.horizontalLayout_3.addWidget(self.dislike_button)

        self.previous_button = TransparentToolButton(PictureInPictureDialog)
        self.previous_button.setObjectName(u"previous_button")
        self.previous_button.setMinimumSize(QSize(40, 40))
        self.previous_button.setMaximumSize(QSize(40, 40))
        self.previous_button.setIconSize(QSize(20, 20))

        self.horizontalLayout_3.addWidget(self.previous_button)

        self.play_pause_button = TransparentToolButton(PictureInPictureDialog)
        self.play_pause_button.setObjectName(u"play_pause_button")
        self.play_pause_button.setMinimumSize(QSize(40, 40))
        self.play_pause_button.setMaximumSize(QSize(40, 40))
        self.play_pause_button.setIconSize(QSize(22, 22))

        self.horizontalLayout_3.addWidget(self.play_pause_button)

        self.next_button = TransparentToolButton(PictureInPictureDialog)
        self.next_button.setObjectName(u"next_button")
        self.next_button.setMinimumSize(QSize(40, 40))
        self.next_button.setMaximumSize(QSize(40, 40))
        self.next_button.setIconSize(QSize(20, 20))

        self.horizontalLayout_3.addWidget(self.next_button)

        self.like_button = TransparentToolButton(PictureInPictureDialog)
        self.like_button.setObjectName(u"like_button")
        self.like_button.setMinimumSize(QSize(40, 40))
        self.like_button.setMaximumSize(QSize(40, 40))
        self.like_button.setIconSize(QSize(20, 20))

        self.horizontalLayout_3.addWidget(self.like_button)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.BodyLabel_2 = BodyLabel(PictureInPictureDialog)
        self.BodyLabel_2.setObjectName(u"BodyLabel_2")
        sizePolicy1.setHeightForWidth(self.BodyLabel_2.sizePolicy().hasHeightForWidth())
        self.BodyLabel_2.setSizePolicy(sizePolicy1)
        self.BodyLabel_2.setMinimumSize(QSize(32, 0))
        self.BodyLabel_2.setMaximumSize(QSize(16777215, 16777215))
        self.BodyLabel_2.setStyleSheet(u"FluentLabelBase {\n"
"    color: black;\n"
"}\n"
"\n"
"HyperlinkLabel {\n"
"    color: #009faa;\n"
"    border: none;\n"
"    background-color: transparent;\n"
"    text-align: left;\n"
"    padding: 0;\n"
"    margin: 0;\n"
"}\n"
"\n"
"HyperlinkLabel[underline=true] {\n"
"    text-decoration: underline;\n"
"}\n"
"\n"
"HyperlinkLabel[underline=false] {\n"
"    text-decoration: none;\n"
"}\n"
"\n"
"HyperlinkLabel:hover {\n"
"    color: #007780;\n"
"}\n"
"\n"
"HyperlinkLabel:pressed {\n"
"    color: #00a7b3;\n"
"}\n"
"FluentLabelBase{color:lightgray}")
        self.BodyLabel_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.BodyLabel_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(PictureInPictureDialog)

        QMetaObject.connectSlotsByName(PictureInPictureDialog)
    # setupUi

    def retranslateUi(self, PictureInPictureDialog):
        PictureInPictureDialog.setWindowTitle(QCoreApplication.translate("PictureInPictureDialog", u"Picture-in-Picture", None))
        self.title_label.setText("")
        self.artist_label.setText("")
        self.artwork_label.setText("")
        self.BodyLabel.setText(QCoreApplication.translate("PictureInPictureDialog", u"0:38", None))
#if QT_CONFIG(tooltip)
        self.dislike_button.setToolTip(QCoreApplication.translate("PictureInPictureDialog", u"Dislike", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.previous_button.setToolTip(QCoreApplication.translate("PictureInPictureDialog", u"Previous", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.previous_button.setShortcut(QCoreApplication.translate("PictureInPictureDialog", u"Left", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.play_pause_button.setToolTip(QCoreApplication.translate("PictureInPictureDialog", u"Play/Pause", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.play_pause_button.setShortcut(QCoreApplication.translate("PictureInPictureDialog", u"Space", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.next_button.setToolTip(QCoreApplication.translate("PictureInPictureDialog", u"Next", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.next_button.setShortcut(QCoreApplication.translate("PictureInPictureDialog", u"Right", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.like_button.setToolTip(QCoreApplication.translate("PictureInPictureDialog", u"Like", None))
#endif // QT_CONFIG(tooltip)
        self.BodyLabel_2.setText(QCoreApplication.translate("PictureInPictureDialog", u"2:34", None))
    # retranslateUi

