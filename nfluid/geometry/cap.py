from nfluid.geometry.geometricmesh import Circle3D, CylindricalPart, Arc3D
from nfluid.geometry.functions import cos_table, sin_table
import numpy as np


class Cap(CylindricalPart):
    def __init__(self, r, l, slices, stacks):
        super(Cap, self).__init__()
        self.r = r
        self.l = l
        # circle = Circle3D(r, slices)
        # point = (0, 0, l)
        rs = (r * r + l * l) / (2 * (l + 0.00001))
        p1 = (0, r, rs - l)
        p2 = (0, 0, rs)
        arc = Arc3D(stacks, p1, p2, (0,0,0))
        n_vertices = arc.n_vertices()
        factor = rs - l
        part = None
        for i in xrange(n_vertices - 1):
            v = arc.vertex(i)
            new_v = (0, 0, v[2] - factor)
            new_r = v[1]
            print " --- --- --- new_r"
            print new_r
            new_circle = Circle3D(new_r, slices, pos=new_v)
            if part is None:
                part = new_circle
            else:
                part = part.connect(new_circle)
        v = arc.vertex(n_vertices-1)
        mid_point = (0, 0, v[2] - factor)
        part = part.connect(mid_point)
        self.copy_from_cylindricalpart(part)

    # def __init__(self, r, l, slices, stacks):
        # super(Cap, self).__init__()
        # self.r = r
        # self.l = l
        # circle = Circle3D(r, slices)
        # point = (0, 0, l)
        # part = circle.connect(point)
        # self.copy_from_cylindricalpart(part)
