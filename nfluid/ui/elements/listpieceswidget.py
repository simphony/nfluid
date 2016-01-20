from PySide import QtCore, QtGui
from nfluid.ui.manager import NfluidDataManager


class ListPiecesWidget(QtGui.QWidget):
    
    def __init__(self):
        super(ListPiecesWidget, self).__init__()
        self.create_actions()
        self.create_gui()
        self._name = "  Current Pieces"

    def name(self):
        return self._name

    def create_gui(self):
        self.layout = QtGui.QVBoxLayout(self)

        self.list_pieces = QtGui.QListWidget(self)
        self.list_pieces.addItem('flow_adapter_0')
        self.list_pieces.addItem('flow_adapter_1')
        self.list_pieces.addItem('flow_adapter_2')
        self.list_pieces.addItem('coupling_0')
        self.list_pieces.addItem('coupling_1')
        self.list_pieces.addItem('tee_0')

        self.delete_button = QtGui.QPushButton("Delete", parent=self)
        self.delete_button.clicked.connect(self.delete_action.triggered)
        
        self.layout.addWidget(self.list_pieces)
        self.layout.addWidget(self.delete_button)
        
        self.setLayout(self.layout)

    def create_actions(self):
        self.delete_action = QtGui.QAction(QtGui.QIcon(), "&Delete",
                self, statusTip="Delete the selected piece", triggered=self.delete_current_piece)

    def delete_current_piece(self):
        print "Deleting current piece"
        print NfluidDataManager.model