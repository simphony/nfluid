from nfluid.geometry.geometricmesh import CylindricalPart
from nfluid.geometry.long_elbow import LongElbow


class ShortElbow(CylindricalPart):
    def __init__(self, r, slices, stacks, angle=90):
        super(ShortElbow, self).__init__()
        self.r = r
        self.angle = angle
        part = LongElbow(0, r, slices, stacks, angle)
        self.copy_from_cylindricalpart(part)
