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
        self.manager = None
        self.main_window = None
        
    def create_gui(self):
        self.main_window = MainWindow()
        self.manager = NfluidDataManager(self.main_window)
        # self.app.aboutToQuit.connect(self.exit_handler)
        
    def exit_handler(self):
        self.main_window.exit_handler()

    def run(self):
        app = QtGui.QApplication.instance()
        if app is None:
            app = QtGui.QApplication(sys.argv)
        app.aboutToQuit.connect(self.exit_handler)
        
        if self.main_window is None:
            self.create_gui()
        self.main_window.show()
        
        
        app.exec_()
        QtGui.QApplication.instance()
        
        self.main_window = None

        

def start_gui():
    gui = NfluidGui()
    gui.run()


if __name__ == "__main__":
    start_gui()

        