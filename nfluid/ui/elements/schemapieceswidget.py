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
        self.name_space = 100
        self.level_space = 20
        self.floor_space = 20
        self.connection_space = 20

    def name(self):
        return self._name

    def create_gui(self):
        self.layout = QtGui.QVBoxLayout(self)

        self.schema_scene = QtGui.QGraphicsScene(self)
        self.schema_view = QtGui.QGraphicsView(self.schema_scene)

        self.layout.addWidget(self.schema_view)

        self.setLayout(self.layout)

        self.rect_pen = QtGui.QPen()
        self.pen_width = 3
        self.rect_pen.setWidth(self.pen_width)
        self.rect_pen.setStyle(QtCore.Qt.SolidLine)
        # self.rect_pen.setColor(QtGui.QColor(0, 0, 0))
        self.rect_pen.setColor(QtGui.QColor(26, 32, 201))

        gradient = QtGui.QLinearGradient()
        # gradient.setColorAt(0, QtGui.QColor.fromRgbF(0, 1, 0, 1))
        # gradient.setColorAt(1, QtGui.QColor.fromRgbF(0, 0, 0, 0))
        # self.rect_brush = QtGui.QBrush(gradient)
        self.rect_brush = QtGui.QBrush()
        # self.rect_brush.setColor(QtGui.QColor(166, 227, 247))
        self.rect_brush.setColor(QtGui.QColor(232, 219, 100))
        self.rect_brush.setStyle(QtCore.Qt.SolidPattern)

        self.rect_brush.setStyle(QtCore.Qt.LinearGradientPattern)

        self.schema_view.setHorizontalScrollBarPolicy(
                            QtCore.Qt.ScrollBarAlwaysOn)
        self.schema_view.setVerticalScrollBarPolicy(
                            QtCore.Qt.ScrollBarAlwaysOn)

        self.schema_view.setSceneRect(0, 0, 300, 600)

    def create_actions(self):
        pass

    def add_element(self, elem, x, y):
        self.schema_scene.addRect(x, y, self.name_space, self.level_space,
                                  pen=self.rect_pen, brush=self.rect_brush)
        text = self.schema_scene.addSimpleText(elem)
        len_text = text.boundingRect().width()
        print "len_text"
        print len_text
        margin = (self.name_space - len_text) / 2
        print "margin"
        print margin
        text.setX(x + self.pen_width + margin)
        text.setY(y + self.pen_width)

    def add_connection(self, x_from, y_from, x_to, y_to):
        f_x = x_from + self.pen_width + (self.name_space / 2)
        f_y = y_from + self.pen_width + self.level_space
        t_x = x_to + self.pen_width + (self.name_space / 2)
        t_y = y_to
        self.schema_scene.addLine(f_x, f_y, t_x, t_y)

    def draw_elements(self, elem, x, y, width, cur_amp):
        if elem is not None:
            self.add_element(elem.data.name(), x, y)
            if elem.next_l is not None:
                if elem.next_r is not None:
                    # new_x = x - (width * ((self.name_space / 2) + self.floor_space))
                    cur_width = width / cur_amp
                    new_x = x - cur_width
                    new_amp = cur_amp + 1
                    # new_x = x - (x / 2)
                else:
                    new_x = x
                    cur_width = width
                    new_amp = cur_amp
                new_y = y + (self.level_space + self.connection_space) 
                self.add_connection(x, y, new_x, new_y)
                self.draw_elements(elem.next_l, new_x, new_y, cur_width,
                                   new_amp)
            if elem.next_r is not None:
                if elem.next_l is not None:
                    # new_x = x + (width * ((self.name_space / 2) + self.floor_space))
                    cur_width = width / cur_amp
                    new_x = x + cur_width
                    new_amp = cur_amp + 1
                    # new_x = x + (x / 2)
                else:
                    new_x = x
                    cur_width = width
                    new_amp = cur_amp
                new_y = y + (self.level_space + self.connection_space) 
                self.add_connection(x, y, new_x, new_y)
                self.draw_elements(elem.next_r, new_x, new_y, cur_width,
                                   new_amp)

    def refresh_gui(self):
        tree = NfluidDataManager.get_assembly_tree()
        if tree is not None:
            init = tree.get_root()
            width = tree.amplitude() + 1
            height = tree.depth() + 1
            total_width = (width) * (self.name_space + self.floor_space + self.pen_width)
            total_height = (height) * (self.level_space + self.connection_space + self.pen_width)
            self.schema_view.setSceneRect(0, 0, total_width, total_height)
            self.schema_scene.clear()
            print "width, height"
            print width, height
            init_x = total_width / 2
            init_x -= (self.name_space) / 2
            init_y = 10
            self.draw_elements(init, init_x, init_y, total_width/4, 1)
            # self.add_element(init.data.name(), init_x, init_y)
            
            
            # name_space = 20
            # strings_struct = tree.strings_structure(name_space)
            # print " - - - - - - - strings_struct - - - - - - - "
            # print strings_struct
