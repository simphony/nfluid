from PySide import QtCore, QtGui
from nfluid.ui.elements.creationpieceswidget import CreationPiecesWidget
from nfluid.ui.elements.listpieceswidget import ListPiecesWidget
from nfluid.ui.elements.schemapieceswidget import SchemaPiecesWidget
from nfluid.ui.elements.piecepanelwidget import PiecePanelWidget
from nfluid.ui.elements.visualizer import VisVisWidget
from nfluid.ui.elements.geometrytoolbar import GeometryToolbar
from nfluid.ui.manager import NfluidDataManager, Piece
from nfluid.util.vector import Vector


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.create_actions()
        self.create_gui()
        self.refresh_all()

    def create_gui(self):
        # General parameters -------------------------------------------------
        min_h = 100
        min_w = 100
        max_h = 350
        max_w = 500

        # Tool bars ----------------------------------------------------------

        self.tb_geometry = GeometryToolbar(self)
        self.addToolBar(self.tb_geometry)

        # Dock Widgets -------------------------------------------------------
        self.dw_pieces_creation = QtGui.QDockWidget()
        cur_widget = CreationPiecesWidget(self)
        self.dw_pieces_creation.setWidget(cur_widget)
        self.dw_pieces_creation.setFeatures(
                    QtGui.QDockWidget.NoDockWidgetFeatures)
        title = QtGui.QLabel(cur_widget.name())
        self.dw_pieces_creation.setTitleBarWidget(title)
        self.dw_pieces_creation.setMaximumWidth(max_w)
        self.dw_pieces_creation.setMaximumHeight(max_h)
        self.dw_pieces_creation.setMinimumWidth(min_w)
        self.dw_pieces_creation.setMinimumHeight(min_h)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea,
                           self.dw_pieces_creation)

        self.dw_pieces_list = QtGui.QDockWidget()
        cur_widget = ListPiecesWidget(self)
        self.dw_pieces_list.setWidget(cur_widget)
        self.dw_pieces_list.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        title = QtGui.QLabel(cur_widget.name())
        self.dw_pieces_list.setTitleBarWidget(title)
        self.dw_pieces_list.setMaximumWidth(max_w)
        self.dw_pieces_list.setMaximumHeight(max_h)
        self.dw_pieces_list.setMinimumWidth(min_w)
        self.dw_pieces_list.setMinimumHeight(min_h)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dw_pieces_list)

        self.dw_pieces_schema = QtGui.QDockWidget()
        cur_widget = SchemaPiecesWidget(self)
        self.dw_pieces_schema.setWidget(cur_widget)
        self.dw_pieces_schema.setFeatures(QtGui.QDockWidget.
                                          NoDockWidgetFeatures)
        title = QtGui.QLabel(cur_widget.name())
        self.dw_pieces_schema.setTitleBarWidget(title)
        self.dw_pieces_schema.setMaximumWidth(max_w)
        self.dw_pieces_schema.setMaximumHeight(max_h)
        self.dw_pieces_schema.setMinimumWidth(min_w)
        self.dw_pieces_schema.setMinimumHeight(min_h)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dw_pieces_schema)

        self.dw_piece_panel_widget = QtGui.QDockWidget()
        cur_widget = PiecePanelWidget(self)
        self.dw_piece_panel_widget.setWidget(cur_widget)
        title = QtGui.QLabel(cur_widget.name())
        self.dw_piece_panel_widget.setTitleBarWidget(title)
        self.dw_piece_panel_widget.setMaximumWidth(max_w)
        self.dw_piece_panel_widget.setMaximumHeight(max_h)
        self.dw_piece_panel_widget.setMinimumWidth(min_w)
        self.dw_piece_panel_widget.setMinimumHeight(min_h)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea,
                           self.dw_piece_panel_widget)

        # Main widget -------------------------------------------------------
        self.cw_visualizer = VisVisWidget(self)
        self.setCentralWidget(self.cw_visualizer.widget())

        # Menu --------------------------------------------------------------
        self.menu_main = self.menuBar()
        file_menu = self.menu_main.addMenu('&File')
        file_menu.addAction(self.stl_action)
        file_menu.addAction(self.foam_snappy_action)
        file_menu.addAction(self.foam_cfmesh_action)
        file_menu.addAction(self.txt_action)

        # Status bar --------------------------------------------------------
        self.status_bar = None

    def create_actions(self):
        self.stl_action = QtGui.QAction(
                            QtGui.QIcon(), "&Export mesh to STL",
                            self,
                            statusTip="Exports the current mesh to STL format",
                            triggered=self.export_mesh_stl)

        self.txt_action = QtGui.QAction(
                            QtGui.QIcon(), "&Export mesh to txt",
                            self,
                            statusTip="Exports the information of the mesh" +
                            " to txt format",
                            triggered=self.export_mesh_info_txt)

        self.foam_snappy_action = QtGui.QAction(
                                    QtGui.QIcon(),
                                    "&Create OpenFoam Snappy project",
                                    self,
                                    statusTip="Creates the OpenFoam Snappy" +
                                    "HexMesh Project with default template",
                                    triggered=self.export_mesh_foam_snappy)

        self.foam_cfmesh_action = QtGui.QAction(
                                    QtGui.QIcon(),
                                    "&Create OpenFoam  cfMesh project",
                                    self,
                                    statusTip="Creates the OpenFoam cfMesh" +
                                    " (tetMesh) Project with default template",
                                    triggered=self.export_mesh_foam_cfmesh)

    def export_mesh_stl(self):
        NfluidDataManager.export_mesh_stl()
        self.refresh_visualizer()

    def export_mesh_foam_snappy(self):
        NfluidDataManager.export_mesh_foam_snappy()

    def export_mesh_foam_cfmesh(self):
        NfluidDataManager.export_mesh_foam_cfmesh()

    def export_mesh_info_txt(self):
        NfluidDataManager.export_mesh_info_txt()

    def exit_handler(self):
        self.cw_visualizer.exit_handler()

    def set_selected(self, name):
        self.dw_pieces_list.widget().set_selected(name)
        self.dw_pieces_schema.widget().set_selected(name)
        self.refresh_piece_panel()

    def refresh_visualizer(self):
        mesh = NfluidDataManager.get_total_mesh()
        self.cw_visualizer.set_mesh(mesh)

    def refresh_list_pieces(self):
        self.dw_pieces_list.widget().refresh_gui()

    def refresh_schema_pieces(self):
        self.dw_pieces_schema.widget().refresh_gui()

    def refresh_piece_panel(self):
        self.dw_piece_panel_widget.widget().refresh_gui()

    def refresh_all(self):
        self.refresh_list_pieces()
        self.refresh_visualizer()
        self.refresh_piece_panel()
        self.refresh_schema_pieces()

    def get_current_piece(self):
        # return self.dw_pieces_list.widget().current_piece()
        selected = self.dw_pieces_schema.widget().selected
        if selected is not None:
            piece = Piece()
            piece.set_name(selected)
            return piece
        return None

    def message(self, msg=''):
        msgBox = QtGui.QMessageBox()
        msgBox.setText(msg)
        msgBox.exec_()

    def status_message(self, msg=''):
        self.statusBar().showMessage(msg)

    def ask_for(self, param_type, param_name, msg=''):
        if param_type == Vector:
            vec = QtGui.QInputDialog.getText(self, param_name, msg)
            vec = vec[0].replace(' ', '')
            vec = vec.replace('(', '')
            vec = vec.replace(')', '')
            vec_list = vec.split(',')
            return Vector(float(vec_list[0]),
                          float(vec_list[1]),
                          float(vec_list[2]))
        if param_type == int:
            number = QtGui.QInputDialog.getInt(self, param_name, msg)
            return int(number[0])
        if param_type == float:
            number = QtGui.QInputDialog.getDouble(self, param_name, msg)
            return float(number[0])
        if param_type == bool:
            but = QtGui.QMessageBox.question(self, param_name, msg,
                                             buttons=QtGui.QMessageBox.Yes |
                                             QtGui.QMessageBox.No)
            if but == QtGui.QMessageBox.Yes:
                return True
            return False

    def get_path_save_file(self, ext):
        res = QtGui.QFileDialog.getSaveFileName(filter=ext)
        return res
