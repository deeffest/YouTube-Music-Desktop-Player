from PySide6.QtCore import Signal, QObject


class SignalBus(QObject):
    show_window_sig = Signal()
    app_error_sig = Signal(str)


signal_bus = SignalBus()
