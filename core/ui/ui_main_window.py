# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.8.3
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QMainWindow,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from qfluentwidgets import (BodyLabel, TransparentDropDownToolButton, TransparentToolButton, TransparentToolButtonWithMenu)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(789, 495)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.ToolBar = QFrame(self.centralwidget)
        self.ToolBar.setObjectName(u"ToolBar")
        self.toolbar_layout = QHBoxLayout(self.ToolBar)
        self.toolbar_layout.setSpacing(0)
        self.toolbar_layout.setObjectName(u"toolbar_layout")
        self.toolbar_layout.setContentsMargins(6, 4, 6, 4)
        self.back_tbutton = TransparentToolButton(self.ToolBar)
        self.back_tbutton.setObjectName(u"back_tbutton")
        self.back_tbutton.setEnabled(False)
        self.back_tbutton.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.toolbar_layout.addWidget(self.back_tbutton)

        self.forward_tbutton = TransparentToolButton(self.ToolBar)
        self.forward_tbutton.setObjectName(u"forward_tbutton")
        self.forward_tbutton.setEnabled(False)
        self.forward_tbutton.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.toolbar_layout.addWidget(self.forward_tbutton)

        self.reload_tbutton = TransparentToolButton(self.ToolBar)
        self.reload_tbutton.setObjectName(u"reload_tbutton")
        self.reload_tbutton.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.toolbar_layout.addWidget(self.reload_tbutton)

        self.horizontalSpacer = QSpacerItem(6, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.toolbar_layout.addItem(self.horizontalSpacer)

        self.url_label = BodyLabel(self.ToolBar)
        self.url_label.setObjectName(u"url_label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.url_label.sizePolicy().hasHeightForWidth())
        self.url_label.setSizePolicy(sizePolicy)
        self.url_label.setMinimumSize(QSize(30, 0))
        self.url_label.setStyleSheet(u"QLabel {\n"
"    color: rgb(210, 210, 210);\n"
"    background-color: rgb(33, 33, 33);\n"
"    border: 1px solid transparent;\n"
"    border-radius: 6px;\n"
"    padding: 3px 6px;\n"
"}\n"
"QLabel:hover {\n"
"    border: 1px solid rgb(255, 41, 41);\n"
"}\n"
"")

        self.toolbar_layout.addWidget(self.url_label)

        self.horizontalSpacer_2 = QSpacerItem(6, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.toolbar_layout.addItem(self.horizontalSpacer_2)

        self.download_ddtbutton = TransparentDropDownToolButton(self.ToolBar)
        self.download_ddtbutton.setObjectName(u"download_ddtbutton")
        self.download_ddtbutton.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.toolbar_layout.addWidget(self.download_ddtbutton)

        self.lyrics_tbutton = TransparentToolButton(self.ToolBar)
        self.lyrics_tbutton.setObjectName(u"lyrics_tbutton")

        self.toolbar_layout.addWidget(self.lyrics_tbutton)

        self.comments_tbutton = TransparentToolButton(self.ToolBar)
        self.comments_tbutton.setObjectName(u"comments_tbutton")

        self.toolbar_layout.addWidget(self.comments_tbutton)

        self.settings_ddtbutton = TransparentToolButtonWithMenu(self.ToolBar)
        self.settings_ddtbutton.setObjectName(u"settings_ddtbutton")
        self.settings_ddtbutton.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.toolbar_layout.addWidget(self.settings_ddtbutton)

        self.plugins_ddtbutton = TransparentDropDownToolButton(self.ToolBar)
        self.plugins_ddtbutton.setObjectName(u"plugins_ddtbutton")
        self.plugins_ddtbutton.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.toolbar_layout.addWidget(self.plugins_ddtbutton)

        self.more_ddtbutton = TransparentToolButtonWithMenu(self.ToolBar)
        self.more_ddtbutton.setObjectName(u"more_ddtbutton")
        self.more_ddtbutton.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.toolbar_layout.addWidget(self.more_ddtbutton)


        self.verticalLayout.addWidget(self.ToolBar)

        self.MainLayout = QHBoxLayout()
        self.MainLayout.setObjectName(u"MainLayout")
        self.verticalSpacer = QSpacerItem(0, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.MainLayout.addItem(self.verticalSpacer)


        self.verticalLayout.addLayout(self.MainLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"YouTube Music Desktop Player", None))
#if QT_CONFIG(tooltip)
        self.back_tbutton.setToolTip(QCoreApplication.translate("MainWindow", u"Back", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.forward_tbutton.setToolTip(QCoreApplication.translate("MainWindow", u"Forward", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.reload_tbutton.setToolTip(QCoreApplication.translate("MainWindow", u"Reload", None))
#endif // QT_CONFIG(tooltip)
        self.url_label.setText(QCoreApplication.translate("MainWindow", u"music.youtube.com", None))
#if QT_CONFIG(tooltip)
        self.download_ddtbutton.setToolTip(QCoreApplication.translate("MainWindow", u"Download", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.lyrics_tbutton.setToolTip(QCoreApplication.translate("MainWindow", u"Lyrics...", None))
#endif // QT_CONFIG(tooltip)
        self.lyrics_tbutton.setText("")
#if QT_CONFIG(tooltip)
        self.comments_tbutton.setToolTip(QCoreApplication.translate("MainWindow", u"Comments...", None))
#endif // QT_CONFIG(tooltip)
        self.comments_tbutton.setText("")
#if QT_CONFIG(tooltip)
        self.settings_ddtbutton.setToolTip(QCoreApplication.translate("MainWindow", u"Settings...", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.plugins_ddtbutton.setToolTip(QCoreApplication.translate("MainWindow", u"Plugins", None))
#endif // QT_CONFIG(tooltip)
        self.plugins_ddtbutton.setText("")
#if QT_CONFIG(tooltip)
        self.more_ddtbutton.setToolTip(QCoreApplication.translate("MainWindow", u"More", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

