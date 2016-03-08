from PySide import QtGui
from nfluid.ui.manager import NfluidDataManager, Piece
from nfluid.core.channel_info import PieceInfo


class PiecePanelWidget(QtGui.QWidget):

    def __init__(self, main_win):
        super(PiecePanelWidget, self).__init__()
        self.create_actions()
        self.create_gui()
        self._name = "  Piece Info"
        self.main_win = main_win
        self.refresh_gui()

    def name(self):
        return self._name

    def create_gui(self):
        self.layout = QtGui.QVBoxLayout(self)

        # self.apply_changes_button = QtGui.QPushButton("Delete", parent=self)
        # self.apply_changes_button.clicked.connect(self.apply_changes_action.triggered)

        self.text_widget = QtGui.QTextEdit()
        self.text_widget.setReadOnly(True)
        # self.layout.addWidget(self.apply_changes_button)

        self.min_h = 100
        self.min_w = 100
        self.max_h = 350
        self.max_w = 500

        self.layout.addWidget(self.text_widget)

        self.setLayout(self.layout)

    def create_actions(self):
        self.apply_changes_action = QtGui.QAction(
                                      QtGui.QIcon(), "&Apply",
                                      self,
                                      statusTip="Change the selected piece",
                                      triggered=self.apply_changes_current_piece)

    def apply_changes_current_piece(self):
        current_piece = self.current_piece()
        if current_piece.id != -1:
            NfluidDataManager.remove_piece(current_piece)
            self.main_win.refresh_all()

    def refresh_gui(self):
        print "refresh_gui called"
        cur_piece = self.current_piece()
        print "cur_piece"
        print cur_piece
        if cur_piece is not None:
            cur_elem = NfluidDataManager.get_piece(cur_piece)
            info = PieceInfo(cur_elem)
            self.text_widget.setText(str(info))
            # get the params!

    def current_piece(self):
        return self.main_win.get_current_piece()
