from PySide import QtGui
from nfluid.ui.manager import NfluidDataManager, Piece


class ListPiecesWidget(QtGui.QWidget):

    def __init__(self, main_win):
        super(ListPiecesWidget, self).__init__()
        self.create_actions()
        self.create_gui()
        self._name = "  Current Pieces"
        self.main_win = main_win
        self.refresh_gui()

    def name(self):
        return self._name

    def create_gui(self):
        self.layout = QtGui.QVBoxLayout(self)

        self.list_pieces = QtGui.QListWidget(self)

        self.delete_button = QtGui.QPushButton("Delete", parent=self)
        self.delete_button.clicked.connect(self.delete_action.triggered)

        self.restart_button = QtGui.QPushButton("Restart", parent=self)
        self.restart_button.clicked.connect(self.restart_action.triggered)

        self.layout.addWidget(self.list_pieces)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.restart_button)

        self.min_h = 100
        self.min_w = 100
        self.max_h = 350
        self.max_w = 500

        self.list_pieces.setMaximumWidth(self.max_w)
        self.list_pieces.setMaximumHeight(self.max_h)
        self.list_pieces.setMinimumWidth(self.min_w)
        self.list_pieces.setMinimumHeight(self.min_h)

        self.setLayout(self.layout)

    def create_actions(self):
        self.delete_action = QtGui.QAction(
                                QtGui.QIcon(), "&Delete",
                                self,
                                statusTip="Delete the selected piece",
                                triggered=self.delete_current_piece)

        self.restart_action = QtGui.QAction(
                                QtGui.QIcon(), "&Restart",
                                self, statusTip="Delete the selected piece",
                                triggered=self.restart_pieces)

    def delete_current_piece(self):
        print "Deleting current piece"
        current_piece = self.current_piece()
        if current_piece.id != -1:
            NfluidDataManager.remove_piece(current_piece)
            self.main_win.refresh_all()

    def restart_pieces(self):
        print "Deleting all pieces"
        NfluidDataManager.remove_all()
        self.main_win.refresh_all()
        # print self.current_piece().name()

    def refresh_gui(self):
        self.list_pieces.clear()
        pieces = NfluidDataManager.list_of_pieces()
        for piece in pieces:
            name = piece.name()
            self.list_pieces.addItem(name)

    def current_piece(self):
        piece_item = self.list_pieces.currentItem()
        res = Piece()
        if piece_item is None:
            return res
        piece = piece_item.text()
        res.set_name(piece)
        return res
