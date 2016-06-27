from PySide import QtGui, QtCore
from nfluid.ui.manager import NfluidDataManager


class GeometryToolbar(QtGui.QToolBar):

    def __init__(self, main_win):
        super(GeometryToolbar, self).__init__()
        self._name = "  Geometry toolbar"
        self.main_win = main_win
        self.create_gui()

    def name(self):
        return self._name

    def create_gui(self):
        self.slices_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.slices_slider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.slices_slider.setGeometry(30, 40, 100, 30)
        self.slices_slider.setTickInterval(1)
        self.slices_slider.setMinimum(3)
        self.slices_slider.setMaximum(100)
        self.slices_slider.sliderReleased.connect(self.change_slices)

        self.stacks_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.stacks_slider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.stacks_slider.setGeometry(30, 40, 100, 30)
        self.stacks_slider.setTickInterval(1)
        self.stacks_slider.setMinimum(1)
        self.stacks_slider.setMaximum(100)
        self.stacks_slider.sliderReleased.connect(self.change_stacks)

        self.lcd_slices = QtGui.QLCDNumber()
        self.lcd_stacks = QtGui.QLCDNumber()
        self.slices_slider.valueChanged.connect(self.lcd_slices.display)
        self.stacks_slider.valueChanged.connect(self.lcd_stacks.display)

        self.addWidget(QtGui.QLabel('Slices: '))
        self.addWidget(self.slices_slider)
        self.addWidget(self.lcd_slices)
        self.addWidget(QtGui.QLabel('Stacks: '))
        self.addWidget(self.stacks_slider)
        self.addWidget(self.lcd_stacks)

        current_slices, current_stacks = NfluidDataManager.get_slices_stacks()
        self.slices_slider.setValue(current_slices)
        self.stacks_slider.setValue(current_stacks)

    def change_slices(self):
        current_slices, current_stacks = NfluidDataManager.get_slices_stacks()
        value = self.slices_slider.value()
        if current_slices != value:
            NfluidDataManager.set_slices_stacks(value, current_stacks)
            self.main_win.refresh_visualizer()

    def change_stacks(self):
        current_slices, current_stacks = NfluidDataManager.get_slices_stacks()
        value = self.stacks_slider.value()
        if current_stacks != value:
            NfluidDataManager.set_slices_stacks(current_slices, value)
            self.main_win.refresh_visualizer()
