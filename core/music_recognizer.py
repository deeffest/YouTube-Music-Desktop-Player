import os
import time
import logging
import platform
import subprocess
from typing import TYPE_CHECKING

import requests
from PySide6.QtCore import QThread, Signal

if TYPE_CHECKING:
    from core.main_window import MainWindow


class MusicRecognizerThread(QThread):
    recording_audio_from_pc = Signal()
    recording_audio_from_pc_success = Signal()
    recognizing_via_audd_api = Signal()
    recognizing_via_audd_api_success = Signal(str, str)
    recognizing_via_audd_api_error = Signal(int, str)

    def __init__(self, service, parent=None):
        super().__init__(parent)
        self.window: "MainWindow" = parent
        self.service = service

        self.temp_wav = os.path.join(self.window.cache_dir, "temp.wav")

    def run(self):
        self.recording_audio_from_pc.emit()

        if platform.system() == "Windows":
            import numpy
            import soundfile
            import pyaudiowpatch as pyaudio

            pa = pyaudio.PyAudio()

            wasapi_info = pa.get_host_api_info_by_type(pyaudio.paWASAPI)

            default_out = pa.get_device_info_by_index(
                wasapi_info["defaultOutputDevice"]
            )

            target_idx = None
            for loopback in pa.get_loopback_device_info_generator():
                if default_out["name"] in loopback["name"]:
                    target_idx = loopback["index"]
                    break

            if target_idx is None:
                target_idx = default_out["index"]

            dev_info = pa.get_device_info_by_index(target_idx)
            rate = int(dev_info["defaultSampleRate"])
            channels = dev_info["maxInputChannels"]

            stream = pa.open(
                format=pyaudio.paFloat32,
                channels=channels,
                rate=rate,
                input=True,
                input_device_index=target_idx,
            )

            frames = []
            num_chunks = int(rate / 1024 * self.window.audd_recording_lenght_setting)
            for i in range(num_chunks):
                data = stream.read(1024, exception_on_overflow=False)
                frames.append(data)

            stream.stop_stream()
            stream.close()
            pa.terminate()

            audio_data = numpy.frombuffer(
                b"".join(frames), dtype=numpy.float32
            ).reshape(-1, channels)
            if channels > 1:
                audio_mono = audio_data.mean(axis=1)
            else:
                audio_mono = audio_data.flatten()

            abs_max = numpy.max(numpy.abs(audio_mono))
            if abs_max > 0:
                audio_mono = audio_mono / abs_max * 0.9

            soundfile.write(self.temp_wav, audio_mono, rate, subtype="PCM_16")
        else:
            if os.path.exists(self.temp_wav):
                os.remove(self.temp_wav)

            cmd = [
                "parec",
                "--device=@DEFAULT_SINK@.monitor",
                "--file-format=wav",
                "--channels=1",
                "--rate=44100",
                self.temp_wav,
            ]

            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            time.sleep(self.window.audd_recording_lenght_setting)
            process.terminate()

        self.recording_audio_from_pc_success.emit()

        if self.service == "AudD":
            self.recognizing_via_audd_api.emit()

            with open(self.temp_wav, "rb") as f:
                resp = requests.post(
                    "https://api.audd.io/",
                    data={
                        "api_token": self.window.audd_api_token_setting,
                        "return": "apple_music,spotify,deezer",
                    },
                    files={"file": f},
                    timeout=10,
                )

            resp_json = resp.json()

            if resp_json["status"] == "success" and resp_json.get("result"):
                r = resp_json["result"]
                self.recognizing_via_audd_api_success.emit(r["title"], r["artist"])
            else:
                e = resp_json.get("error", {})
                msg = e.get("error_message", "Unknown error")
                code = e.get("error_code", "Unknown code")
                logging.error(resp_json)
                self.recognizing_via_audd_api_error.emit(code, msg)

    def stop(self):
        self.terminate()
        self.wait()
