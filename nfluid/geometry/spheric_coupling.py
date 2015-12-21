from nfluid.geometry.geometricmesh import Circle3D, CylindricalPart
from nfluid.external.transformations import vector_norm
from nfluid.geometry.functions import cos_table, sin_table
import math


class SphericCoupling(CylindricalPart):
    def __init__(self, r, R, slices, stacks):
        super(SphericCoupling, self).__init__()
        self.r = r
        self.R = R
        l = math.sqrt(R*R - r*r)
        top = Circle3D(r, slices, pos=(0, 0, l))
        bottom = Circle3D(r, slices, pos=(0, 0, -l))
        p1 = top.vertex(0)
        sphere_r = vector_norm(p1)
        cos_t = cos_table(stacks, angle=math.pi)[::-1]
        sin_t = sin_table(stacks, angle=math.pi)[::-1]
        part = bottom
        for i in xrange(stacks):
            c_sin = sin_t[i]
            c_cos = cos_t[i]
            cur_r = abs(sphere_r * c_sin)
            cur_pos = (0, 0, -c_cos*sphere_r)
            if cur_r > r:
                circle = Circle3D(cur_r, slices, pos=cur_pos)
                part = part.connect(circle)
        part = part.connect(top)
        self.copy_from_cylindricalpart(part)
