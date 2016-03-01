from PySide import QtGui
from nfluid.util.vector import Vector


class ParametersString(object):
    def __init__(self):
        self.head_position = "PosH - position of head"
        self.tail_position = "PosT - position of tail"
        self.tail_position0 = "PosT0 - position of tee tail 0"
        self.tail_position1 = "PosT1 - position of tee tail 1"
        self.head_normal = "NormH - unit vector at head"
        self.tail_normal = "NormT - unit vector at tail"
        self.tail_normal0 = "NormT0 - unit vector for tee tail 0"
        self.tail_normal1 = "NormT1 - unit vector for tee tail 1"
        self.head_radius = "RH - head gate radius"
        self.tail_radius = "RT - tail gate radius"
        self.length = "L  - length"
        self.curvature_radius = "RC - outer elbow radius"
        self.angle = "Angle - elbow and path angle"
        self.sphere_radius = "RS - sphere radius"
        self.points_list = "P - list of points in path"
        self.coupling = "coupling"
        self.flow_adapter = "flow_adapter"
        self.short_elbow_angle = "short_elbow_angle"
        self.long_elbow_angle = "long_elbow_angle"
        self.short_elbow_normals = "short_elbow_normals"
        self.long_elbow_normals = "long_elbow_normals"
        self.spheric_coupling = "spheric_coupling"
        self.circle_path = "circle_path"
        self.tee = "tee"
        self.cap = "cap"
        self.gate = "Gate"

strings = ParametersString()


class WidgetParameterNumber(QtGui.QWidget):
    def __init__(self, name, value):
        super(WidgetParameterNumber, self).__init__()
        self._name = name
        self._value = value
        self.create_gui()

    def name(self):
        return self._name

    def value(self):
        self._value = float(self.value_widget.text())
        return self._value

    def setValue(self, value):
        self._value = value
        self.value_widget = str(value)

    def create_gui(self):
        self.layout = QtGui.QHBoxLayout()
        self.name_widget = QtGui.QLabel(self._name)
        self.value_widget = QtGui.QLineEdit()
        self.value_widget.setText(str(self._value))
        self.layout.addWidget(self.name_widget)
        self.layout.addWidget(self.value_widget)
        self.setLayout(self.layout)


class WidgetParameterVector(QtGui.QWidget):
    def __init__(self, name, value):
        super(WidgetParameterVector, self).__init__()
        self._name = name
        self._value = value
        self.create_gui()

    def name(self):
        return self._name

    def value(self):
        x = self.x_widget.value()
        y = self.y_widget.value()
        z = self.z_widget.value()
        self._value = Vector(x, y, z)
        return self._value

    def set_value(self, value):
        self._value = value
        self.x_widget.set_value(value[0])
        self.y_widget.set_value(value[1])
        self.z_widget.set_value(value[2])

    def create_gui(self):
        self.layout = QtGui.QHBoxLayout()
        self.name_widget = QtGui.QLabel(self._name)
        self.x_widget = WidgetParameterNumber('X', 0)
        self.y_widget = WidgetParameterNumber('Y', 0)
        self.z_widget = WidgetParameterNumber('Z', 0)
        self.layout.addWidget(self.name_widget)
        self.layout.addWidget(self.x_widget)
        self.layout.addWidget(self.y_widget)
        self.layout.addWidget(self.z_widget)
        self.setLayout(self.layout)


class WidgetParameterList(QtGui.QWidget):
    def __init__(self, name, value):
        super(WidgetParameterList, self).__init__()
        self._name = name
        self._value = [] #... value
        self.create_actions()
        self.create_gui()

    def name(self):
        return self._name

    def value(self):
        # self._value = ...
        return [(0,0,0),(5,0,0),(5,0,5)]

    def setValue(self, value):
        self._value = value
        # ...

    def create_actions(self):
        self.add_point_action = QtGui.QAction(QtGui.QIcon(), "&Add Point",
                                        self, statusTip="Add a new point",
                                        triggered=self.add_current_point)

    def create_gui(self):
        self.layout = QtGui.QVBoxLayout()
        self.name_widget = QtGui.QLabel(self._name)
        self._value_widget = QtGui.QListWidget(self)
        self.layout.addWidget(self.name_widget)
        self.items_layout = QtGui.QHBoxLayout()
        self.items_layout.addWidget(self._value_widget)
        
        self.options_layout = QtGui.QVBoxLayout()
        self.point_widget = WidgetParameterVector("Point", (0,0,0))
        self.add_point_button = QtGui.QPushButton("Add Point", parent=self)
        self.add_point_button.clicked.connect(self.add_point_action.triggered)

        self.remove_point_button = QtGui.QPushButton("Remove Point", parent=self)
        self.remove_point_button.clicked.connect(self.remove_point_action.triggered)

        self.remove_all_button = QtGui.QPushButton("Remove All", parent=self)
        self.remove_all_button.clicked.connect(self.remove_all_action.triggered)

        self.options_layout.addWidget(self.point_widget)
        self.options_layout.addWidget(self.add_point_button)
        self.options_layout.addWidget(self.remove_point_button)
        self.options_layout.addWidget(self.remove_all_button)

        self.items_layout.addWidget(self.options_layout)

        self.layout.addWidget(self.item_layout)

    def add_current_point(self):
        pass

    def remove_current_point(self):
        pass

    def remove_all_points(self):
        pass

class WidgetNewPiece(QtGui.QWidget):

    def __init__(self, name, params):
        super(WidgetNewPiece, self).__init__()
        self.parameters = list(params)
        self._name = name
        self.create_gui()

    def get_param(self, name):
        for elem in self.parameters:
            if elem[0] == name:
                for index in xrange(self.layout.count()):
                    cur_widget = self.layout.itemAt(index).widget()
                    if cur_widget.name() == name:
                        return cur_widget.value()
        return None

    def name(self):
        return self._name

    def create_gui(self):
        self.layout = QtGui.QVBoxLayout()
        for par in self.parameters:
            # if hasattr(par[1], '__iter__'):
            if isinstance(par[1], tuple):
                new_param = WidgetParameterVector(par[0], par[1])
            elif isinstance(par[1], list):
                new_param = WidgetParameterList(par[0], par[1])
            else:
                new_param = WidgetParameterNumber(par[0], par[1])

            self.layout.addWidget(new_param)

        self.setLayout(self.layout)
