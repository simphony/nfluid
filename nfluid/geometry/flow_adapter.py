from nfluid.geometry.geometricmesh import Circle3D, CylindricalPart


class FlowAdapter(CylindricalPart):
    def __init__(self, r1, r2, l, slices, stacks):
        super(FlowAdapter, self).__init__()
        self.r1 = r1
        self.r2 = r2
        self.l = l
        step = l / ((stacks)*1.0)
        r_step = (r2-r1) / ((stacks)*1.0)
        part = Circle3D(r1, slices)
        for i in xrange(stacks):
            part = part.connect(Circle3D(r1+(i+1)*r_step, slices,
                                pos=(0, 0, (i+1)*step)))
        self.copy_from_cylindricalpart(part)
