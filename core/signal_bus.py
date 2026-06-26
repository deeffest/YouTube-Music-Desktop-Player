from PyQt5.QtCore import pyqtSignal, QObject


class SignalBus(QObject):
    show_window_sig = pyqtSignal()
    app_error_sig = pyqtSignal(str)


signal_bus = SignalBus()
