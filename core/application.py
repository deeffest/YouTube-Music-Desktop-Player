import sys
import logging
import traceback
from typing import List

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSharedMemory, QIODevice
from PySide6.QtNetwork import QLocalServer, QLocalSocket

from core.signal_bus import signal_bus


class SingletonApplication(QApplication):
    def __init__(self, argv: List[str], key):
        super().__init__(argv)
        self.key = key
        self.timeout = 1000
        self.server = QLocalServer(self)

        self.memory = QSharedMemory(self)
        self.memory.setKey(key)
        if self.memory.attach():
            self.is_running = True
            print("Application is already running!")
            self.show_existing_instance()
            sys.exit(0)

        QLocalServer.removeServer(key)

        if not self.memory.create(1):
            logging.error(self.memory.errorString())
            sys.exit(1)

        self.is_running = False

        self.server.newConnection.connect(self.on_new_connection)
        if not self.server.listen(key):
            logging.error(self.server.errorString())
            sys.exit(1)

    def on_new_connection(self):
        socket = self.server.nextPendingConnection()
        signal_bus.show_window_sig.emit()
        socket.disconnectFromServer()

    def show_existing_instance(self):
        if not self.is_running:
            return

        socket = QLocalSocket(self)
        socket.connectToServer(self.key, QIODevice.OpenModeFlag.WriteOnly)
        if not socket.waitForConnected(self.timeout):
            logging.error(socket.errorString())
            return

        socket.disconnectFromServer()


def exception_hook(type, value, tb):
    if issubclass(type, KeyboardInterrupt):
        QApplication.quit()
        return
    logging.error("".join(traceback.format_exception(type, value, tb)))
    error_msg = "".join(traceback.format_exception(type, value, tb))
    signal_bus.app_error_sig.emit(error_msg)


sys.excepthook = exception_hook
