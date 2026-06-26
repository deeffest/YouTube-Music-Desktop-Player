import sys
import subprocess

QT6 = [    
    "PySide6",
    "PySide6-Essentials",
    "PySide6-Addons",
    "shiboken6",
    "PySide6-Fluent-Widgets",
    "PySideSix-Frameless-Window",
]

subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", *QT6])
subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
