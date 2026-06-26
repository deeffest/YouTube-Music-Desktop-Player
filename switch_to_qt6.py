import sys
import subprocess

QT5 = [
    "PyQt5-Fluent-Widgets",
    "PyQt5-Frameless-Window",
    "PyQt5",
    "PyQt5-Qt5",
    "PyQt5-sip",
    "PyQtWebEngine",
    "PyQtWebEngine-Qt5",
]

subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", *QT5])
subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
