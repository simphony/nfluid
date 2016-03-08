from PySide import QtGui
from nfluid.ui.manager import NfluidDataManager, Piece


class PiecesList(QtGui.QListWidget):
    def __init__(self, parent, main_win):
        self.main_win = main_win
        self.parent = parent
        super(PiecesList, self).__init__(parent)
        self.itemClicked.connect(self.on_item_click)

    def on_item_click(self, item):
        print "Hola!!"
        super(PiecesList, self).setCurrentItem(item)
        name = item.text()
        print name
        self.main_win.set_selected(name)
        # self.parent.set_selected(name)
        


class ListPiecesWidget(QtGui.QWidget):

    def __init__(self, main_win):
        super(ListPiecesWidget, self).__init__()
        self._name = "  Current Pieces"
        self.main_win = main_win
        self.create_actions()
        self.create_gui()
        self.refresh_gui()

    def name(self):
        return self._name

    def set_selected(self, name):
        n = self.list_pieces.count()
        for i in xrange(n):
            cur_item = self.list_pieces.item(i)
            cur_name = cur_item.text()
            if cur_name == name:
                row = i
                break
        # row = self.list_pieces.row(QtGui.QListWidgetItem(name))
        print "row ! ! ! "
        print row
        self.list_pieces.setCurrentRow(row)

    def create_gui(self):
        self.layout = QtGui.QVBoxLayout(self)

        self.list_pieces = PiecesList(self, self.main_win)

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
        current_piece = self.current_piece()
        if current_piece.id != -1:
            NfluidDataManager.remove_piece(current_piece)
            self.main_win.refresh_all()

    def restart_pieces(self):
        NfluidDataManager.remove_all()
        self.main_win.refresh_all()

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
            return None
        piece = piece_item.text()
        res.set_name(piece)
        return res
