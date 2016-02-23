from PySide import QtCore, QtGui
from nfluid.ui.elements.creationpieceswidget import CreationPiecesWidget
from nfluid.ui.elements.listpieceswidget import ListPiecesWidget
from nfluid.ui.elements.schemapieceswidget import SchemaPiecesWidget
from nfluid.ui.elements.visualizer import VisVisWidget
from nfluid.ui.manager import NfluidDataManager
from nfluid.util.vector import Vector


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.create_actions()
        self.create_gui()
        self.refresh_all()

    def create_gui(self):
        self.dw_pieces_creation = QtGui.QDockWidget()
        cur_widget = CreationPiecesWidget(self)
        self.dw_pieces_creation.setWidget(cur_widget)
        self.dw_pieces_creation.setFeatures(
                    QtGui.QDockWidget.NoDockWidgetFeatures)
        title = QtGui.QLabel(cur_widget.name())
        self.dw_pieces_creation.setTitleBarWidget(title)

        self.dw_pieces_list = QtGui.QDockWidget()
        cur_widget = ListPiecesWidget(self)
        self.dw_pieces_list.setWidget(cur_widget)
        self.dw_pieces_list.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        title = QtGui.QLabel(cur_widget.name())
        self.dw_pieces_list.setTitleBarWidget(title)

        self.dw_pieces_schema = QtGui.QDockWidget()
        cur_widget = SchemaPiecesWidget(self)
        self.dw_pieces_schema.setWidget(cur_widget)
        self.dw_pieces_schema.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        title = QtGui.QLabel(cur_widget.name())
        self.dw_pieces_schema.setTitleBarWidget(title)

        self.cw_visualizer = VisVisWidget()

        self.menu_main = self.menuBar()
        file_menu = self.menu_main.addMenu('&File')
        file_menu.addAction(self.stl_action)
        file_menu.addAction(self.foam_snappy_action)
        file_menu.addAction(self.foam_cfmesh_action)
        file_menu.addAction(self.txt_action)

        self.status_bar = None

        self.min_h = 100
        self.min_w = 100
        self.max_h = 350
        self.max_w = 500

        self.dw_pieces_creation.setMaximumWidth(self.max_w)
        self.dw_pieces_creation.setMaximumHeight(self.max_h)
        self.dw_pieces_creation.setMinimumWidth(self.min_w)
        self.dw_pieces_creation.setMinimumHeight(self.min_h)

        self.dw_pieces_list.setMaximumWidth(self.max_w)
        self.dw_pieces_list.setMaximumHeight(self.max_h)
        self.dw_pieces_list.setMinimumWidth(self.min_w)
        self.dw_pieces_list.setMinimumHeight(self.min_h)

        self.dw_pieces_schema.setMaximumWidth(self.max_w)
        self.dw_pieces_schema.setMaximumHeight(self.max_h)
        self.dw_pieces_schema.setMinimumWidth(self.min_w)
        self.dw_pieces_schema.setMinimumHeight(self.min_h)        

        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea,
                           self.dw_pieces_creation)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dw_pieces_list)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dw_pieces_schema)
        self.setCentralWidget(self.cw_visualizer.widget())

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

    def export_mesh_foam_snappy(self):
        NfluidDataManager.export_mesh_foam_snappy()

    def export_mesh_foam_cfmesh(self):
        NfluidDataManager.export_mesh_foam_cfmesh()

    def export_mesh_info_txt(self):
        NfluidDataManager.export_mesh_info_txt()

    def exit_handler(self):
        self.cw_visualizer.exit_handler()

    def refresh_visualizer(self):
        mesh = NfluidDataManager.get_total_mesh()
        self.cw_visualizer.set_mesh(mesh)

    def refresh_list_pieces(self):
        self.dw_pieces_list.widget().refresh_gui()

    def refresh_schemea_pieces(self):
        self.dw_pieces_schema.widget().refresh_gui()

    def refresh_all(self):
        self.refresh_list_pieces()
        self.refresh_visualizer()

    def message(self, msg=''):
        msgBox = QtGui.QMessageBox()
        msgBox.setText(msg)
        msgBox.exec_()

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
            return None
        if param_type == bool:
            but = QtGui.QMessageBox.question(self, param_name, msg,
                                             buttons=QtGui.QMessageBox.Yes |
                                             QtGui.QMessageBox.No)
            if but == QtGui.QMessageBox.Yes:
                print "R E T U R N E D True"
                return True
            print "R E T U R N E D False"
            return False

    def get_path_save_file(self, ext):
        res = QtGui.QFileDialog.getSaveFileName(filter=ext)
        return res
