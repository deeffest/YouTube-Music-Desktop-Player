from typing import TYPE_CHECKING

from PyQt5.QtCore import QObject, pyqtSlot

if TYPE_CHECKING:
    from core.main_window import MainWindow


class WebChannelBackend(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window: "MainWindow" = parent

    @pyqtSlot(str, str, str, str, int)
    def song_info_changed(self, title, artist, artwork, video_id, duration):
        self.window.title = title
        self.window.artist = artist
        self.window.artwork = artwork
        self.window.video_id = video_id
        self.window.duration = duration

        is_empty = (
            not self.window.title
            or not self.window.artist
            or not self.window.artwork
            or not self.window.video_id
            or not self.window.duration
        )

        if is_empty:
            window_title = self.window.display_name
            self.window.clear_discord_rpc()
            self.window.go_to_youtube_action.setEnabled(False)
            self.window.go_to_youtube_shortcut.setEnabled(False)
            self.window.musicbrainz_action.setEnabled(False)
            self.window.musicbrainz_shortcut.setEnabled(False)
            self.window.spotify_action.setEnabled(False)
            self.window.spotify_shortcut.setEnabled(False)
            self.window.genius_action.setEnabled(False)
            self.window.genius_shortcut.setEnabled(False)
        else:
            window_title = f"{self.window.title} - {self.window.display_name}"
            self.window.update_picture_in_picture_song_info()
            self.window.update_discord_rpc()
            self.window.go_to_youtube_action.setEnabled(True)
            self.window.go_to_youtube_shortcut.setEnabled(True)
            self.window.musicbrainz_action.setEnabled(True)
            self.window.musicbrainz_shortcut.setEnabled(True)
            self.window.spotify_action.setEnabled(True)
            self.window.spotify_shortcut.setEnabled(True)
            self.window.genius_action.setEnabled(True)
            self.window.genius_shortcut.setEnabled(True)

        self.window.update_download_buttons_state()
        self.window.setWindowTitle(window_title)
        if self.window.system_tray_icon is not None:
            self.window.system_tray_icon.setToolTip(window_title)

    @pyqtSlot(str)
    def song_state_changed(self, state):
        self.window.song_state = state

        if self.window.song_state == "Playing" or self.window.song_state == "Paused":
            self.window.watch_in_pip_action.setEnabled(True)
            self.window.watch_in_pip_tbutton.setEnabled(True)
            self.window.watch_in_pip_shortcut.setEnabled(True)
        else:
            self.window.watch_in_pip_action.setEnabled(False)
            self.window.watch_in_pip_tbutton.setEnabled(False)
            self.window.watch_in_pip_shortcut.setEnabled(False)

        self.window.update_picture_in_picture_song_state()
        self.window.update_win_thumbnail_buttons_song_state()
        self.window.update_system_tray_icon_song_state()

    @pyqtSlot(str, str)
    def song_progress_changed(self, current_time, total_time):
        self.window.current_time = current_time
        self.window.total_time = total_time

        self.window.update_picture_in_picture_song_progress()

    @pyqtSlot(str)
    def song_status_changed(self, status):
        if status != "":
            self.window.song_status = status
        else:
            self.window.song_status = "Indifferent"

        self.window.update_picture_in_picture_song_status()
        self.window.update_system_tray_icon_song_status()
