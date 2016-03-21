from PySide import QtGui
from nfluid.ui.elements.tabpieceswidget import TabPiecesWidget
from nfluid.ui.manager import NfluidDataManager


class CreationPiecesWidget(QtGui.QWidget):

    def __init__(self, main_win):
        super(CreationPiecesWidget, self).__init__()
        self.create_actions()
        self.create_gui()
        self._name = "  Pieces Creation"
        self.main_win = main_win

    def name(self):
        return self._name

    def create_gui(self):
        self.layout = QtGui.QVBoxLayout()
        self.pieces_widget = TabPiecesWidget()

        self.add_button = QtGui.QPushButton("Add", parent=self)
        self.add_button.clicked.connect(self.add_action.triggered)

        self.insert_before_button = QtGui.QPushButton("Insert before",
                                                      parent=self)
        self.insert_before_button.clicked.connect(self.insert_before_action.
                                                  triggered)

        self.layout.addWidget(self.pieces_widget)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.insert_before_button)

        self.min_h = 100
        self.min_w = 100
        self.max_h = 350
        self.max_w = 500

        self.pieces_widget.setMaximumWidth(self.max_w)
        self.pieces_widget.setMaximumHeight(self.max_h)
        self.pieces_widget.setMinimumWidth(self.min_w)
        self.pieces_widget.setMinimumHeight(self.min_h)

        # self.layout.SizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.setLayout(self.layout)

    def create_actions(self):
        self.add_action = QtGui.QAction(QtGui.QIcon(), "&Add",
                                        self, statusTip="Add a new piece",
                                        triggered=self.add_current_piece)

        self.insert_before_action = \
            QtGui.QAction(QtGui.QIcon(), "&Insert before",
                          self, statusTip="Insert a new piece",
                          triggered=self.insert_piece_before)

    def add_current_piece(self):
        piece = self.pieces_widget.get_piece()
        ok = NfluidDataManager.add_piece(piece)
        if ok is 0:
            self.main_win.refresh_all()

    def insert_piece_before(self):
        piece = self.pieces_widget.get_piece()
        ok = NfluidDataManager.insert_piece_before(piece)
        if ok is 0:
            self.main_win.refresh_all()
