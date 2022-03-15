#!/bin/python3
import os
import sys

from Adafruit_IO import Client
from PySide6 import QtWidgets, QtGui

ADAFRUIT_IO_USERNAME = 'i_sandwich'
ADAFRUIT_IO_KEY = 'aio_fMAi58HKkhQeaEa8tlenXZkNwUD0'
FEED_ID = 'autoblinds1'

NUM_RETRIES = 3
RETRY_DELAY = 0.1  # seconds


def send_to_aio(aio_client, value):
    test = aio_client.feeds(FEED_ID)
    aio_client.send_data(test.key, value)


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    """
    CREATE A SYSTEM TRAY ICON CLASS AND ADD MENU
    """
    aio_client = None

    def __init__(self, icon, client, parent=None):
        self.aio_client = client

        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip(f'Local blinds control')
        menu = QtWidgets.QMenu(parent)

        open_cal = menu.addAction("🔲 Blinds up")
        open_cal.triggered.connect(self.blinds_up)

        open_app = menu.addAction("⬛ Blinds down")
        open_app.triggered.connect(self.blinds_down)

        open_app = menu.addAction("🛑 Blinds stop")
        open_app.triggered.connect(self.blinds_stop)

        open_app = menu.addAction("🙊 Quiet")
        open_app.triggered.connect(self.setup_quiet)

        open_cal = menu.addAction("🐵 Default speed")
        open_cal.triggered.connect(self.setup_default)

        exit_ = menu.addAction("💩 ‍Exit")
        exit_.triggered.connect(lambda: sys.exit())
        # exit_.setIcon(QtGui.QIcon("icon.png"))

        menu.addSeparator()
        self.setContextMenu(menu)
        self.activated.connect(self.onTrayIconActivated)

    def onTrayIconActivated(self, reason):
        """
        This function will trigger function on click or double click
        :param reason:
        :return:
        """
        if reason == self.DoubleClick:
            self.open_notepad()
        # if reason == self.Trigger:
        #     self.open_notepad()

    def blinds_stop(self):
        send_to_aio(self.aio_client, 0)

    def blinds_up(self):
        send_to_aio(self.aio_client, 1)

    def blinds_down(self):
        send_to_aio(self.aio_client, 2)

    def left_blinds_up(self):
        send_to_aio(self.aio_client, 3)

    def left_blinds_down(self):
        send_to_aio(self.aio_client, 4)

    def right_blinds_up(self):
        send_to_aio(self.aio_client, 5)

    def right_blinds_down(self):
        send_to_aio(self.aio_client, 6)

    def setup_default(self):
        send_to_aio(self.aio_client, 7)

    def setup_quiet(self):
        send_to_aio(self.aio_client, 8)

    def open_notepad(self):
        """
        this function will open application
        :return:
        """
        os.system('notepad')

    def open_calc(self):
        """
        this function will open application
        :return:
        """
        os.system('calc')


def main():
    print('Setting up aio client')
    aio_client = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

    print('Setting up widget')
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon("icon.png"), aio_client, widget)
    tray_icon.show()
    tray_icon.showMessage('Local blinds control', 'Hello! 🐸')
    print('Starting widget')
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
