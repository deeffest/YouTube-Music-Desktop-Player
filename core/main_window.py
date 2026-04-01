import os
import sys
import json
import base64
import logging
import platform
from urllib.parse import urlparse

from PyQt5.QtCore import (
    Qt,
    QUrl,
    QSize,
    QRect,
    QFile,
    QPoint,
    QTimer,
    QEvent,
    QProcess,
    QTextStream,
)
from PyQt5.QtWidgets import (
    QAction,
    QShortcut,
    QFileDialog,
    QMainWindow,
    QApplication,
    QSystemTrayIcon,
)
from PyQt5.QtTest import QTest
from PyQt5.QtWebEngineWidgets import (
    QWebEnginePage,
    QWebEngineScript,
    QWebEngineProfile,
    QWebEngineSettings,
)
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtGui import QIcon, QKeySequence
from qfluentwidgets import (
    Theme,
    Action,
    InfoBar,
    setTheme,
    RoundMenu,
    MessageBox,
    PushButton,
    StateToolTip,
    SplashScreen,
    CheckableMenu,
    ToolTipFilter,
    setThemeColor,
    ToolTipPosition,
    InfoBarPosition,
)
from packaging import version as pkg_version
from discordrpc import RPC, Button, Activity, ProgressBar

from core.helpers import (
    open_url,
    copy_text,
    str_to_bool,
    clean_up_url,
    recolor_icon,
    is_valid_ytmusic_url,
    get_centered_geometry,
)
from core.about_card import AboutCard
from core.signal_bus import signal_bus
from core.multi_action import MultiAction
from core.update_checker import UpdateChecker
from core.web_engine_page import WebEnginePage
from core.web_engine_view import WebEngineView
from core.settings_dialog import SettingsDialog
from core.system_tray_icon import SystemTrayIcon
from core.ui.ui_main_window import Ui_MainWindow
from core.ytmusic_downloader import DownloadThread
from core.hotkey_controller import HotkeyController
from core.text_view_msg_box import TextViewMessageBox
from core.web_channel_backend import WebChannelBackend
from core.music_recognizer import MusicRecognizerThread
from core.picture_in_picture_dialog import PictureInPictureDialog

if platform.system() == "Windows":
    from PyQt5.QtWinExtras import (  # type: ignore
        QWinThumbnailToolBar,
        QWinThumbnailToolButton,
    )
    from pywinstyles import apply_style  # type: ignore


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(
        self, app_settings, opengl_enviroment_setting, theme_setting, app_info
    ):
        super().__init__()
        self.settings_ = app_settings
        self.opengl_enviroment_setting = opengl_enviroment_setting
        self.theme_setting = theme_setting
        self.name = app_info[0]
        self.display_name = app_info[1]
        self.version = app_info[2]
        self.author = app_info[3]
        self.website = app_info[4]
        self.current_dir = app_info[5]
        self.home_dir = app_info[6]

        self.title = ""
        self.artist = ""
        self.artwork = ""
        self.video_id = ""
        self.duration = 0
        self.current_time = "0:00"
        self.total_time = "0:00"
        self.song_state = "NoSong"
        self.song_status = "Indifferent"
        self.icon_folder = f"{self.current_dir}/resources/icons"
        self.force_exit = False
        self.is_downloading = False
        self.current_url = None
        self.picture_in_picture_dialog = None
        self.download_thread = None
        self.update_checker_thread = None
        self.hotkey_controller_thread = None
        self.music_recognizer_thread = None
        self.downloading_state_tool_tip = None
        self.recognizing_state_tool_tip = None
        self.discord_rpc = None
        self.win_thumbnail_toolbar = None

        self.load_settings()
        self.configure_window()
        self.connect_signals()
        self.connect_shortcuts()
        self.show_splash_screen()
        self.setup_web_engine()

        if platform.system() == "Windows":
            self.ffmpeg_url = (
                "https://github.com/deeffest/pytubefix/"
                "releases/download/v8.12.3/FFmpeg-Win32.exe"
            )
            self.deno_url = (
                "https://github.com/deeffest/pytubefix/"
                "releases/download/v8.12.3/Deno-Win32.exe"
            )
            self.ytdlp_url = (
                "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
            )
            self.ffmpeg_path = os.path.join(self.home_dir, "bin", "ffmpeg.exe")
            self.deno_path = os.path.join(self.home_dir, "bin", "deno.exe")
            self.ytdlp_path = os.path.join(self.home_dir, "bin", "yt-dlp.exe")
        else:
            self.ffmpeg_url = (
                "https://github.com/deeffest/pytubefix/"
                "releases/download/v8.12.3/FFmpeg-Linux"
            )
            self.deno_url = (
                "https://github.com/deeffest/pytubefix/"
                "releases/download/v8.12.3/Deno-Linux"
            )
            self.ytdlp_url = (
                "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_linux"
            )
            self.ffmpeg_path = os.path.join(self.home_dir, "bin", "ffmpeg")
            self.deno_path = os.path.join(self.home_dir, "bin", "deno")
            self.ytdlp_path = os.path.join(self.home_dir, "bin", "yt-dlp_linux")

        self.cache_dir = os.path.join(self.home_dir, "__cache__")
        os.makedirs(self.cache_dir, exist_ok=True)

        self.create_actions()
        self.create_submenus()
        self.create_context_menus()
        self.configure_ui_elements()
        self.activate_plugins()
        self.activate_custom_plugins()
        self.connect_actions()
        self.run_discord_rpc()
        self.show_system_tray_icon()
        self.start_playback_control()
        self.create_win_thumbnail_toolbar()

    def load_settings(self):
        if self.settings_.value("ad_blocker") is None:
            self.settings_.setValue("ad_blocker", 1)
        if self.settings_.value("save_last_win_geometry") is None:
            self.settings_.setValue("save_last_win_geometry", 1)
        if self.settings_.value("open_last_url_at_startup") is None:
            self.settings_.setValue("open_last_url_at_startup", 1)
        if self.settings_.value("last_url") is None:
            self.settings_.setValue("last_url", "https://music.youtube.com/")
        if self.settings_.value("fullscreen_mode_support") is None:
            self.settings_.setValue("fullscreen_mode_support", 1)
        if self.settings_.value("support_animated_scrolling") is None:
            self.settings_.setValue("support_animated_scrolling", 0)
        if self.settings_.value("save_last_pos_of_mp") is None:
            self.settings_.setValue("save_last_pos_of_mp", 0)
        if self.settings_.value("last_win_geometry") is None:
            self.settings_.setValue(
                "last_win_geometry", QRect(get_centered_geometry(1000, 799))
            )
        if self.settings_.value("save_last_zoom_factor") is None:
            self.settings_.setValue("save_last_zoom_factor", 1)
        if self.settings_.value("last_zoom_factor") is None:
            self.settings_.setValue("last_zoom_factor", 1.0)
        if self.settings_.value("last_download_folder") is None:
            self.settings_.setValue("last_download_folder", os.path.expanduser("~"))
        if self.settings_.value("discord_rpc") is None:
            self.settings_.setValue("discord_rpc", 0)
        if self.settings_.value("geometry_of_mp") is None:
            self.settings_.setValue(
                "geometry_of_mp", QRect(get_centered_geometry(360, 150))
            )
        if self.settings_.value("tray_icon") is None:
            self.settings_.setValue(
                "tray_icon", 1 if QSystemTrayIcon.isSystemTrayAvailable() else 0
            )
        if self.settings_.value("hotkey_playback_control") is None:
            self.settings_.setValue("hotkey_playback_control", 0)
        if self.settings_.value("only_audio_mode") is None:
            self.settings_.setValue("only_audio_mode", 0)
        if self.settings_.value("nonstop_music") is None:
            self.settings_.setValue("nonstop_music", 1)
        if self.settings_.value("hide_toolbar") is None:
            self.settings_.setValue("hide_toolbar", 0)
        if self.settings_.value("use_hd_thumbnails") is None:
            self.settings_.setValue("use_hd_thumbnails", 0)
        if self.settings_.value("hide_mini_player") is None:
            self.settings_.setValue("hide_mini_player", 0)
        if self.settings_.value("use_cookies") is None:
            self.settings_.setValue("use_cookies", "false")
        if self.settings_.value("auto_update_ytdlp") is None:
            self.settings_.setValue("auto_update_ytdlp", "true")
        if self.settings_.value("maximized_state_setting") is None:
            self.settings_.setValue("maximized_state_setting", 0)
        if self.settings_.value("im_not_a_kid") is None:
            self.settings_.setValue("im_not_a_kid", 1)
        if self.settings_.value("icon_color") is None:
            self.settings_.setValue("icon_color", 0)
        if self.settings_.value("win_thumbnail_buttons") is None:
            self.settings_.setValue(
                "win_thumbnail_buttons", 1 if platform.system() == "Windows" else 0
            )
        if self.settings_.value("pip_is_always_on_top") is None:
            self.settings_.setValue("pip_is_always_on_top", 1)
        if self.settings_.value("do_not_save_cookies") is None:
            self.settings_.setValue("do_not_save_cookies", 0)
        if self.settings_.value("pip_opacity") is None:
            self.settings_.setValue("pip_opacity", 1.0)
        if self.settings_.value("embed_metadata") is None:
            self.settings_.setValue("embed_metadata", 1)
        if self.settings_.value("ytdlp_format") is None:
            self.settings_.setValue("ytdlp_format", 1)
        if self.settings_.value("audd_api_token") is None:
            self.settings_.setValue("audd_api_token", "")
        if self.settings_.value("audd_recording_lenght") is None:
            self.settings_.setValue("audd_recording_lenght", 5)
        if self.settings_.value("prefer_system_ffmpeg") is None:
            self.settings_.setValue("prefer_system_ffmpeg", 0)
        if self.settings_.value("prefer_system_deno") is None:
            self.settings_.setValue("prefer_system_deno", 0)

        self.ad_blocker_setting = int(self.settings_.value("ad_blocker"))
        self.save_last_win_geometry_setting = int(
            self.settings_.value("save_last_win_geometry")
        )
        self.open_last_url_at_startup_setting = int(
            self.settings_.value("open_last_url_at_startup")
        )
        self.last_url_setting = self.settings_.value("last_url")
        self.fullscreen_mode_support_setting = int(
            self.settings_.value("fullscreen_mode_support")
        )
        self.support_animated_scrolling_setting = int(
            self.settings_.value("support_animated_scrolling")
        )
        self.save_last_pos_of_mp_setting = int(
            self.settings_.value("save_last_pos_of_mp")
        )
        self.last_win_geometry_setting = self.settings_.value("last_win_geometry")
        self.save_last_zoom_factor_setting = int(
            self.settings_.value("save_last_zoom_factor")
        )
        self.last_zoom_factor_setting = float(self.settings_.value("last_zoom_factor"))
        self.last_download_folder_setting = self.settings_.value("last_download_folder")
        self.discord_rpc_setting = int(self.settings_.value("discord_rpc"))
        self.geometry_of_mp_setting = self.settings_.value("geometry_of_mp")
        self.tray_icon_setting = (
            int(self.settings_.value("tray_icon"))
            if QSystemTrayIcon.isSystemTrayAvailable()
            else 0
        )
        self.hotkey_playback_control_setting = int(
            self.settings_.value("hotkey_playback_control")
        )
        self.only_audio_mode_setting = int(self.settings_.value("only_audio_mode"))
        self.nonstop_music_setting = int(self.settings_.value("nonstop_music"))
        self.hide_toolbar_setting = int(self.settings_.value("hide_toolbar"))
        self.use_hd_thumbnails_setting = int(self.settings_.value("use_hd_thumbnails"))
        self.hide_mini_player_setting = int(self.settings_.value("hide_mini_player"))
        self.use_cookies_setting = str_to_bool(self.settings_.value("use_cookies"))
        self.auto_update_ytdlp_setting = str_to_bool(
            self.settings_.value("auto_update_ytdlp")
        )
        self.maximized_state_setting = int(
            self.settings_.value("maximized_state_setting")
        )
        self.im_not_a_kid_setting = int(self.settings_.value("im_not_a_kid"))
        self.icon_color_setting = int(self.settings_.value("icon_color"))
        self.win_thumbnail_buttons_setting = (
            int(self.settings_.value("win_thumbnail_buttons"))
            if platform.system() == "Windows"
            else 0
        )
        self.pip_is_always_on_top_setting = int(
            self.settings_.value("pip_is_always_on_top")
        )
        self.do_not_save_cookies_setting = int(
            self.settings_.value("do_not_save_cookies")
        )
        self.pip_opacity_setting = float(self.settings_.value("pip_opacity"))
        self.embed_metadata_setting = int(self.settings_.value("embed_metadata"))
        self.ytdlp_format_setting = int(self.settings_.value("ytdlp_format"))
        self.audd_api_token_setting = self.settings_.value("audd_api_token")
        self.audd_recording_lenght_setting = int(
            self.settings_.value("audd_recording_lenght")
        )
        self.prefer_system_ffmpeg_setting = int(
            self.settings_.value("prefer_system_ffmpeg")
        )
        self.prefer_system_deno_setting = int(
            self.settings_.value("prefer_system_deno")
        )

    def configure_window(self):
        theme = self.theme_setting
        if theme == 0:
            color = "dark"
            setTheme(Theme.DARK)
        else:
            color = "light"
            setTheme(Theme.LIGHT)
        setThemeColor("red")

        if platform.system() == "Windows":
            try:
                apply_style(self, color)
            except Exception as e:
                logging.error(f"Failed to apply dark style: + {str(e)}")

        self.setupUi(self)
        self.setWindowIcon(QIcon(f"{self.icon_folder}/icon.ico"))
        if self.save_last_win_geometry_setting == 1:
            self.setGeometry(self.last_win_geometry_setting)
            if self.maximized_state_setting == 1:
                self.showMaximized()
        else:
            self.setGeometry(get_centered_geometry(1000, 799))

    def connect_signals(self):
        signal_bus.show_window_sig.connect(self.show_window_or_picture_in_picture)
        signal_bus.app_error_sig.connect(self.show_error_message)

    def show_error_message(self, msg, title=None):
        text_view_dialog = TextViewMessageBox(
            f"{title}" if title else "Unexpected error", msg, self
        )
        text_view_dialog.cancelButton.hide()
        text_view_dialog.exec_()

    def connect_shortcuts(self):
        self.back_shortcut = QShortcut(QKeySequence(Qt.ALT + Qt.Key_Left), self)
        self.back_shortcut.activated.connect(self.back)

        self.forward_shortcut = QShortcut(QKeySequence(Qt.ALT + Qt.Key_Right), self)
        self.forward_shortcut.activated.connect(self.forward)

        self.home_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_H), self)
        self.home_shortcut.activated.connect(self.home)

        self.reload_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_R), self)
        self.reload_shortcut.activated.connect(self.reload)

        self.stop_shortcut = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.stop_shortcut.setEnabled(False)
        self.stop_shortcut.activated.connect(self.stop)

        self.go_to_youtube_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Y), self)
        self.go_to_youtube_shortcut.setEnabled(False)
        self.go_to_youtube_shortcut.activated.connect(self.go_to_youtube)

        self.musicbrainz_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_B), self)
        self.musicbrainz_shortcut.setEnabled(False)
        self.musicbrainz_shortcut.activated.connect(
            lambda: self.search_on("MusicBrainz")
        )

        self.download_song_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_D), self)
        self.download_song_shortcut.setEnabled(False)
        self.download_song_shortcut.activated.connect(self.download_song)

        self.download_album_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_P), self)
        self.download_album_shortcut.setEnabled(False)
        self.download_album_shortcut.activated.connect(self.download_album)

        self.watch_in_pip_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_M), self)
        self.watch_in_pip_shortcut.setEnabled(False)
        self.watch_in_pip_shortcut.activated.connect(self.watch_in_pip)

        self.audd_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_U), self)
        self.audd_shortcut.activated.connect(lambda: self.recognize_music("AudD"))

        self.settings_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_S), self)
        self.settings_shortcut.activated.connect(self.open_settings)

        self.hide_toolbar_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_T), self)
        self.hide_toolbar_shortcut.activated.connect(self.hide_toolbar)

        self.restart_app_shortcut = QShortcut(
            QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_R), self
        )
        self.restart_app_shortcut.activated.connect(self.restart_app)

    def show_splash_screen(self):
        self.splash_screen = SplashScreen(self.windowIcon(), self, enableTitleBar=False)
        self.splash_screen.setIconSize(QSize(102, 102))

    def setup_web_engine(self):
        if self.do_not_save_cookies_setting:
            self.webprofile = QWebEngineProfile(self)
        else:
            self.webprofile = QWebEngineProfile.defaultProfile()

        self.webchannel_backend = WebChannelBackend(self)
        self.webchannel = QWebChannel()
        self.webchannel.registerObject("backend", self.webchannel_backend)

        self.webpage = WebEnginePage(self.webprofile, self)
        self.webpage.setWebChannel(self.webchannel)
        self.webpage.fullScreenRequested.connect(self.on_fullscreen_requested)

        self.websettings = QWebEngineSettings.globalSettings()
        self.websettings.setAttribute(
            QWebEngineSettings.FullScreenSupportEnabled,
            self.fullscreen_mode_support_setting,
        )
        self.websettings.setAttribute(
            QWebEngineSettings.ScrollAnimatorEnabled,
            self.support_animated_scrolling_setting,
        )

        self.webview = WebEngineView(self)
        self.webview.setPage(self.webpage)
        self.webview.urlChanged.connect(self.on_url_changed)
        self.webview.loadProgress.connect(self.on_load_progress)
        self.webview.loadStarted.connect(self.on_load_started)
        if self.open_last_url_at_startup_setting == 1 and is_valid_ytmusic_url(
            self.last_url_setting
        ):
            self.webview.load(QUrl(self.last_url_setting))
        else:
            self.home()
        if self.save_last_zoom_factor_setting == 1:
            self.webview.setZoomFactor(self.last_zoom_factor_setting)

    def create_actions(self):
        self.exit_full_screen_action = Action("Exit full screen", shortcut="Esc")
        self.exit_full_screen_action.setIcon(
            recolor_icon(f"{self.icon_folder}/exit_full_screen.png", self.theme_setting)
        )
        self.exit_full_screen_action.triggered.connect(self.exit_full_screen)

        self.back_action = Action("Back", shortcut="Alt+Left")
        self.back_action.setIcon(
            recolor_icon(f"{self.icon_folder}/left.png", self.theme_setting)
        )
        self.back_action.setEnabled(False)
        self.back_action.triggered.connect(self.back)

        self.forward_action = Action("Forward", shortcut="Alt+Right")
        self.forward_action.setIcon(
            recolor_icon(f"{self.icon_folder}/right.png", self.theme_setting)
        )
        self.forward_action.setEnabled(False)
        self.forward_action.triggered.connect(self.forward)

        self.home_action = Action("Home", shortcut="Ctrl+H")
        self.home_action.setIcon(
            recolor_icon(f"{self.icon_folder}/home.png", self.theme_setting)
        )
        self.home_action.triggered.connect(self.home)

        self.reload_action = Action("Reload", shortcut="Ctrl+R")
        self.reload_action.setIcon(
            recolor_icon(f"{self.icon_folder}/reload.png", self.theme_setting)
        )
        self.reload_action.triggered.connect(self.reload)

        self.go_to_youtube_action = MultiAction()

        self.musicbrainz_action = MultiAction()

        self.download_song_action = Action("Song", shortcut="Ctrl+D")
        self.download_song_action.setIcon(
            recolor_icon(f"{self.icon_folder}/song.png", self.theme_setting)
        )
        self.download_song_action.setEnabled(False)
        self.download_song_action.triggered.connect(self.download_song)

        self.download_album_action = Action("Album", shortcut="Ctrl+P")
        self.download_album_action.setIcon(
            recolor_icon(f"{self.icon_folder}/album.png", self.theme_setting)
        )
        self.download_album_action.setEnabled(False)
        self.download_album_action.triggered.connect(self.download_album)

        self.watch_in_pip_action = Action("Watch in PiP", shortcut="Ctrl+M")
        self.watch_in_pip_action.setIcon(
            recolor_icon(
                f"{self.icon_folder}/picture_in_picture.png", self.theme_setting
            )
        )
        self.watch_in_pip_action.setEnabled(False)
        self.watch_in_pip_action.triggered.connect(self.watch_in_pip)

        self.audd_action = MultiAction()

        self.restart_app_action = Action("Restart app", shortcut="Ctrl+Shift+R")
        self.restart_app_action.setIcon(
            recolor_icon(f"{self.icon_folder}/restart.png", self.theme_setting)
        )
        self.restart_app_action.triggered.connect(self.restart_app)

        self.settings_action = Action("Settings...", shortcut="Ctrl+S")
        self.settings_action.setIcon(
            recolor_icon(f"{self.icon_folder}/settings.png", self.theme_setting)
        )
        self.settings_action.triggered.connect(self.open_settings)

        self.bug_report_action = Action("Bug report")
        self.bug_report_action.setIcon(
            recolor_icon(f"{self.icon_folder}/bug.png", self.theme_setting)
        )
        self.bug_report_action.triggered.connect(self.bug_report)

        self.visit_github_action = QAction("Visit GitHub", self)
        self.visit_github_action.setIcon(QIcon(f"{self.icon_folder}/github.png"))
        self.visit_github_action.triggered.connect(self.visit_github)

        self.icons_by_icons8_action = QAction("Icons by Icons8", self)
        self.icons_by_icons8_action.setIcon(QIcon(f"{self.icon_folder}/icons8.png"))
        self.icons_by_icons8_action.triggered.connect(self.icons_by_icons8)

        self.by_deeffest_action = QAction("by deeffest, 2024-2026", self)
        self.by_deeffest_action.setIcon(QIcon(f"{self.icon_folder}/deeffest.png"))
        self.by_deeffest_action.triggered.connect(self.by_deeffest)

        self.hide_toolbar_action = MultiAction()

        self.cut_action = Action("Cut", shortcut="Ctrl+X")
        self.cut_action.setIcon(
            recolor_icon(f"{self.icon_folder}/cut.png", self.theme_setting)
        )
        self.cut_action.triggered.connect(self.cut)

        self.copy_action = Action("Copy", shortcut="Ctrl+C")
        self.copy_action.setIcon(
            recolor_icon(f"{self.icon_folder}/copy.png", self.theme_setting)
        )
        self.copy_action.triggered.connect(self.copy)

        self.paste_action = Action("Paste", shortcut="Ctrl+V")
        self.paste_action.setIcon(
            recolor_icon(f"{self.icon_folder}/paste.png", self.theme_setting)
        )
        self.paste_action.triggered.connect(self.paste)

        self.copy_url_action = Action("Copy URL")
        self.copy_url_action.setIcon(
            recolor_icon(f"{self.icon_folder}/url.png", self.theme_setting)
        )
        self.copy_url_action.triggered.connect(self.copy_current_url)

        self.copy_clean_url_action = Action("Copy clean URL")
        self.copy_clean_url_action.triggered.connect(self.copy_current_clean_url)

        self.skip_video_ads_action = Action("Skip video ads")
        self.skip_video_ads_action.setIcon(QIcon(f"{self.icon_folder}/adblock.png"))
        self.skip_video_ads_action.setCheckable(True)
        self.skip_video_ads_action.setChecked(bool(self.ad_blocker_setting))

        self.audio_only_mode_action = Action("Audio-only mode")
        self.audio_only_mode_action.setIcon(QIcon(f"{self.icon_folder}/audio_only.png"))
        self.audio_only_mode_action.setCheckable(True)
        self.audio_only_mode_action.setChecked(bool(self.only_audio_mode_setting))

        self.nonstop_music_action = Action("Non-stop music")
        self.nonstop_music_action.setIcon(
            QIcon(f"{self.icon_folder}/nonstop_music.png")
        )
        self.nonstop_music_action.setCheckable(True)
        self.nonstop_music_action.setChecked(bool(self.nonstop_music_setting))

        self.hide_mini_player_action = Action("Hide mini player")
        self.hide_mini_player_action.setIcon(
            QIcon(f"{self.icon_folder}/hide_mini_player.png")
        )
        self.hide_mini_player_action.setCheckable(True)
        self.hide_mini_player_action.setChecked(bool(self.hide_mini_player_setting))

        self.im_not_a_kid_action = Action("I'm not a kid!", self)
        self.im_not_a_kid_action.setIcon(QIcon(f"{self.icon_folder}/im_not_a_kid.png"))
        self.im_not_a_kid_action.setCheckable(True)
        self.im_not_a_kid_action.setChecked(bool(self.im_not_a_kid_setting))

    def create_submenus(self):
        self.search_on_menu = self.create_search_on_menu()

        self.download_menu = RoundMenu("Download")
        self.download_menu.setIcon(
            recolor_icon(f"{self.icon_folder}/download.png", self.theme_setting)
        )
        self.download_menu.addAction(self.download_song_action)
        self.download_menu.addAction(self.download_album_action)

        self.recognize_music_menu = self.create_recognize_music_menu()

        self.plugins_menu = CheckableMenu("Plugins")
        self.plugins_menu.setIcon(
            recolor_icon(f"{self.icon_folder}/plugins.png", self.theme_setting)
        )
        self.plugins_menu.addAction(self.skip_video_ads_action)
        self.plugins_menu.addAction(self.audio_only_mode_action)
        self.plugins_menu.addAction(self.nonstop_music_action)
        self.plugins_menu.addAction(self.hide_mini_player_action)
        self.plugins_menu.addAction(self.im_not_a_kid_action)

        self.about_menu = self.create_about_menu()

    def create_context_menus(self):
        self.main_menu = RoundMenu()
        self.main_menu.addAction(self.exit_full_screen_action)
        self.main_menu.setActionVisible(self.exit_full_screen_action, False)
        self.main_menu.addSeparator()
        self.main_menu.addAction(self.back_action)
        self.main_menu.addAction(self.forward_action)
        self.main_menu.addAction(self.home_action)
        self.main_menu.addAction(self.reload_action)
        self.main_menu.addSeparator()
        self.go_to_youtube_action.add(
            self.main_menu, self.create_go_to_youtube_action()
        )
        self.main_menu.addMenu(self.search_on_menu)
        self.main_menu.addSeparator()
        self.main_menu.addMenu(self.download_menu)
        self.main_menu.addAction(self.watch_in_pip_action)
        self.main_menu.addMenu(self.recognize_music_menu)
        self.main_menu.addAction(self.restart_app_action)
        self.main_menu.addSeparator()
        self.main_menu.addAction(self.settings_action)
        self.main_menu.addMenu(self.plugins_menu)
        self.main_menu.addSeparator()
        self.main_menu.addAction(self.bug_report_action)
        self.main_menu.addMenu(self.about_menu)
        self.main_menu.addSeparator()
        self.hide_toolbar_action.add(self.main_menu, self.create_hide_toolbar_action())

        self.more_menu = RoundMenu()
        self.go_to_youtube_action.add(
            self.more_menu, self.create_go_to_youtube_action()
        )
        self.more_menu.addMenu(self.create_search_on_menu())
        self.more_menu.addSeparator()
        self.more_menu.addMenu(self.create_recognize_music_menu())
        self.more_menu.addAction(self.restart_app_action)
        self.more_menu.addSeparator()
        self.more_menu.addAction(self.bug_report_action)
        self.more_menu.addMenu(self.create_about_menu())
        self.more_menu.addSeparator()
        self.hide_toolbar_action.add(self.more_menu, self.create_hide_toolbar_action())

        self.edit_menu = RoundMenu()
        self.edit_menu.addAction(self.cut_action)
        self.edit_menu.addAction(self.copy_action)
        self.edit_menu.addAction(self.paste_action)

        self.copy_menu = RoundMenu()
        self.copy_menu.addAction(self.copy_action)

        self.paste_menu = RoundMenu()
        self.paste_menu.addAction(self.paste_action)

        self.url_menu = RoundMenu()
        self.url_menu.addAction(self.copy_url_action)
        self.url_menu.addAction(self.copy_clean_url_action)

    def configure_ui_elements(self):
        self.back_tbutton.setIcon(
            recolor_icon(f"{self.icon_folder}/left.png", self.theme_setting)
        )
        self.back_tbutton.setEnabled(False)
        self.back_tbutton.clicked.connect(self.back)

        self.forward_tbutton.setIcon(
            recolor_icon(f"{self.icon_folder}/right.png", self.theme_setting)
        )
        self.forward_tbutton.setEnabled(False)
        self.forward_tbutton.clicked.connect(self.forward)

        self.home_tbutton.setIcon(
            recolor_icon(f"{self.icon_folder}/home.png", self.theme_setting)
        )
        self.home_tbutton.clicked.connect(self.home)

        self.reload_tbutton.setIcon(
            recolor_icon(f"{self.icon_folder}/reload.png", self.theme_setting)
        )
        self.reload_tbutton.clicked.connect(self.reload)

        if self.theme_setting == 1:
            self.url_label.setStyleSheet(
                """
                QLabel {
                    color: rgb(30, 30, 30);
                    background-color: rgb(234, 234, 234);
                    border: 1px solid transparent;
                    border-radius: 6px;
                    padding: 3px 6px;
                }
                QLabel:hover {
                    border: 1px solid rgb(255, 0, 0);
                }
                """
            )
        self.update_url_label(self.current_url)
        self.url_label.customContextMenuRequested.disconnect()
        self.url_label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.url_label.customContextMenuRequested.connect(
            lambda pos: self.show_url_menu(pos)
        )

        self.download_ddtbutton.setIcon(
            recolor_icon(f"{self.icon_folder}/download.png", self.theme_setting)
        )
        self.download_ddtbutton.setMenu(self.download_menu)

        self.plugins_ddtbutton.setIcon(
            recolor_icon(f"{self.icon_folder}/plugins.png", self.theme_setting)
        )
        self.plugins_ddtbutton.setMenu(self.plugins_menu)

        self.watch_in_pip_tbutton.setIcon(
            recolor_icon(
                f"{self.icon_folder}/picture_in_picture.png", self.theme_setting
            )
        )
        self.watch_in_pip_tbutton.setEnabled(False)
        self.watch_in_pip_tbutton.clicked.connect(self.watch_in_pip)

        self.settings_ddtbutton.setIcon(
            recolor_icon(f"{self.icon_folder}/settings.png", self.theme_setting)
        )
        self.settings_ddtbutton.clicked.connect(self.open_settings)

        self.more_ddtbutton.setIcon(
            recolor_icon(f"{self.icon_folder}/more.png", self.theme_setting)
        )
        self.more_ddtbutton.setMenu(self.more_menu)

        self.back_tbutton.installEventFilter(
            ToolTipFilter(self.back_tbutton, 300, ToolTipPosition.TOP)
        )
        self.forward_tbutton.installEventFilter(
            ToolTipFilter(self.forward_tbutton, 300, ToolTipPosition.TOP)
        )
        self.home_tbutton.installEventFilter(
            ToolTipFilter(self.home_tbutton, 300, ToolTipPosition.TOP)
        )
        self.reload_tbutton.installEventFilter(
            ToolTipFilter(self.reload_tbutton, 300, ToolTipPosition.TOP)
        )
        self.download_ddtbutton.installEventFilter(
            ToolTipFilter(self.download_ddtbutton, 300, ToolTipPosition.TOP)
        )
        self.watch_in_pip_tbutton.installEventFilter(
            ToolTipFilter(self.watch_in_pip_tbutton, 300, ToolTipPosition.TOP)
        )
        self.settings_ddtbutton.installEventFilter(
            ToolTipFilter(self.settings_ddtbutton, 300, ToolTipPosition.TOP)
        )
        self.plugins_ddtbutton.installEventFilter(
            ToolTipFilter(self.plugins_ddtbutton, 300, ToolTipPosition.TOP)
        )
        self.more_ddtbutton.installEventFilter(
            ToolTipFilter(self.more_ddtbutton, 300, ToolTipPosition.TOP)
        )

        self.ToolBar.installEventFilter(self)
        if self.hide_toolbar_setting == 1:
            QTimer.singleShot(0, lambda: self.ToolBar.hide())

        self.MainLayout.addWidget(self.webview)

    def delete_all_cookies(self):
        cookie_store = self.webprofile.cookieStore()
        cookie_store.deleteAllCookies()

    def open_settings(self):
        self.settings_dialog = SettingsDialog(self)
        self.settings_dialog.exec()

    def restart_app(self):
        msg_box = None

        if self.song_state == "Playing":
            msg_box = MessageBox(
                "Restart confirmation",
                (
                    "Restarting now will stop the current playback and "
                    "close the application.\n"
                    "Do you want to restart now?"
                ),
                self,
            )
            msg_box.yesButton.setText("Restart")
        if not msg_box or msg_box.exec_():
            self.save_settings()

            QProcess.startDetached(sys.executable, sys.argv)
            QApplication.quit()

    def remove_tool_from_device(self, tool):
        try:
            if tool == "yt-dlp":
                os.remove(self.ytdlp_path)
                os.remove(self.cookies_txt)
            elif tool == "FFmpeg":
                os.remove(self.ffmpeg_path)
            elif tool == "Deno":
                os.remove(self.deno_path)
        except Exception as e:
            logging.error(f"Failed to remove {tool} from device: {e}")

    def check_tool_availability(self, tool):
        if tool == "yt-dlp":
            return os.path.isfile(self.ytdlp_path)
        elif tool == "FFmpeg":
            return os.path.isfile(self.ffmpeg_path)
        elif tool == "Deno":
            return os.path.isfile(self.deno_path)

    def copy_current_url(self):
        copy_text(self.current_url)

    def copy_current_clean_url(self):
        copy_text(clean_up_url(self.current_url))

    def show_url_menu(self, pos):
        def reset_hover():
            self.url_label.setAttribute(Qt.WA_UnderMouse, False)
            self.url_label.style().unpolish(self.url_label)
            self.url_label.style().polish(self.url_label)
            self.url_label.update()

        self.url_menu.exec(self.url_label.mapToGlobal(pos))
        QTimer.singleShot(0, reset_hover)

    def create_hide_toolbar_action(self):
        action = Action("Hide toolbar", shortcut="Ctrl+T")
        action.setIcon(
            recolor_icon(f"{self.icon_folder}/hide_toolbar.png", self.theme_setting)
        )
        action.triggered.connect(self.hide_toolbar)
        return action

    def create_audd_action(self):
        action = Action("AudD API", shortcut="Ctrl+U")
        action.setIcon(QIcon(f"{self.icon_folder}/audd.png"))
        action.triggered.connect(lambda: self.recognize_music("AudD"))
        return action

    def create_musicbrainz_action(self):
        action = Action("MusicBrainz", shortcut="Ctrl+B")
        action.setIcon(QIcon(f"{self.icon_folder}/musicbrainz.png"))
        action.setEnabled(False)
        action.triggered.connect(lambda: self.search_on("MusicBrainz"))
        return action

    def create_go_to_youtube_action(self):
        action = Action("Go to YouTube", shortcut="Ctrl+Y")
        action.setIcon(recolor_icon(f"{self.icon_folder}/open.png", self.theme_setting))
        action.setEnabled(False)
        action.triggered.connect(self.go_to_youtube)
        return action

    def create_search_on_menu(self):
        menu = RoundMenu("Search on")
        menu.setIcon(recolor_icon(f"{self.icon_folder}/search.png", self.theme_setting))

        self.musicbrainz_action.add(menu, self.create_musicbrainz_action())
        return menu

    def create_recognize_music_menu(self):
        menu = RoundMenu("Recognize music", self)
        menu.setIcon(
            recolor_icon(f"{self.icon_folder}/recognize_music.png", self.theme_setting)
        )
        self.audd_action.add(menu, self.create_audd_action())
        return menu

    def create_about_menu(self):
        menu = RoundMenu("About")
        menu.setIcon(recolor_icon(f"{self.icon_folder}/about.png", self.theme_setting))

        card = AboutCard(
            f"{self.icon_folder}/logo.png",
            self.display_name,
            f"Version: {self.version}",
            self,
        )
        card.setFixedSize(card.sizeHint())

        menu.addWidget(card, selectable=False)
        menu.addSeparator()
        menu.addAction(self.visit_github_action)
        menu.addAction(self.icons_by_icons8_action)
        menu.addAction(self.by_deeffest_action)
        return menu

    def recognize_music(self, service):
        self.audd_action.setEnabled(False)
        self.audd_shortcut.setEnabled(False)

        self.webpage.runJavaScript("document.querySelector('video').pause()")

        self.music_recognizer_thread = MusicRecognizerThread(service, self)
        self.music_recognizer_thread.recording_audio_from_pc.connect(
            self.on_recording_audio_from_pc
        )
        self.music_recognizer_thread.recording_audio_from_pc_success.connect(
            self.on_recording_audio_from_pc_success
        )
        self.music_recognizer_thread.recognizing_via_audd_api.connect(
            self.on_recognizing_via_audd_api
        )
        self.music_recognizer_thread.recognizing_via_audd_api_success.connect(
            self.on_recognizing_via_audd_api_success
        )
        self.music_recognizer_thread.recognizing_via_audd_api_error.connect(
            self.on_recognizing_via_audd_api_error
        )
        self.music_recognizer_thread.finished.connect(self.on_recognizing_finish)
        self.music_recognizer_thread.start()

    def show_recognizing_state_tooltip(self, title, content):
        def calculate_tooltip_pos(
            parent_widget,
            tooltip_widget,
            margin=20,
            top_offset=63 if self.hide_toolbar_setting == 0 else 20,
        ):
            parent_width = parent_widget.width()
            parent_height = parent_widget.height()

            tooltip_width = tooltip_widget.width()
            tooltip_height = tooltip_widget.height()

            x = parent_width - tooltip_width - margin
            y = top_offset

            if x < 0:
                x = 0
            if y < 0:
                y = 0
            if x + tooltip_width > parent_width:
                x = parent_width - tooltip_width
            if y + tooltip_height > parent_height:
                y = parent_height - tooltip_height

            return QPoint(x, y)

        self.recognizing_state_tool_tip = StateToolTip(title, content, self)
        pos = calculate_tooltip_pos(self, self.recognizing_state_tool_tip)
        self.recognizing_state_tool_tip.move(pos)
        self.recognizing_state_tool_tip.show()

    def hide_recognizing_state_tooltip(self):
        if self.recognizing_state_tool_tip is not None:
            self.recognizing_state_tool_tip.setState(True)
            self.recognizing_state_tool_tip = None

    def on_recording_audio_from_pc(self):
        self.show_recognizing_state_tooltip("Recording audio from PC", "Please wait...")

    def on_recording_audio_from_pc_success(self):
        self.hide_recognizing_state_tooltip()

    def on_recognizing_via_audd_api(self):
        self.show_recognizing_state_tooltip(
            "Recognizing via AudD API", "Please wait..."
        )

    def on_recognizing_via_audd_api_error(self, code, msg):
        self.hide_recognizing_state_tooltip()

        info_bar = InfoBar.error(
            title=f"Error code: {code}",
            content="Recognize music failed!",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM,
            duration=-1,
            parent=self,
        )

        button = PushButton(
            recolor_icon(f"{self.icon_folder}/show.png", self.theme_setting),
            "Show error",
            self,
        )
        button.clicked.connect(lambda: self.show_recognize_error(msg, info_bar))
        info_bar.addWidget(button)

    def on_recognizing_via_audd_api_success(self, author, title):
        self.hide_downloading_state_tooltip()

        info_bar = InfoBar.success(
            title=f"{author} - {title}",
            content="Recognize music successfully!",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM,
            duration=-1,
            parent=self,
        )

        button = PushButton(
            recolor_icon(f"{self.icon_folder}/search.png", self.theme_setting),
            "Search song",
            self,
        )
        button.clicked.connect(lambda: self.search_song(f"{author} {title}", info_bar))
        info_bar.addWidget(button)

    def show_recognize_error(self, msg, info_bar):
        info_bar.close()

        QTimer.singleShot(0, lambda: self.show_error_message(msg, "AudD API error"))

    def search_song(self, query, info_bar):
        info_bar.close()

        js = f"""
        (function() {{
            const input = document.querySelector('ytmusic-search-box input#input');
            if (!input) return;
            input.focus();
            document.execCommand('selectAll');
            document.execCommand('insertText', false, {json.dumps(query)});
        }})();
        """

        def after_insert(_):
            QTest.keyClick(self.webview.focusProxy(), Qt.Key_Return)

        if is_valid_ytmusic_url(self.current_url):
            self.webpage.runJavaScript(js, after_insert)
        else:
            self.webview.setUrl(QUrl(f"https://music.youtube.com/search?q={query}"))

    def on_recognizing_finish(self):
        self.music_recognizer_thread = None
        self.hide_recognizing_state_tooltip()

        self.audd_action.setEnabled(True)
        self.audd_shortcut.setEnabled(True)

    def activate_plugins(self):
        qtwebchannel = QWebEngineScript()
        file = QFile(":/qtwebchannel/qwebchannel.js")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            qtwebchannel.setSourceCode(stream.readAll())
            file.close()
        qtwebchannel.setInjectionPoint(QWebEngineScript.DocumentReady)
        qtwebchannel.setWorldId(QWebEngineScript.MainWorld)
        qtwebchannel.setRunsOnSubFrames(False)
        self.webpage.profile().scripts().insert(qtwebchannel)

        def insert_script(filename):
            script = QWebEngineScript()
            script.setName(filename)
            script.setSourceCode(self.read_script(filename))
            script.setWorldId(QWebEngineScript.MainWorld)
            script.setRunsOnSubFrames(False)
            self.webpage.profile().scripts().insert(script)

        insert_script("scrollbar_styles.js")
        insert_script("ytmusic_observer.js")
        if self.ad_blocker_setting == 1:
            insert_script("skip_video_ads.js")
        if self.only_audio_mode_setting == 1:
            insert_script("audio_only_mode.js")
            insert_script("block_video.js")
        if self.nonstop_music_setting == 1:
            insert_script("non_stop_music.js")
        if self.hide_mini_player_setting == 1:
            insert_script("hide_mini_player.js")
        if self.im_not_a_kid_setting == 1:
            insert_script("im_not_a_kid.js")

    def activate_custom_plugins(self):
        plugins_dir = os.path.join(self.current_dir, "plugins")

        if not os.path.isdir(plugins_dir):
            return

        js_files = sorted(f for f in os.listdir(plugins_dir) if f.endswith(".js"))
        if not js_files:
            return

        for filename in js_files:
            filepath = os.path.join(plugins_dir, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    source = f.read()
            except Exception as e:
                logging.error(f"Failed to load custom plugin '{filename}': {str(e)}")
                continue

            script = QWebEngineScript()
            script.setName(f"custom_{filename}")
            script.setSourceCode(source)
            script.setWorldId(QWebEngineScript.MainWorld)
            script.setRunsOnSubFrames(False)
            self.webpage.profile().scripts().insert(script)

            action = Action(filename)
            action.setEnabled(False)
            self.plugins_menu.addAction(action)

    def connect_actions(self):
        def toggle_audio_only_mode(enabled):
            toggle_script("audio_only_mode.js", enabled=enabled)
            toggle_script("block_video.js", enabled=enabled)

        def toggle_script(filename, enabled=None):
            scripts = self.webpage.profile().scripts()
            existing = scripts.findScript(filename)
            if not existing.isNull():
                scripts.remove(existing)

            if enabled:
                script = QWebEngineScript()
                script.setName(filename)
                script.setSourceCode(self.read_script(filename))
                script.setWorldId(QWebEngineScript.MainWorld)
                script.setRunsOnSubFrames(False)
                scripts.insert(script)

        self.skip_video_ads_action.toggled.connect(
            lambda checked: toggle_script("skip_video_ads.js", enabled=checked)
        )
        self.audio_only_mode_action.toggled.connect(
            lambda checked: toggle_audio_only_mode(checked)
        )
        self.nonstop_music_action.toggled.connect(
            lambda checked: toggle_script("non_stop_music.js", enabled=checked)
        )
        self.hide_mini_player_action.toggled.connect(
            lambda checked: toggle_script("hide_mini_player.js", enabled=checked)
        )
        self.im_not_a_kid_action.toggled.connect(
            lambda checked: toggle_script("im_not_a_kid.js", enabled=checked)
        )

    def create_win_thumbnail_toolbar(self):
        if platform.system() == "Windows" and self.win_thumbnail_buttons_setting == 1:
            self.win_thumbnail_toolbar = QWinThumbnailToolBar(self)
            self.create_previous_button()
            self.create_play_pause_button()
            self.create_next_button()
            self.win_thumbnail_toolbar.setWindow(self.windowHandle())

    def on_load_progress(self, progress):
        if progress > 70:
            self.reload_tbutton.setToolTip("Reload")
            self.reload_tbutton.setIcon(
                recolor_icon(f"{self.icon_folder}/reload.png", self.theme_setting)
            )
            self.reload_tbutton.clicked.disconnect()
            self.reload_tbutton.clicked.connect(self.reload)

            self.reload_action.setText("Reload")
            self.reload_action.setShortcut("Ctrl+R")
            self.reload_action.setIcon(
                recolor_icon(f"{self.icon_folder}/reload.png", self.theme_setting)
            )
            self.reload_action.triggered.disconnect()
            self.reload_action.triggered.connect(self.reload)

            self.stop_shortcut.setEnabled(False)

            if self.splash_screen is not None:
                self.close_splash_screen()
                self.check_updates()

    def on_load_started(self):
        self.reload_tbutton.setToolTip("Stop")
        self.reload_tbutton.setIcon(
            recolor_icon(f"{self.icon_folder}/close.png", self.theme_setting)
        )
        self.reload_tbutton.clicked.disconnect()
        self.reload_tbutton.clicked.connect(self.stop)

        self.reload_action.setText("Stop")
        self.reload_action.setShortcut("Esc")
        self.reload_action.setIcon(
            recolor_icon(f"{self.icon_folder}/close.png", self.theme_setting)
        )
        self.reload_action.triggered.disconnect()
        self.reload_action.triggered.connect(self.stop)

        self.stop_shortcut.setEnabled(True)

    def close_splash_screen(self):
        self.splash_screen.deleteLater()
        self.splash_screen = None

    def check_updates(self):
        self.update_checker_thread = UpdateChecker(self)
        self.update_checker_thread.update_checked.connect(self.on_update_checked)
        self.update_checker_thread.start()

    def on_update_checked(self, last_version, title, whats_new, last_release_url):
        self.update_checker_thread = None

        if pkg_version.parse(self.version) < pkg_version.parse(last_version):
            msg_box = MessageBox(title, whats_new, self)
            msg_box.yesButton.setText("Download")
            msg_box.cancelButton.setText("Later")
            if msg_box.exec_():
                open_url(last_release_url)
                self.force_exit = True
                self.close()

    def on_fullscreen_requested(self, request):
        if not self.isFullScreen():
            if self.isMaximized():
                self.maximized_state_setting = 1
            else:
                self.maximized_state_setting = 0
                self.last_win_geometry_setting = self.geometry()
                self.settings_.setValue(
                    "last_win_geometry", self.last_win_geometry_setting
                )
            self.ToolBar.hide()
            self.showFullScreen()
            self.main_menu.setActionVisible(self.exit_full_screen_action, True)
        else:
            if self.hide_toolbar_setting == 0:
                self.ToolBar.show()
            if self.maximized_state_setting == 1:
                self.maximized_state_setting = 0
                self.showMaximized()
            else:
                self.showNormal()
            self.main_menu.setActionVisible(self.exit_full_screen_action, False)
        request.accept()

    def exit_full_screen(self):
        self.webpage.triggerAction(QWebEnginePage.WebAction.ExitFullScreen)

    def on_url_changed(self, url):
        self.current_url = url.toString()
        self.update_url_label(self.current_url)

        if is_valid_ytmusic_url(self.current_url):
            self.settings_.setValue("last_url", self.current_url)

        can_go_back = self.webview.history().canGoBack()
        can_go_forward = self.webview.history().canGoForward()
        self.back_action.setEnabled(can_go_back)
        self.back_tbutton.setEnabled(can_go_back)
        self.forward_action.setEnabled(can_go_forward)
        self.forward_tbutton.setEnabled(can_go_forward)

        self.update_download_buttons_state()

    def update_url_label(self, url):
        def lock_svg(locked):
            icon_name = "lock.svg" if locked else "lock2.svg"
            icon_path = f"{self.icon_folder}/{icon_name}"
            with open(icon_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            return (
                f'<img src="data:image/svg+xml;base64,{b64}" '
                'width="16" height="16" style="vertical-align: middle;"/>'
            )

        parsed = urlparse(url)
        lock_img = lock_svg(parsed.scheme == "https")
        host = parsed.hostname or ""

        parts = host.split(".")
        if len(parts) > 2:
            subdomain = ".".join(parts[:-2])
            domain = ".".join(parts[-2:])
        else:
            subdomain = ""
            domain = host

        rest = parsed.path
        if parsed.query:
            rest += "?" + parsed.query
        if parsed.fragment:
            rest += "#" + parsed.fragment

        if self.theme_setting == 0:
            gray = "rgb(130, 130, 130)"
        else:
            gray = "rgb(150, 150, 150)"

        parts_html = [f"{lock_img}&nbsp;&nbsp;"]
        if subdomain:
            parts_html.append(f'<span style="color: {gray};">{subdomain}.</span>')
        parts_html.append(domain)
        if rest and rest != "/":
            parts_html.append(f'<span style="color: {gray};">{rest}</span>')

        self.url_label.setText("".join(parts_html))
        self.url_label.setTextFormat(Qt.RichText)
        self.url_label.setToolTip(url)

    def run_discord_rpc(self):
        if self.discord_rpc_setting == 1:
            try:
                self.discord_rpc = RPC(
                    app_id="1254202610781655050",
                    output=False,
                    exit_if_discord_close=False,
                    exit_on_disconnect=False,
                )
            except Exception as e:
                self.discord_rpc = None
                logging.error(f"Failed to activate Discord RPC: {str(e)}")

    def update_discord_rpc(self):
        if not self.discord_rpc:
            self.run_discord_rpc()

        if self.discord_rpc:
            details = (
                self.title + "\u200b" if len(self.title) == 1 else self.title[:128]
            )
            state = self.artist[:128]
            large_image = self.artwork
            small_image = (
                "https://cdn.discordapp.com/app-icons/1254202610781655050/"
                "b4ede41d663f6caa7e45c6a042e447c9.png?size=32"
            )
            duration = self.duration
            project_url = f"https://github.com/{self.author}/{self.name}"
            video_url = f"https://music.youtube.com/watch?v={self.video_id}"

            try:
                self.discord_rpc.set_activity(
                    details=details,
                    state=state,
                    large_image=large_image,
                    small_image=small_image,
                    act_type=Activity.Listening,
                    **ProgressBar(0, duration),
                    buttons=[
                        Button("Play in Browser", video_url),
                        Button("Get App on GitHub", project_url),
                    ],
                )
            except Exception as e:
                if "[Errno 22]" in str(e) or "[Errno 32]" in str(e):
                    self.reconnect_discord_rpc()
                else:
                    logging.error(f"Failed to update Discord RPC: {str(e)}")

    def clear_discord_rpc(self):
        if self.discord_rpc:
            try:
                self.discord_rpc.clear()
            except Exception as e:
                logging.error(f"Failed to clear Discord RPC: {str(e)}")

    def reconnect_discord_rpc(self):
        if self.discord_rpc:
            self.run_discord_rpc()
            self.update_discord_rpc()

    def show_system_tray_icon(self):
        if self.tray_icon_setting == 1:
            self.system_tray_icon = SystemTrayIcon(self.windowIcon(), self)
            self.system_tray_icon.setToolTip(self.display_name)
            self.system_tray_icon.show()
        else:
            self.system_tray_icon = None

    def update_system_tray_icon_song_state(self):
        if self.tray_icon_setting == 1 and self.system_tray_icon:
            if self.song_state == "Playing":
                self.system_tray_icon.play_pause_action.setIcon(
                    recolor_icon(
                        f"{self.icon_folder}/pause.png",
                        (
                            1
                            if self.icon_color_setting == 1
                            else (
                                2
                                if self.icon_color_setting == 2
                                else self.theme_setting
                            )
                        ),
                    )
                )
                self.system_tray_icon.play_pause_action.setEnabled(True)
                self.system_tray_icon.like_action.setEnabled(True)
                self.system_tray_icon.previous_action.setEnabled(True)
                self.system_tray_icon.next_action.setEnabled(True)
                self.system_tray_icon.dislike_action.setEnabled(True)
            elif self.song_state == "Paused":
                self.system_tray_icon.play_pause_action.setIcon(
                    recolor_icon(
                        f"{self.icon_folder}/play.png",
                        (
                            1
                            if self.icon_color_setting == 1
                            else (
                                2
                                if self.icon_color_setting == 2
                                else self.theme_setting
                            )
                        ),
                    )
                )
                self.system_tray_icon.play_pause_action.setEnabled(True)
                self.system_tray_icon.like_action.setEnabled(True)
                self.system_tray_icon.previous_action.setEnabled(True)
                self.system_tray_icon.next_action.setEnabled(True)
                self.system_tray_icon.dislike_action.setEnabled(True)
            else:
                self.system_tray_icon.play_pause_action.setIcon(
                    recolor_icon(
                        f"{self.icon_folder}/play.png",
                        (
                            1
                            if self.icon_color_setting == 1
                            else (
                                2
                                if self.icon_color_setting == 2
                                else self.theme_setting
                            )
                        ),
                    )
                )
                self.system_tray_icon.play_pause_action.setEnabled(False)
                self.system_tray_icon.like_action.setEnabled(False)
                self.system_tray_icon.previous_action.setEnabled(False)
                self.system_tray_icon.next_action.setEnabled(False)
                self.system_tray_icon.dislike_action.setEnabled(False)

    def update_system_tray_icon_song_status(self):
        if self.tray_icon_setting == 1 and self.system_tray_icon:
            if self.song_status == "Like":
                self.system_tray_icon.like_action.setIcon(
                    recolor_icon(
                        f"{self.icon_folder}/like-filled.png",
                        (
                            1
                            if self.icon_color_setting == 1
                            else (
                                2
                                if self.icon_color_setting == 2
                                else self.theme_setting
                            )
                        ),
                    )
                )
                self.system_tray_icon.dislike_action.setIcon(
                    recolor_icon(
                        f"{self.icon_folder}/dislike.png",
                        (
                            1
                            if self.icon_color_setting == 1
                            else (
                                2
                                if self.icon_color_setting == 2
                                else self.theme_setting
                            )
                        ),
                    )
                )
            elif self.song_status == "Dislike":
                self.system_tray_icon.like_action.setIcon(
                    recolor_icon(
                        f"{self.icon_folder}/like.png",
                        (
                            1
                            if self.icon_color_setting == 1
                            else (
                                2
                                if self.icon_color_setting == 2
                                else self.theme_setting
                            )
                        ),
                    )
                )
                self.system_tray_icon.dislike_action.setIcon(
                    recolor_icon(
                        f"{self.icon_folder}/dislike-filled.png",
                        (
                            1
                            if self.icon_color_setting == 1
                            else (
                                2
                                if self.icon_color_setting == 2
                                else self.theme_setting
                            )
                        ),
                    )
                )
            else:
                self.system_tray_icon.like_action.setIcon(
                    recolor_icon(
                        f"{self.icon_folder}/like.png",
                        (
                            1
                            if self.icon_color_setting == 1
                            else (
                                2
                                if self.icon_color_setting == 2
                                else self.theme_setting
                            )
                        ),
                    )
                )
                self.system_tray_icon.dislike_action.setIcon(
                    recolor_icon(
                        f"{self.icon_folder}/dislike.png",
                        (
                            1
                            if self.icon_color_setting == 1
                            else (
                                2
                                if self.icon_color_setting == 2
                                else self.theme_setting
                            )
                        ),
                    )
                )

    def update_win_thumbnail_buttons_song_state(self):
        if self.win_thumbnail_toolbar:
            if self.song_state == "Playing":
                self.tool_btn_previous.setEnabled(True)
                self.tool_btn_play_pause.setIcon(
                    QIcon(f"{self.icon_folder}/pause-taskbar.png")
                )
                self.tool_btn_play_pause.setEnabled(True)
                self.tool_btn_next.setEnabled(True)
            elif self.song_state == "Paused":
                self.tool_btn_previous.setEnabled(True)
                self.tool_btn_play_pause.setIcon(
                    QIcon(f"{self.icon_folder}/play-taskbar.png")
                )
                self.tool_btn_play_pause.setEnabled(True)
                self.tool_btn_next.setEnabled(True)
            else:
                self.tool_btn_previous.setEnabled(False)
                self.tool_btn_play_pause.setIcon(
                    QIcon(f"{self.icon_folder}/play-taskbar.png")
                )
                self.tool_btn_play_pause.setEnabled(False)
                self.tool_btn_next.setEnabled(False)

    def update_picture_in_picture_song_info(self):
        if self.picture_in_picture_dialog:
            self.picture_in_picture_dialog.title_label.setText(self.title)
            self.picture_in_picture_dialog.title_label.setToolTip(self.title)
            self.picture_in_picture_dialog.artist_label.setText(self.artist)
            self.picture_in_picture_dialog.artist_label.setToolTip(self.artist)
            self.picture_in_picture_dialog.load_artwork(self.artwork)

    def update_picture_in_picture_song_state(self):
        if self.picture_in_picture_dialog:
            if self.song_state == "Playing":
                self.picture_in_picture_dialog.dislike_button.setEnabled(True)
                self.picture_in_picture_dialog.previous_button.setEnabled(True)
                self.picture_in_picture_dialog.play_pause_button.setIcon(
                    recolor_icon(
                        f"{self.icon_folder}/pause-filled.png", self.theme_setting
                    )
                )
                self.picture_in_picture_dialog.play_pause_button.setEnabled(True)
                self.picture_in_picture_dialog.next_button.setEnabled(True)
                self.picture_in_picture_dialog.like_button.setEnabled(True)
            elif self.song_state == "Paused":
                self.picture_in_picture_dialog.dislike_button.setEnabled(True)
                self.picture_in_picture_dialog.previous_button.setEnabled(True)
                self.picture_in_picture_dialog.play_pause_button.setIcon(
                    recolor_icon(
                        f"{self.icon_folder}/play-filled.png", self.theme_setting
                    )
                )
                self.picture_in_picture_dialog.play_pause_button.setEnabled(True)
                self.picture_in_picture_dialog.next_button.setEnabled(True)
                self.picture_in_picture_dialog.like_button.setEnabled(True)
            else:
                self.picture_in_picture_dialog.dislike_button.setEnabled(False)
                self.picture_in_picture_dialog.previous_button.setEnabled(False)
                self.picture_in_picture_dialog.play_pause_button.setIcon(
                    recolor_icon(
                        f"{self.icon_folder}/play-filled.png", self.theme_setting
                    )
                )
                self.picture_in_picture_dialog.play_pause_button.setEnabled(False)
                self.picture_in_picture_dialog.next_button.setEnabled(False)
                self.picture_in_picture_dialog.like_button.setEnabled(False)

    def update_picture_in_picture_song_progress(self):
        if self.picture_in_picture_dialog:
            self.picture_in_picture_dialog.BodyLabel.setText(self.current_time)
            self.picture_in_picture_dialog.BodyLabel_2.setText(self.total_time)

    def update_picture_in_picture_song_status(self):
        if self.picture_in_picture_dialog:
            if self.song_status == "Like":
                self.picture_in_picture_dialog.dislike_button.setIcon(
                    recolor_icon(f"{self.icon_folder}/dislike.png", self.theme_setting)
                )
                self.picture_in_picture_dialog.like_button.setIcon(
                    recolor_icon(
                        f"{self.icon_folder}/like-filled.png", self.theme_setting
                    )
                )
            elif self.song_status == "Dislike":
                self.picture_in_picture_dialog.dislike_button.setIcon(
                    recolor_icon(
                        f"{self.icon_folder}/dislike-filled.png", self.theme_setting
                    )
                )
                self.picture_in_picture_dialog.like_button.setIcon(
                    recolor_icon(f"{self.icon_folder}/like.png", self.theme_setting)
                )
            else:
                self.picture_in_picture_dialog.dislike_button.setIcon(
                    recolor_icon(f"{self.icon_folder}/dislike.png", self.theme_setting)
                )
                self.picture_in_picture_dialog.like_button.setIcon(
                    recolor_icon(f"{self.icon_folder}/like.png", self.theme_setting)
                )

    def start_playback_control(self):
        if self.hotkey_playback_control_setting == 1:
            self.hotkey_controller_thread = HotkeyController(self)
            self.hotkey_controller_thread.play_pause.connect(self.play_pause)
            self.hotkey_controller_thread.previous.connect(self.previous)
            self.hotkey_controller_thread.next.connect(self.next)
            self.hotkey_controller_thread.start()

    def create_previous_button(self):
        self.tool_btn_previous = QWinThumbnailToolButton(self.win_thumbnail_toolbar)
        self.tool_btn_previous.setToolTip("Previous")
        self.tool_btn_previous.setEnabled(False)
        self.tool_btn_previous.setIcon(
            QIcon(f"{self.icon_folder}/previous-taskbar.png")
        )
        self.tool_btn_previous.clicked.connect(self.previous)
        self.win_thumbnail_toolbar.addButton(self.tool_btn_previous)

    def create_play_pause_button(self):
        self.tool_btn_play_pause = QWinThumbnailToolButton(self.win_thumbnail_toolbar)
        self.tool_btn_play_pause.setToolTip("Play/Pause")
        self.tool_btn_play_pause.setEnabled(False)
        self.tool_btn_play_pause.setIcon(QIcon(f"{self.icon_folder}/play-taskbar.png"))
        self.tool_btn_play_pause.clicked.connect(self.play_pause)
        self.win_thumbnail_toolbar.addButton(self.tool_btn_play_pause)

    def create_next_button(self):
        self.tool_btn_next = QWinThumbnailToolButton(self.win_thumbnail_toolbar)
        self.tool_btn_next.setToolTip("Next")
        self.tool_btn_next.setEnabled(False)
        self.tool_btn_next.setIcon(QIcon(f"{self.icon_folder}/next-taskbar.png"))
        self.tool_btn_next.clicked.connect(self.next)
        self.win_thumbnail_toolbar.addButton(self.tool_btn_next)

    def dislike(self):
        js = """
        document
            .querySelector(
                "ytmusic-player-bar ytmusic-like-button-renderer " +
                "yt-button-shape.dislike button"
            )
            ?.click();
        """
        self.webpage.runJavaScript(js)

    def previous(self):
        js = """
        document.querySelector(".previous-button")?.click();
        """
        self.webpage.runJavaScript(js)

    def play_pause(self):
        js = """
        var v = document.querySelector("video");
        v && (v.paused ? v.play() : v.pause());
        """
        self.webpage.runJavaScript(js)

    def next(self):
        js = """
        document.querySelector(".next-button")?.click();
        """
        self.webpage.runJavaScript(js)

    def like(self):
        js = """
        document
            .querySelector(
                "ytmusic-player-bar ytmusic-like-button-renderer " +
                "yt-button-shape.like button"
            )
            ?.click();
        """
        self.webpage.runJavaScript(js)

    def read_script(self, filename):
        with open(f"{self.current_dir}/core/js/{filename}", "r", encoding="utf-8") as f:
            return f.read()

    def back(self):
        self.webview.back()

    def forward(self):
        self.webview.forward()

    def home(self):
        self.webview.load(QUrl("https://music.youtube.com/"))

    def reload(self):
        self.webview.reload()

    def stop(self):
        self.webview.stop()

    def search_on(self, service):
        if service == "MusicBrainz":
            open_url(
                "https://musicbrainz.org/search?query="
                f"{self.title}+-+{self.artist}&type=release"
            )

    def go_to_youtube(self):
        open_url(f"https://www.youtube.com/watch?v={self.video_id}")

    def select_download_folder(self):
        title = "Select Folder"
        folder = QFileDialog.getExistingDirectory(
            self, title, self.last_download_folder_setting
        )
        return folder if folder else None

    def download_song(self):
        self.start_download(f"https://music.youtube.com/watch?v={self.video_id}")

    def download_album(self):
        self.start_download(self.current_url)

    def start_download(self, download_url):
        download_folder = self.select_download_folder()
        if not download_folder:
            return

        self.last_download_folder_setting = download_folder
        self.settings_.setValue("last_download_folder", download_folder)

        self.is_downloading = True
        self.update_download_buttons_state()

        self.download_thread = DownloadThread(
            download_url,
            download_folder,
            use_cookies=self.use_cookies_setting,
            auto_update=self.auto_update_ytdlp_setting,
            embed_metadata=self.embed_metadata_setting,
            ytdlp_format=self.ytdlp_format_setting,
            parent=self,
        )
        self.download_thread.downloading_ffmpeg.connect(self.on_downloading_ffmpeg)
        self.download_thread.downloading_ffmpeg_success.connect(
            self.on_downloading_ffmpeg_success
        )

        self.download_thread.downloading_deno.connect(self.on_downloading_deno)
        self.download_thread.downloading_deno_success.connect(
            self.on_downloading_deno_success
        )

        self.download_thread.downloading_ytdlp.connect(self.on_downloading_ytdlp)
        self.download_thread.downloading_ytdlp_success.connect(
            self.on_downloading_ytdlp_success
        )

        self.download_thread.downloading_audio.connect(self.on_downloading_audio)
        self.download_thread.downloading_audio_error.connect(
            self.on_downloading_audio_error
        )
        self.download_thread.downloading_audio_success.connect(
            self.on_downloading_audio_success
        )

        self.download_thread.finished.connect(self.on_download_finished)
        self.download_thread.start()

    def show_downloading_state_tooltip(self, title, content):
        def calculate_tooltip_pos(
            parent_widget,
            tooltip_widget,
            margin=20,
            top_offset=63 if self.hide_toolbar_setting == 0 else 20,
        ):
            parent_width = parent_widget.width()
            parent_height = parent_widget.height()

            tooltip_width = tooltip_widget.width()
            tooltip_height = tooltip_widget.height()

            x = parent_width - tooltip_width - margin
            y = top_offset

            if x < 0:
                x = 0
            if y < 0:
                y = 0
            if x + tooltip_width > parent_width:
                x = parent_width - tooltip_width
            if y + tooltip_height > parent_height:
                y = parent_height - tooltip_height

            return QPoint(x, y)

        self.downloading_state_tool_tip = StateToolTip(title, content, self)
        pos = calculate_tooltip_pos(self, self.downloading_state_tool_tip)
        self.downloading_state_tool_tip.move(pos)
        self.downloading_state_tool_tip.show()

    def hide_downloading_state_tooltip(self):
        if self.downloading_state_tool_tip is not None:
            self.downloading_state_tool_tip.setState(True)
            self.downloading_state_tool_tip = None

    def on_downloading_ffmpeg(self):
        self.show_downloading_state_tooltip("Downloading ffmpeg", "Please wait...")

    def on_downloading_ffmpeg_success(self):
        self.hide_downloading_state_tooltip()

    def on_downloading_deno(self):
        self.show_downloading_state_tooltip("Downloading deno", "Please wait...")

    def on_downloading_deno_success(self):
        self.hide_downloading_state_tooltip()

    def on_downloading_ytdlp(self):
        self.show_downloading_state_tooltip("Downloading yt-dlp", "Please wait...")

    def on_downloading_ytdlp_success(self):
        self.hide_downloading_state_tooltip()

    def on_downloading_audio(self):
        self.show_downloading_state_tooltip("Downloading audio", "Please wait...")

    def on_downloading_audio_error(self, msg, title):
        self.hide_downloading_state_tooltip()

        info_bar = InfoBar.error(
            title=f"{title}",
            content="Audio downloaded failed!",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM,
            duration=-1,
            parent=self,
        )

        button = PushButton(
            recolor_icon(f"{self.icon_folder}/show.png", self.theme_setting),
            "Show error",
            self,
        )
        button.clicked.connect(lambda: self.show_download_error(msg, info_bar))
        info_bar.addWidget(button)

    def on_downloading_audio_success(self, folder, title):
        self.hide_downloading_state_tooltip()

        info_bar = InfoBar.success(
            title=f"{title}",
            content="Audio downloaded successfully!",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM,
            duration=-1,
            parent=self,
        )

        button = PushButton(
            recolor_icon(f"{self.icon_folder}/open_folder.png", self.theme_setting),
            "Open Folder",
            self,
        )
        button.clicked.connect(lambda: self.open_download_folder(folder, info_bar))
        info_bar.addWidget(button)

    def show_download_error(self, msg, info_bar):
        info_bar.close()

        QTimer.singleShot(0, lambda: self.show_error_message(msg, "yt-dlp error"))

    def open_download_folder(self, folder, info_bar):
        info_bar.close()
        open_url(folder)

    def on_download_finished(self):
        self.download_thread = None
        self.hide_downloading_state_tooltip()

        self.is_downloading = False
        self.update_download_buttons_state()

    def update_download_buttons_state(self):
        can_download_song = not self.is_downloading and bool(self.video_id)
        can_download_album = not self.is_downloading and "playlist" in self.current_url

        self.download_song_action.setEnabled(can_download_song)
        self.download_song_shortcut.setEnabled(can_download_song)
        self.download_album_action.setEnabled(can_download_album)
        self.download_album_shortcut.setEnabled(can_download_album)

    def watch_in_pip(self):
        if self.song_state == "Playing" or "Paused":
            self.picture_in_picture_dialog = PictureInPictureDialog(
                self.geometry(), self
            )
            self.update_picture_in_picture_song_info()
            self.update_picture_in_picture_song_state()
            self.update_picture_in_picture_song_progress()
            self.update_picture_in_picture_song_status()
            self.picture_in_picture_dialog.show()
            self.picture_in_picture_dialog.activateWindow()

            self.hide()
            if self.system_tray_icon:
                self.system_tray_icon.hide()

    def load_url(self, url):
        self.webview.load(QUrl(url))

    def bug_report(self):
        open_url(f"https://github.com/{self.author}/{self.name}/issues")

    def visit_github(self):
        open_url(f"https://github.com/{self.author}/{self.name}")

    def icons_by_icons8(self):
        open_url("https://icons8.com")

    def by_deeffest(self):
        open_url("https://deeffest.pythonanywhere.com")

    def hide_toolbar(self):
        if self.ToolBar.isHidden():
            self.ToolBar.show()
            self.hide_toolbar_setting = 0
        else:
            self.ToolBar.hide()
            self.hide_toolbar_setting = 1

    def cut(self):
        self.webpage.triggerAction(QWebEnginePage.Cut)

    def copy(self):
        self.webpage.triggerAction(QWebEnginePage.Copy)

    def paste(self):
        self.webpage.triggerAction(QWebEnginePage.Paste)

    def save_settings(self):
        if self.save_last_win_geometry_setting == 1:
            if self.isMaximized():
                self.settings_.setValue("maximized_state_setting", 1)
            elif self.isFullScreen():
                self.settings_.setValue(
                    "last_win_geometry", self.last_win_geometry_setting
                )
            else:
                self.settings_.setValue("last_win_geometry", self.geometry())
                self.settings_.setValue("maximized_state_setting", 0)
        if self.save_last_zoom_factor_setting == 1:
            self.settings_.setValue("last_zoom_factor", self.webview.zoomFactor())
        self.settings_.setValue(
            "ad_blocker", int(self.skip_video_ads_action.isChecked())
        )
        self.settings_.setValue(
            "only_audio_mode", int(self.audio_only_mode_action.isChecked())
        )
        self.settings_.setValue(
            "nonstop_music", int(self.nonstop_music_action.isChecked())
        )
        self.settings_.setValue(
            "hide_mini_player", int(self.hide_mini_player_action.isChecked())
        )
        self.settings_.setValue(
            "im_not_a_kid", int(self.im_not_a_kid_action.isChecked())
        )

    def show_window(self, last_win_geo=None):
        if self.isMinimized() or self.isHidden():
            if self.isMaximized():
                self.showMaximized()
            elif self.isMinimized():
                self.showNormal()
            else:
                self.show()
        self.activateWindow()
        if last_win_geo:
            self.setGeometry(last_win_geo)
        if self.system_tray_icon:
            self.system_tray_icon.last_win_geo = None

    def show_window_or_picture_in_picture(self):
        if self.picture_in_picture_dialog is None:
            self.show_window(
                self.system_tray_icon.last_win_geo if self.system_tray_icon else None
            )
        else:
            if self.picture_in_picture_dialog.isMinimized():
                if self.isMaximized():
                    self.picture_in_picture_dialog.showMaximized()
                else:
                    self.picture_in_picture_dialog.showNormal()

    def eventFilter(self, obj, event):
        if obj == self.ToolBar:
            if event.type() == QEvent.Show:
                self.hide_toolbar_action.setText("Hide toolbar")
                self.hide_toolbar_action.setIcon(
                    recolor_icon(
                        f"{self.icon_folder}/hide_toolbar.png", self.theme_setting
                    )
                )
            elif event.type() == QEvent.Hide:
                self.hide_toolbar_action.setText("Show toolbar")
                self.hide_toolbar_action.setIcon(
                    recolor_icon(f"{self.icon_folder}/toolbar.png", self.theme_setting)
                )
        return super().eventFilter(obj, event)

    def stop_running_threads(self):
        if (
            self.hotkey_controller_thread is not None
            and self.hotkey_controller_thread.isRunning()
        ):
            self.hotkey_controller_thread.stop()

        if self.download_thread is not None and self.download_thread.isRunning():
            self.download_thread.stop()

        if (
            self.update_checker_thread is not None
            and self.update_checker_thread.isRunning()
        ):
            self.update_checker_thread.stop()

        if (
            self.music_recognizer_thread is not None
            and self.music_recognizer_thread.isRunning()
        ):
            self.music_recognizer_thread.stop()

    def app_quit(self):
        self.stop_running_threads()

        app = QApplication.instance()
        if hasattr(app, "memory") and app.memory.isAttached():
            app.memory.detach()
        if hasattr(app, "server"):
            app.server.close()

    def closeEvent(self, event):
        self.save_settings()

        if self.tray_icon_setting == 1 and self.system_tray_icon is not None:
            if not self.force_exit:
                self.system_tray_icon.last_win_geo = self.geometry()
                self.hide()
                event.ignore()
                return

        if self.song_state == "Playing":
            self.show_window(
                self.system_tray_icon.last_win_geo if self.system_tray_icon else None
            )

            msg_box = MessageBox(
                "Exit confirmation",
                (
                    "Exiting now will stop the current playback and "
                    "close the application.\n"
                    "Do you want to exit now?"
                ),
                self,
            )
            msg_box.yesButton.setText("Exit")
            if not msg_box.exec_():
                self.force_exit = False
                event.ignore()
                return

        event.accept()
