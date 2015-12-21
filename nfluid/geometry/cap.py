from nfluid.geometry.geometricmesh import Circle3D, CylindricalPart


class Cap(CylindricalPart):
    def __init__(self, r, l, slices, stacks):
        super(Cap, self).__init__()
        self.r = r
        self.l = l
        circle = Circle3D(r, slices)
        point = (0, 0, l)
        part = circle.connect(point)
        self.copy_from_cylindricalpart(part)
