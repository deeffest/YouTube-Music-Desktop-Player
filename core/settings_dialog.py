import platform
from typing import TYPE_CHECKING

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QSystemTrayIcon

from core.helpers import recolor_icon
from core.ui.ui_settings_dialog import Ui_SettingsDialog

if TYPE_CHECKING:
    from main_window import MainWindow


class SettingsDialog(QDialog, Ui_SettingsDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window: "MainWindow" = parent

        self.configure_window()
        self.configure_ui_elements()

    def configure_window(self):
        self.setupUi(self)
        self.setWindowIcon(QIcon(f"{self.window.icon_folder}/settings-colored.png"))

    def configure_ui_elements(self):
        def remove_deno_from_device():
            self.window.remove_tool_from_device("Deno")
            self.pushButton_3.setEnabled(False)

        def remove_ffmpeg_from_device():
            self.window.remove_tool_from_device("FFmpeg")
            self.pushButton_2.setEnabled(False)

        def remove_ytdlp_from_device():
            self.window.remove_tool_from_device("yt-dlp")
            self.pushButton.setEnabled(False)

        def delete_all_saved_cookies():
            self.window.delete_all_cookies()
            self.pushButton_4.setEnabled(False)

        self.buttonBox.accepted.connect(self.save_settings)
        self.buttonBox.rejected.connect(self.close)

        self.checkBox.setChecked(self.window.save_last_win_geometry_setting)
        self.checkBox_2.setChecked(self.window.open_last_url_at_startup_setting)
        self.checkBox_3.setChecked(self.window.save_last_zoom_factor_setting)
        self.checkBox_7.setChecked(self.window.light_theme_setting)
        self.comboBox_2.setCurrentIndex(
            1
            if self.window.icon_color_setting == 1
            else 2 if self.window.icon_color_setting == 2 else 0
        )
        self.checkBox_10.setChecked(self.window.tray_icon_setting)
        if not QSystemTrayIcon.isSystemTrayAvailable():
            self.checkBox_10.setEnabled(False)
            self.checkBox_10.setToolTip("System tray is not available.")
        self.checkBox_11.setChecked(self.window.discord_rpc_setting)
        self.checkBox_13.setChecked(self.window.hotkey_playback_control_setting)
        self.checkBox_8.setChecked(self.window.fullscreen_mode_support_setting)
        self.checkBox_9.setChecked(self.window.support_animated_scrolling_setting)
        self.checkBox_12.setChecked(self.window.disable_frame_rate_limit_setting)
        self.checkBox_15.setChecked(self.window.do_not_save_cookies_setting)
        self.pushButton_4.setIcon(
            recolor_icon(
                f"{self.window.icon_folder}/delete.png", self.window.light_theme_setting
            )
        )
        self.pushButton_4.clicked.connect(delete_all_saved_cookies)
        self.checkBox_4.setChecked(self.window.use_cookies_setting)
        if self.window.prefer_system_ytdlp_setting == 0:
            self.checkBox_6.setChecked(self.window.auto_update_ytdlp_setting)
        else:
            self.checkBox_6.setEnabled(False)
            self.checkBox_6.setToolTip("Not available for the system yt-dlp.")
        self.checkBox_17.setChecked(self.window.embed_metadata_setting)
        self.comboBox_3.setCurrentIndex(
            1
            if self.window.ytdlp_format_setting == 1
            else (
                2
                if self.window.ytdlp_format_setting == 2
                else 3 if self.window.ytdlp_format_setting == 3 else 0
            )
        )
        self.comboBox_3.setItemIcon(
            0,
            recolor_icon(
                f"{self.window.icon_folder}/audio.png", self.window.light_theme_setting
            ),
        )
        self.comboBox_3.setItemIcon(
            1,
            recolor_icon(
                f"{self.window.icon_folder}/audio.png", self.window.light_theme_setting
            ),
        )
        self.comboBox_3.setItemIcon(
            2,
            recolor_icon(
                f"{self.window.icon_folder}/video.png", self.window.light_theme_setting
            ),
        )
        self.comboBox_3.setItemIcon(
            3,
            recolor_icon(
                f"{self.window.icon_folder}/video.png", self.window.light_theme_setting
            ),
        )
        if self.window.is_downloading or not self.window.check_tool_availability(
            "yt-dlp"
        ):
            self.pushButton.setEnabled(False)
        self.pushButton.setIcon(
            recolor_icon(
                f"{self.window.icon_folder}/remove.png", self.window.light_theme_setting
            )
        )
        self.pushButton.clicked.connect(remove_ytdlp_from_device)
        if self.window.is_downloading or not self.window.check_tool_availability(
            "FFmpeg"
        ):
            self.pushButton_2.setEnabled(False)
        self.pushButton_2.setIcon(
            recolor_icon(
                f"{self.window.icon_folder}/remove.png", self.window.light_theme_setting
            )
        )
        self.pushButton_2.clicked.connect(remove_ffmpeg_from_device)
        if self.window.is_downloading or not self.window.check_tool_availability(
            "Deno"
        ):
            self.pushButton_3.setEnabled(False)
        self.pushButton_3.setIcon(
            recolor_icon(
                f"{self.window.icon_folder}/remove.png", self.window.light_theme_setting
            )
        )
        self.pushButton_3.clicked.connect(remove_deno_from_device)
        self.lineEdit.setText(self.window.audd_api_token_setting)
        self.label_6.setText(f"{self.window.audd_recording_lenght_setting}s")
        self.label_6.setFixedWidth(
            self.label_6.fontMetrics().horizontalAdvance(
                str(self.horizontalSlider.maximum()) + "s"
            )
        )
        self.horizontalSlider.setValue(self.window.audd_recording_lenght_setting)
        self.horizontalSlider.valueChanged.connect(
            lambda value: self.label_6.setText(f"{value}s")
        )
        self.checkBox_5.setChecked(self.window.prefer_system_ffmpeg_setting)
        self.checkBox_18.setChecked(self.window.prefer_system_deno_setting)
        self.checkBox_14.setChecked(self.window.win_thumbnail_buttons_setting)
        if not platform.system() == "Windows":
            self.checkBox_14.setEnabled(False)
            self.checkBox_14.setToolTip("Works only on Windows.")
        self.checkBox_16.setChecked(self.window.prefer_system_ytdlp_setting)

    def save_settings(self):
        self.window.save_last_win_geometry_setting = int(self.checkBox.isChecked())
        self.window.settings_.setValue(
            "save_last_win_geometry", self.window.save_last_win_geometry_setting
        )
        self.window.open_last_url_at_startup_setting = int(self.checkBox_2.isChecked())
        self.window.settings_.setValue(
            "open_last_url_at_startup", self.window.open_last_url_at_startup_setting
        )
        self.window.save_last_zoom_factor_setting = int(self.checkBox_3.isChecked())
        self.window.settings_.setValue(
            "save_last_zoom_factor", self.window.save_last_zoom_factor_setting
        )
        self.window.light_theme_setting = int(self.checkBox_7.isChecked())
        self.window.settings_.setValue("light_theme", self.window.light_theme_setting)
        self.window.icon_color_setting = int(self.comboBox_2.currentIndex())
        self.window.settings_.setValue("icon_color", self.window.icon_color_setting)
        self.window.tray_icon_setting = int(self.checkBox_10.isChecked())
        self.window.settings_.setValue("tray_icon", self.window.tray_icon_setting)
        self.window.discord_rpc_setting = int(self.checkBox_11.isChecked())
        self.window.settings_.setValue("discord_rpc", self.window.discord_rpc_setting)
        self.window.hotkey_playback_control_setting = int(self.checkBox_13.isChecked())
        self.window.settings_.setValue(
            "hotkey_playback_control", self.window.hotkey_playback_control_setting
        )
        self.window.fullscreen_mode_support_setting = int(self.checkBox_8.isChecked())
        self.window.settings_.setValue(
            "fullscreen_mode_support", self.window.fullscreen_mode_support_setting
        )
        self.window.support_animated_scrolling_setting = int(
            self.checkBox_9.isChecked()
        )
        self.window.settings_.setValue(
            "support_animated_scrolling", self.window.support_animated_scrolling_setting
        )
        self.window.disable_frame_rate_limit_setting = int(self.checkBox_12.isChecked())
        self.window.settings_.setValue(
            "disable_frame_rate_limit", self.window.disable_frame_rate_limit_setting
        )
        self.window.do_not_save_cookies_setting = int(self.checkBox_15.isChecked())
        self.window.settings_.setValue(
            "do_not_save_cookies", self.window.do_not_save_cookies_setting
        )
        self.window.use_cookies_setting = self.checkBox_4.isChecked()
        self.window.settings_.setValue(
            "use_cookies", "true" if self.window.use_cookies_setting else "false"
        )
        self.window.auto_update_ytdlp_setting = self.checkBox_6.isChecked()
        self.window.settings_.setValue(
            "auto_update_ytdlp",
            "true" if self.window.auto_update_ytdlp_setting else "false",
        )
        self.window.embed_metadata_setting = int(self.checkBox_17.isChecked())
        self.window.settings_.setValue(
            "embed_metadata", self.window.embed_metadata_setting
        )
        self.window.ytdlp_format_setting = int(self.comboBox_3.currentIndex())
        self.window.settings_.setValue("ytdlp_format", self.window.ytdlp_format_setting)
        self.window.audd_api_token_setting = self.lineEdit.text()
        self.window.settings_.setValue(
            "audd_api_token", self.window.audd_api_token_setting
        )
        self.window.audd_recording_lenght_setting = int(self.horizontalSlider.value())
        self.window.settings_.setValue(
            "audd_recording_lenght", self.window.audd_recording_lenght_setting
        )
        self.window.prefer_system_ffmpeg_setting = int(self.checkBox_5.isChecked())
        self.window.settings_.setValue(
            "prefer_system_ffmpeg", self.window.prefer_system_ffmpeg_setting
        )
        self.window.prefer_system_deno_setting = int(self.checkBox_18.isChecked())
        self.window.settings_.setValue(
            "prefer_system_deno", self.window.prefer_system_deno_setting
        )
        self.window.win_thumbnail_buttons_setting = int(self.checkBox_14.isChecked())
        self.window.settings_.setValue(
            "win_thumbnail_buttons", self.window.win_thumbnail_buttons_setting
        )
        self.window.prefer_system_ytdlp_setting = int(self.checkBox_16.isChecked())
        self.window.settings_.setValue(
            "prefer_system_ytdlp", self.window.prefer_system_ytdlp_setting
        )

        self.close()

    def fix_size(self):
        hint = self.minimumSizeHint()
        if self.width() < hint.width() or self.height() < hint.height():
            self.resize(hint)

    def focusNextPrevChild(self, next):
        return False

    def showEvent(self, event):
        super().showEvent(event)
        hint = self.minimumSizeHint()
        current_min = self.minimumSize()
        if hint.width() > current_min.width() or hint.height() > current_min.height():
            self.setMinimumSize(hint)
        self.fix_size()

    def resizeEvent(self, event):
        self.fix_size()
        super().resizeEvent(event)

    def closeEvent(self, event):
        self.window.settings_dialog = None
        event.accept()
