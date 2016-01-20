from nfluid.ui.elements.mainwindow import MainWindow
from nfluid.ui.manager import NfluidDataManager
from nfluid.core.channel_element import ChannelElement

from PySide import QtCore, QtGui
import sys

class NfluidGui(object):
    def __init__(self):
        """Starts the gui, taking the channel assembly it is has been
        created. If not, it will create a new one.
        """
        self.manager = NfluidDataManager()
        self.main_window = None
        self.app = None

    def create_gui(self):
        self.app = QtGui.QApplication(sys.argv)
        self.main_window = MainWindow()

    def run(self):
        if self.main_window is None:
            self.create_gui()
        self.main_window.show()
        self.app.exec_()
        

def start_gui():
    gui = NfluidGui()
    gui.run()


if __name__ == "__main__":
    start_gui()

        