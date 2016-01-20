from PySide import QtCore, QtGui
from nfluid.core.channel_assembly import ChannelAssembly
from nfluid.core.channel_element import ChannelElement
from nfluid.ui.elements.tabpieceswidget import TabPiecesWidget


class CreationPiecesWidget(QtGui.QWidget):
    
    def __init__(self):
        super(CreationPiecesWidget, self).__init__()
        self.create_actions()
        self.create_gui()
        self._name = "  Pieces Creation"

    def name(self):
        return self._name

    def create_gui(self):
        self.layout = QtGui.QVBoxLayout()
        self.pieces_widget = TabPiecesWidget()
        
        self.add_button = QtGui.QPushButton("Add", parent=self)
        self.add_button.clicked.connect(self.add_action.triggered)
        
        self.layout.addWidget(self.pieces_widget)
        self.layout.addWidget(self.add_button)
        
        self.setLayout(self.layout)


    def create_actions(self):
        self.add_action = QtGui.QAction(QtGui.QIcon(), "&Add",
                self, statusTip="Add a new piece", triggered=self.add_current_piece)

    def add_current_piece(self):
        print "Adding new piece"
        print self.pieces_widget.get_piece()


        