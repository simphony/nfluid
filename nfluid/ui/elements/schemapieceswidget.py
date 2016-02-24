from PySide import QtGui, QtCore
from nfluid.ui.manager import NfluidDataManager, Piece
from nfluid.util.tree import TreeFunctions


# class TreeFunctionsSchemaPieces(TreeFunctions):
    # scene
    
    # @classmethod
    # def reset(cls):
        # TreeFunctions.reset()


# class SchemaPiecesWidget(QtGui.QWidget):

    # def __init__(self, main_win):
        # super(SchemaPiecesWidget, self).__init__()
        # self.main_win = main_win
        # self._name = "SSSSS"
        # self.initUI()

    # def name(self):
        # return self._name

    # def initUI(self):

        # hbox=QtGui.QHBoxLayout()
        # leftpanel=QtGui.QFrame()
        # leftpanel.setGeometry(0,0,300,400)
        # self.scene=QtGui.QGraphicsScene()
        # self.scene.addText("Hello, world!")
        # view=QtGui.QGraphicsView(self.scene,leftpanel)
        # view.setSceneRect(0,0,300,400)
        # pen=QtGui.QPen(QtCore.Qt.black,2)
        # self.scene.addLine(0,0,200,200,pen)
        # hbox.addWidget(leftpanel)
        # rightpanel=QtGui.QFrame()
        # hbox.addWidget(rightpanel)
        # szoveg=QtGui.QLabel(rightpanel)
        # szoveg.setText(u"Hello World!")
        # self.setLayout(hbox)
        # self.resize(500,500)
        # self.setWindowTitle('blabla')
        # self.show()

    # def refresh_gui(self):
        # pass




class SchemaPiecesWidget(QtGui.QWidget):

    def __init__(self, main_win):
        super(SchemaPiecesWidget, self).__init__()
        self.create_actions()
        self.create_gui()
        self._name = "  Assembly Structure"
        self.main_win = main_win
        self.refresh_gui()
        self.name_space = 20
        self.level_space = 40

    def name(self):
        return self._name

    def create_gui(self):
        self.layout = QtGui.QVBoxLayout(self)

        self.schema_scene = QtGui.QGraphicsScene(self)
        self.schema_view = QtGui.QGraphicsView(self.schema_scene)

        self.layout.addWidget(self.schema_view)

        self.setLayout(self.layout)

        self.rect_pen = QtGui.QPen()
        self.rect_pen.setWidth(3)
        self.rect_pen.setStyle(QtCore.Qt.SolidLine)
        self.rect_pen.setColor(QtGui.QColor(0, 0, 0))

        self.rect_brush = QtGui.QBrush()
        self.rect_brush.setColor(QtGui.QColor(166, 227, 247))
        self.rect_brush.setStyle(QtCore.Qt.SolidPattern)

    def create_actions(self):
        pass

    def add_element(self, elem, x, y):
        self.schema_scene.addRect(x, y, self.name_space, self.level_space,
                                  pen=self.rect_pen, brush=self.rect_brush) 

    def refresh_gui(self):
        tree = NfluidDataManager.get_assembly_tree()
        if tree is not None:
            init = tree.get_root()
            width = tree.amplitude()
            init_x = width * self.name_space
            init_y = 0
            self.add_element("hahaha", init_x, init_y)
            
            
            # name_space = 20
            # strings_struct = tree.strings_structure(name_space)
            # print " - - - - - - - strings_struct - - - - - - - "
            # print strings_struct
