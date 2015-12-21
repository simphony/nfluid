from nfluid.geometry.geometricmesh import Circle3D, CylindricalPart
from nfluid.geometry.functions import cos_table, sin_table
import numpy as np
from nfluid.external.transformations import unit_vector
from nfluid.external.transformations import vector_product


class LongElbow(CylindricalPart):
    def __init__(self, r1, r2, slices, stacks, angle=90):
        super(LongElbow, self).__init__()
        print "r1"
        print r1
        print "r2"
        print r2
        print "slices"
        print slices
        print "stacks"
        print stacks
        print "angle"
        print angle
        self.r1 = r1
        self.r2 = r2
        self.angle = angle
        cos_t = cos_table(stacks, np.radians(angle))
        sin_t = sin_table(stacks, np.radians(angle))
        v1 = (1, 0, 0)
        part = None
        for i in xrange(len(sin_t)):
            c_sin = sin_t[i]
            c_cos = cos_t[i]
            cur_pos = (0, c_cos * r2 + c_cos * r1, c_sin * r2 + c_sin * r1)
            v2 = unit_vector(cur_pos)
            cur_n = unit_vector(vector_product(v1, v2))
            circle = Circle3D(r2, slices, pos=cur_pos, normal=cur_n)
            if part is not None:
                part = part.connect(circle)
            else:
                part = circle
        self.copy_from_cylindricalpart(part)
