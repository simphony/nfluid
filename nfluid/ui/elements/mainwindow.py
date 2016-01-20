from PySide import QtCore, QtGui
from nfluid.ui.elements.creationpieceswidget import CreationPiecesWidget
from nfluid.ui.elements.listpieceswidget import ListPiecesWidget
from nfluid.ui.elements.visualizer import VisVisWidget


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.create_gui()

    def create_gui(self):
        self.dw_pieces_creation = QtGui.QDockWidget()
        cur_widget = CreationPiecesWidget()
        print cur_widget
        self.dw_pieces_creation.setWidget(cur_widget)
        self.dw_pieces_creation.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        title = QtGui.QLabel(cur_widget.name())
        self.dw_pieces_creation.setTitleBarWidget(title)

        self.dw_pieces_list = QtGui.QDockWidget()
        cur_widget = ListPiecesWidget()
        self.dw_pieces_list.setWidget(cur_widget)
        self.dw_pieces_list.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        title = QtGui.QLabel(cur_widget.name())
        self.dw_pieces_list.setTitleBarWidget(title)
        
        self.cw_visualizer = VisVisWidget()

        self.menu_main = None

        self.status_bar = None

        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dw_pieces_creation)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dw_pieces_list)
        self.setCentralWidget(self.cw_visualizer)
    