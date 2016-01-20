from PySide import QtCore, QtGui
from nfluid.core.channel_assembly import ChannelAssembly
from nfluid.core.channel_element import ChannelElement


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
        self.angle = "Angle - elbow angle"
        self.sphere_radius = "RS - sphere radius"
        self.points_list = "P - list of points in path"

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
        self._value = (x, y, z)
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
                    if cur_widget.name() ==  name:
                        return cur_widget.value()
        return None

    def name(self):
        return self._name

    def create_gui(self):
        self.layout = QtGui.QVBoxLayout()
        for par in self.parameters:
            if hasattr(par[1], '__iter__'):
                new_param = WidgetParameterVector(par[0], par[1])
            else:
                new_param = WidgetParameterNumber(par[0], par[1])
                
            self.layout.addWidget(new_param)
        
        self.setLayout(self.layout)
        