import visvis as vv
from visvis import Point, Pointset
import numpy as np


class VisVisWidget(object):

    def __init__(self):
        super(VisVisWidget, self).__init__()
        # self.app = vv.use()
        self._vv_widget = vv.gcf()
        self._vv_widget._widget.show()
        self.create_gui()

    def create_gui(self):
        pass

    def set_mesh(self, mesh):
        vv.clf()
        if mesh:
            v_mesh = mesh.to_visvis_mesh()
            v_mesh.faceColor = 'y'
            v_mesh.edgeShading = 'plain'
            v_mesh.edgeColor = (0, 0, 1)

            axes = vv.gca()
            if axes.daspectAuto is None:
                axes.daspectAuto = False
            axes.SetLimits()
            axes.legend = 'X', 'Y', 'Z'
            axes.axis.showGrid = True
            axes.axis.xLabel = 'X'
            axes.axis.yLabel = 'Y'
            axes.axis.zLabel = 'Z'
        # else:
            # self.test_gui()

    def test_gui(self):
        pp = Pointset(3)
        pp.append(0, 0, 0)
        pp.append(0, 1, 0)
        pp.append(1, 2, 0)
        pp.append(0, 2, 1)

        # Create all solids
        vv.solidBox((0, 0, 0))
        sphere = vv.solidSphere((3, 0, 0))
        cone = vv.solidCone((6, 0, 0))
        # a cone with 4 faces is a pyramid
        pyramid = vv.solidCone((9, 0, 0), N=4)
        vv.solidCylinder((0, 3, 0), (1, 1, 2))
        ring = vv.solidRing((3, 3, 0))
        vv.solidTeapot((6, 3, 0))
        vv.solidLine(pp+Point(9, 3, 0), radius=0.2)

        # Make the ring green
        ring.faceColor = 'g'

        # Make the sphere dull
        sphere.specular = 0
        sphere.diffuse = 0.4

        # Show lines in yellow pyramid
        pyramid.faceColor = 'r'
        pyramid.edgeShading = 'plain'

        # Colormap example
        N = cone._vertices.shape[0]
        cone.SetValues(np.linspace(0, 1, N))
        cone.colormap = vv.CM_JET

    def widget(self):
        return self._vv_widget._widget

    def exit_handler(self):
        vv.close(self._vv_widget)
