from nfluid.geometry.geometricmesh import Circle3D, CylindricalPart


class Coupling(CylindricalPart):
    def __init__(self, r, l, slices, stacks):
        super(Coupling, self).__init__()
        self.r = r
        self.l = l
        step = l / ((stacks-1)*1.0)
        part = Circle3D(r, slices)
        for i in xrange(stacks):
            part = part.connect(Circle3D(r, slices, pos=(0, 0, (i+1)*step)))
        self.copy_from_cylindricalpart(part)
