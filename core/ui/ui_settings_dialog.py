# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QFrame, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSlider, QSpacerItem, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        if not SettingsDialog.objectName():
            SettingsDialog.setObjectName(u"SettingsDialog")
        SettingsDialog.resize(320, 500)
        SettingsDialog.setMinimumSize(QSize(320, 500))
        self.horizontalLayout_2 = QHBoxLayout(SettingsDialog)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(SettingsDialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.frame)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_2 = QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(self.tab)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.checkBox = QCheckBox(self.groupBox)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.verticalLayout_3.addWidget(self.checkBox)

        self.checkBox_2 = QCheckBox(self.groupBox)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.verticalLayout_3.addWidget(self.checkBox_2)

        self.checkBox_3 = QCheckBox(self.groupBox)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.verticalLayout_3.addWidget(self.checkBox_3)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.groupBox_8 = QGroupBox(self.tab)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.verticalLayout_11 = QVBoxLayout(self.groupBox_8)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.checkBox_7 = QCheckBox(self.groupBox_8)
        self.checkBox_7.setObjectName(u"checkBox_7")
        self.checkBox_7.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.verticalLayout_11.addWidget(self.checkBox_7)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.groupBox_8)
        self.label.setObjectName(u"label")
        self.label.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.horizontalLayout_3.addWidget(self.label)

        self.comboBox_2 = QComboBox(self.groupBox_8)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBox_2.sizePolicy().hasHeightForWidth())
        self.comboBox_2.setSizePolicy(sizePolicy1)
        self.comboBox_2.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.horizontalLayout_3.addWidget(self.comboBox_2)


        self.verticalLayout_11.addLayout(self.horizontalLayout_3)


        self.verticalLayout_2.addWidget(self.groupBox_8)

        self.groupBox_10 = QGroupBox(self.tab)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.verticalLayout_14 = QVBoxLayout(self.groupBox_10)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.checkBox_14 = QCheckBox(self.groupBox_10)
        self.checkBox_14.setObjectName(u"checkBox_14")

        self.verticalLayout_14.addWidget(self.checkBox_14)

        self.checkBox_10 = QCheckBox(self.groupBox_10)
        self.checkBox_10.setObjectName(u"checkBox_10")
        self.checkBox_10.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.verticalLayout_14.addWidget(self.checkBox_10)

        self.checkBox_11 = QCheckBox(self.groupBox_10)
        self.checkBox_11.setObjectName(u"checkBox_11")
        self.checkBox_11.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.verticalLayout_14.addWidget(self.checkBox_11)

        self.checkBox_13 = QCheckBox(self.groupBox_10)
        self.checkBox_13.setObjectName(u"checkBox_13")
        self.checkBox_13.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.verticalLayout_14.addWidget(self.checkBox_13)


        self.verticalLayout_2.addWidget(self.groupBox_10)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_4 = QVBoxLayout(self.tab_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBox_2 = QGroupBox(self.tab_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_12 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.checkBox_8 = QCheckBox(self.groupBox_2)
        self.checkBox_8.setObjectName(u"checkBox_8")
        self.checkBox_8.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.verticalLayout_12.addWidget(self.checkBox_8)

        self.checkBox_9 = QCheckBox(self.groupBox_2)
        self.checkBox_9.setObjectName(u"checkBox_9")
        self.checkBox_9.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.verticalLayout_12.addWidget(self.checkBox_9)


        self.verticalLayout_4.addWidget(self.groupBox_2)

        self.groupBox_4 = QGroupBox(self.tab_2)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.checkBox_12 = QCheckBox(self.groupBox_4)
        self.checkBox_12.setObjectName(u"checkBox_12")

        self.verticalLayout_6.addWidget(self.checkBox_12)


        self.verticalLayout_4.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(self.tab_2)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.checkBox_15 = QCheckBox(self.groupBox_5)
        self.checkBox_15.setObjectName(u"checkBox_15")
        self.checkBox_15.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.verticalLayout_7.addWidget(self.checkBox_15)

        self.pushButton_4 = QPushButton(self.groupBox_5)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pushButton_4.setAutoDefault(False)

        self.verticalLayout_7.addWidget(self.pushButton_4)


        self.verticalLayout_4.addWidget(self.groupBox_5)

        self.verticalSpacer_2 = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.verticalLayout_5 = QVBoxLayout(self.tab_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.groupBox_3 = QGroupBox(self.tab_4)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setCheckable(False)
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(self.groupBox_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.horizontalLayout_4.addWidget(self.label_3)

        self.comboBox_3 = QComboBox(self.groupBox_3)
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")
        sizePolicy1.setHeightForWidth(self.comboBox_3.sizePolicy().hasHeightForWidth())
        self.comboBox_3.setSizePolicy(sizePolicy1)
        self.comboBox_3.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.horizontalLayout_4.addWidget(self.comboBox_3)


        self.verticalLayout_8.addLayout(self.horizontalLayout_4)

        self.checkBox_4 = QCheckBox(self.groupBox_3)
        self.checkBox_4.setObjectName(u"checkBox_4")
        self.checkBox_4.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.verticalLayout_8.addWidget(self.checkBox_4)

        self.checkBox_6 = QCheckBox(self.groupBox_3)
        self.checkBox_6.setObjectName(u"checkBox_6")
        self.checkBox_6.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.verticalLayout_8.addWidget(self.checkBox_6)

        self.checkBox_17 = QCheckBox(self.groupBox_3)
        self.checkBox_17.setObjectName(u"checkBox_17")
        self.checkBox_17.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.verticalLayout_8.addWidget(self.checkBox_17)

        self.pushButton = QPushButton(self.groupBox_3)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pushButton.setAutoDefault(False)

        self.verticalLayout_8.addWidget(self.pushButton)


        self.verticalLayout_5.addWidget(self.groupBox_3)

        self.groupBox_6 = QGroupBox(self.tab_4)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setEnabled(True)
        self.groupBox_6.setFlat(False)
        self.groupBox_6.setCheckable(False)
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.checkBox_5 = QCheckBox(self.groupBox_6)
        self.checkBox_5.setObjectName(u"checkBox_5")
        self.checkBox_5.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.verticalLayout_9.addWidget(self.checkBox_5)

        self.pushButton_2 = QPushButton(self.groupBox_6)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pushButton_2.setAutoDefault(False)

        self.verticalLayout_9.addWidget(self.pushButton_2)


        self.verticalLayout_5.addWidget(self.groupBox_6)

        self.groupBox_7 = QGroupBox(self.tab_4)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setCheckable(False)
        self.verticalLayout_10 = QVBoxLayout(self.groupBox_7)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.checkBox_18 = QCheckBox(self.groupBox_7)
        self.checkBox_18.setObjectName(u"checkBox_18")
        self.checkBox_18.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.verticalLayout_10.addWidget(self.checkBox_18)

        self.pushButton_3 = QPushButton(self.groupBox_7)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pushButton_3.setAutoDefault(False)

        self.verticalLayout_10.addWidget(self.pushButton_3)


        self.verticalLayout_5.addWidget(self.groupBox_7)

        self.verticalSpacer_4 = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_4)

        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.verticalLayout_18 = QVBoxLayout(self.tab_5)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.groupBox_12 = QGroupBox(self.tab_5)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.verticalLayout_17 = QVBoxLayout(self.groupBox_12)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_4 = QLabel(self.groupBox_12)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_5.addWidget(self.label_4)

        self.lineEdit = QLineEdit(self.groupBox_12)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        self.horizontalLayout_5.addWidget(self.lineEdit)


        self.verticalLayout_17.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_5 = QLabel(self.groupBox_12)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.horizontalLayout_6.addWidget(self.label_5)

        self.horizontalSlider = QSlider(self.groupBox_12)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(12)
        self.horizontalSlider.setPageStep(1)
        self.horizontalSlider.setOrientation(Qt.Orientation.Horizontal)
        self.horizontalSlider.setTickPosition(QSlider.TickPosition.TicksBelow)

        self.horizontalLayout_6.addWidget(self.horizontalSlider)

        self.label_6 = QLabel(self.groupBox_12)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_6.addWidget(self.label_6)


        self.verticalLayout_17.addLayout(self.horizontalLayout_6)


        self.verticalLayout_18.addWidget(self.groupBox_12)

        self.verticalSpacer_5 = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)

        self.verticalLayout_18.addItem(self.verticalSpacer_5)

        self.tabWidget.addTab(self.tab_5, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.buttonBox = QDialogButtonBox(self.frame)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Save)

        self.verticalLayout.addWidget(self.buttonBox)


        self.horizontalLayout_2.addWidget(self.frame)


        self.retranslateUi(SettingsDialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(SettingsDialog)
    # setupUi

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QCoreApplication.translate("SettingsDialog", u"Settings", None))
        self.groupBox.setTitle(QCoreApplication.translate("SettingsDialog", u"Startup", None))
        self.checkBox.setText(QCoreApplication.translate("SettingsDialog", u"Restore window geometry", None))
        self.checkBox_2.setText(QCoreApplication.translate("SettingsDialog", u"Restore last URL", None))
        self.checkBox_3.setText(QCoreApplication.translate("SettingsDialog", u"Restore zoom factor", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("SettingsDialog", u"Appearance", None))
        self.checkBox_7.setText(QCoreApplication.translate("SettingsDialog", u"Light theme", None))
        self.label.setText(QCoreApplication.translate("SettingsDialog", u"Icon color", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("SettingsDialog", u"Auto", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("SettingsDialog", u"Dark", None))
        self.comboBox_2.setItemText(2, QCoreApplication.translate("SettingsDialog", u"Light", None))

#if QT_CONFIG(tooltip)
        self.comboBox_2.setToolTip(QCoreApplication.translate("SettingsDialog", u"<html><head/><body><p>This setting applies only to the icons in the system tray.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_10.setTitle(QCoreApplication.translate("SettingsDialog", u"Features", None))
        self.checkBox_14.setText(QCoreApplication.translate("SettingsDialog", u"Windows thumbnail buttons", None))
        self.checkBox_10.setText(QCoreApplication.translate("SettingsDialog", u"System tray icon", None))
        self.checkBox_11.setText(QCoreApplication.translate("SettingsDialog", u"Discord Rich Presence", None))
#if QT_CONFIG(tooltip)
        self.checkBox_13.setToolTip(QCoreApplication.translate("SettingsDialog", u"\u2022 Ctrl + Shift + Space: Play/Pause.\n"
"\u2022 Ctrl + Shift + Left: Previous.\n"
"\u2022 Ctrl + Shift + Right: Next.", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_13.setText(QCoreApplication.translate("SettingsDialog", u"Global playback hotkeys", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("SettingsDialog", u"General", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("SettingsDialog", u"Features", None))
        self.checkBox_8.setText(QCoreApplication.translate("SettingsDialog", u"Full-screen mode support", None))
        self.checkBox_9.setText(QCoreApplication.translate("SettingsDialog", u"Animated scrolling support", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("SettingsDialog", u"Rendering", None))
#if QT_CONFIG(tooltip)
        self.checkBox_12.setToolTip(QCoreApplication.translate("SettingsDialog", u"This setting removes the 60 fps limit,\n"
"but puts a heavy load on the CPU\n"
"during video playback (even in the background).\n"
"\n"
"Recommended to use only with\n"
"the Audio-only mode plugin.", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_12.setText(QCoreApplication.translate("SettingsDialog", u"Disable frame rate limit", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("SettingsDialog", u"Cookies", None))
        self.checkBox_15.setText(QCoreApplication.translate("SettingsDialog", u"Do not save cookies to disk", None))
        self.pushButton_4.setText(QCoreApplication.translate("SettingsDialog", u"Delete all saved cookies", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("SettingsDialog", u"Web engine", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("SettingsDialog", u"yt-dlp", None))
        self.label_3.setText(QCoreApplication.translate("SettingsDialog", u"Format", None))
        self.comboBox_3.setItemText(0, QCoreApplication.translate("SettingsDialog", u"Opus", None))
        self.comboBox_3.setItemText(1, QCoreApplication.translate("SettingsDialog", u"M4A", None))
        self.comboBox_3.setItemText(2, QCoreApplication.translate("SettingsDialog", u"MP4", None))
        self.comboBox_3.setItemText(3, QCoreApplication.translate("SettingsDialog", u"WebM", None))

        self.checkBox_4.setText(QCoreApplication.translate("SettingsDialog", u"Use cookies", None))
        self.checkBox_6.setText(QCoreApplication.translate("SettingsDialog", u"Auto update", None))
        self.checkBox_17.setText(QCoreApplication.translate("SettingsDialog", u"Embed metadata", None))
        self.pushButton.setText(QCoreApplication.translate("SettingsDialog", u"Remove from device", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("SettingsDialog", u"FFmpeg", None))
#if QT_CONFIG(tooltip)
        self.checkBox_5.setToolTip(QCoreApplication.translate("SettingsDialog", u"The system's FFmpeg will be used, if available.", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_5.setText(QCoreApplication.translate("SettingsDialog", u"Prefer system FFmpeg", None))
#if QT_CONFIG(tooltip)
        self.pushButton_2.setToolTip(QCoreApplication.translate("SettingsDialog", u"This will not remove the system version of FFmpeg - only the built-in version.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_2.setText(QCoreApplication.translate("SettingsDialog", u"Remove from device", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("SettingsDialog", u"Deno", None))
#if QT_CONFIG(tooltip)
        self.checkBox_18.setToolTip(QCoreApplication.translate("SettingsDialog", u"The system's Deno will be used, if available.", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_18.setText(QCoreApplication.translate("SettingsDialog", u"Prefer system Deno", None))
#if QT_CONFIG(tooltip)
        self.pushButton_3.setToolTip(QCoreApplication.translate("SettingsDialog", u"This will not remove the system version of Deno - only the built-in version.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_3.setText(QCoreApplication.translate("SettingsDialog", u"Remove from device", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("SettingsDialog", u"Tools", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("SettingsDialog", u"AudD API", None))
        self.label_4.setText(QCoreApplication.translate("SettingsDialog", u"Token", None))
#if QT_CONFIG(tooltip)
        self.lineEdit.setToolTip(QCoreApplication.translate("SettingsDialog", u"To get more than 10 recognitions, obtain a token from the AudD API dashboard.", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("SettingsDialog", u"Enter your AudD token here", None))
        self.label_5.setText(QCoreApplication.translate("SettingsDialog", u"Recording lenght", None))
#if QT_CONFIG(tooltip)
        self.horizontalSlider.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("SettingsDialog", u"1s", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("SettingsDialog", u"Music recognition", None))
    # retranslateUi

