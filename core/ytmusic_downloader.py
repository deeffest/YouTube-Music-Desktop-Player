import os
import json
import shutil
import sqlite3
import logging
import requests
import platform
import subprocess
from typing import TYPE_CHECKING

from PyQt5.QtCore import QThread, pyqtSignal

if TYPE_CHECKING:
    from core.main_window import MainWindow


class DownloadThread(QThread):
    downloading_ffmpeg = pyqtSignal()
    downloading_ffmpeg_success = pyqtSignal()

    downloading_deno = pyqtSignal()
    downloading_deno_success = pyqtSignal()

    downloading_ytdlp = pyqtSignal()
    downloading_ytdlp_success = pyqtSignal()

    downloading_audio = pyqtSignal()
    downloading_audio_error = pyqtSignal(str, str)
    downloading_audio_success = pyqtSignal(str, str)

    def __init__(
        self,
        url,
        download_folder,
        use_cookies,
        auto_update,
        embed_metadata,
        ytdlp_format,
        parent=None,
    ):
        super().__init__(parent)
        self.window: "MainWindow" = parent
        self.url = url
        self.download_folder = download_folder
        self.use_cookies = use_cookies
        self.auto_update = auto_update
        self.embed_metadata = embed_metadata
        self.ytdlp_format = ytdlp_format

        self.format_name = {0: "opus", 1: "m4a", 2: "mp4", 3: "webm"}
        self.cookies_txt = os.path.join(self.window.cache_dir, "cookies.txt")
        self.cookies_sqlite = os.path.join(
            self.window.webview.page().profile().persistentStoragePath(), "Cookies"
        )

    def run(self):
        self.ensure_tools()
        if self.use_cookies:
            self.export_cookies()
        self.emit_command()

    def get_ffmpeg(self):
        if self.window.prefer_system_ffmpeg_setting == 1:
            system = shutil.which("ffmpeg")
            if system:
                return system
        return self.window.ffmpeg_path

    def get_deno(self):
        if self.window.prefer_system_deno_setting == 1:
            system = shutil.which("deno")
            if system:
                return system
        return self.window.deno_path

    def ensure_tools(self):
        def download_binary(url, dst_path):
            tmp_path = dst_path + ".tmp"
            r = requests.get(
                url,
                stream=True,
                timeout=10,
            )
            r.raise_for_status()
            with open(tmp_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            os.rename(tmp_path, dst_path)
            if platform.system() != "Windows":
                os.chmod(dst_path, 0o755)

        os.makedirs(os.path.join(self.window.home_dir, "bin"), exist_ok=True)

        if self.get_ffmpeg() == self.window.ffmpeg_path and not os.path.isfile(
            self.window.ffmpeg_path
        ):
            self.downloading_ffmpeg.emit()
            download_binary(self.window.ffmpeg_url, self.window.ffmpeg_path)
            self.downloading_ffmpeg_success.emit()
        if self.get_deno() == self.window.deno_path and not os.path.isfile(
            self.window.deno_path
        ):
            self.downloading_deno.emit()
            download_binary(self.window.deno_url, self.window.deno_path)
            self.downloading_deno_success.emit()
        if not os.path.isfile(self.window.ytdlp_path):
            self.downloading_ytdlp.emit()
            download_binary(self.window.ytdlp_url, self.window.ytdlp_path)
            self.downloading_ytdlp_success.emit()

    def export_cookies(self):
        if not os.path.exists(self.cookies_sqlite):
            return

        conn = sqlite3.connect(self.cookies_sqlite)
        cursor = conn.cursor()

        def chrome_time_to_unix(chrome_time):
            return int(chrome_time / 1_000_000 - 11644473600) if chrome_time else 0

        with open(self.cookies_txt, "w", encoding="utf-8") as f:
            f.write("# Netscape HTTP Cookie File\n")
            for row in cursor.execute(
                "SELECT host_key, path, is_secure, expires_utc, name, value "
                "FROM cookies"
            ):
                domain, path, is_secure, expires_utc, name, value = row
                include_subdomains = "TRUE" if domain.startswith(".") else "FALSE"
                expires = chrome_time_to_unix(expires_utc)
                secure_flag = "TRUE" if is_secure else "FALSE"
                f.write(
                    f"{domain}\t{include_subdomains}\t{path}\t{secure_flag}\t"
                    f"{expires}\t{name}\t{value}\n"
                )
        conn.close()

    def emit_command(self):
        url = self.url.replace("music.youtube.com", "www.youtube.com")
        is_playlist = "list=" in url and "watch" not in url

        output_template = (
            "%(playlist_title).80B/%(title).150B.%(ext)s"
            if is_playlist
            else "%(title).150B.%(ext)s"
        )

        is_video = self.ytdlp_format in (2, 3)

        if self.ytdlp_format == 1:
            format_selector = "ba[ext=m4a]/ba/best"
        elif self.ytdlp_format == 2:
            format_selector = (
                "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best"
            )
        elif self.ytdlp_format == 3:
            format_selector = (
                "bestvideo[ext=webm]+bestaudio[ext=webm]/bestvideo+bestaudio/best"
            )
        else:
            format_selector = "ba/best"

        command = [
            self.window.ytdlp_path,
            "-f",
            format_selector,
            "--ffmpeg-location",
            self.get_ffmpeg(),
            "-o",
            output_template,
            "--print-json",
            "--socket-timeout",
            "10",
            "--js-runtimes",
            f"deno:{self.get_deno()}",
        ]

        if is_video:
            command += ["--merge-output-format", self.format_name[self.ytdlp_format]]
        else:
            command += [
                "--extract-audio",
                "--audio-format",
                self.format_name[self.ytdlp_format],
            ]

        if self.embed_metadata:
            command += ["--embed-metadata"]
            if self.ytdlp_format != 3:
                command += [
                    "--embed-thumbnail",
                    "--convert-thumbnails",
                    "jpg",
                    "--ppa",
                    "ThumbnailsConvertor+ffmpeg_o:-vf crop=ih:ih",
                ]

        if "watch" in url and "list=" in url:
            command.append("--no-playlist")

        if self.use_cookies and os.path.exists(self.cookies_txt):
            command += ["--cookies", self.cookies_txt]

        command.append(url)
        self.start_ytdlp(command)

    def start_ytdlp(self, command):
        self.downloading_audio.emit()

        if self.auto_update:
            try:
                cflags = 0
                if platform.system() == "Windows":
                    cflags = subprocess.CREATE_NO_WINDOW

                subprocess.run(
                    [self.window.ytdlp_path, "--update"],
                    check=False,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=cflags,
                )
            except Exception as e:
                logging.error(f"Failed to update yt-dlp: {e}")

        kwargs = dict(
            cwd=self.download_folder,
            capture_output=True,
            text=False,
        )

        if platform.system() == "Windows":
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

        result = subprocess.run(command, **kwargs)

        stdout_decoded = (
            result.stdout.decode("utf-8", errors="ignore") if result.stdout else ""
        )
        stderr_decoded = (
            result.stderr.decode("utf-8", errors="ignore") if result.stderr else ""
        )

        lines = stdout_decoded.strip().splitlines()
        titles = []
        playlist_title = None
        for line in lines:
            try:
                data = json.loads(line)
                titles.append(data.get("title", "Unknown"))
                if not playlist_title and "playlist_title" in data:
                    playlist_title = data["playlist_title"]
            except Exception:
                titles.append("Unknown")

        title = (
            playlist_title if playlist_title else (titles[0] if titles else "Unknown")
        )

        if result.returncode == 0:
            self.downloading_audio_success.emit(self.download_folder, title)
        else:
            e = stderr_decoded.strip()
            logging.error(e)
            self.downloading_audio_error.emit(e, title)

    def stop(self):
        self.terminate()
        self.wait()
