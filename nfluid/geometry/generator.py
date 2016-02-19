from nfluid.geometry.coupling import Coupling
from nfluid.geometry.short_elbow import ShortElbow
from nfluid.geometry.long_elbow import LongElbow
from nfluid.geometry.flow_adapter import FlowAdapter
from nfluid.geometry.spheric_coupling import SphericCoupling
from nfluid.geometry.cap import Cap
from nfluid.geometry.tee import Tee
from nfluid.geometry.coupling_path import CouplingPath


class GeometryGenerator():
    """Class to create and generate the vertices, normals and triangles of
    the different pieces of nfluid.
    """

    def __init__(self, slices=30, stacks=15):
        # STUB!!!!
        self.slices = slices
        self.stacks = stacks
        # self.slices = 4
        # self.stacks = 1

    def create_coupling(self, r, l):
        return Coupling(r, l, self.slices, self.stacks)

    def create_short_elbow(self, r, angle=90):
        return ShortElbow(r, self.slices, self.stacks, angle)

    def create_long_elbow(self, r1, r2, angle=90):
        return LongElbow(r1, r2, self.slices, self.stacks, angle)

    def create_flow_adapter(self, r1, r2, l):
        return FlowAdapter(r1, r2, l, self.slices, self.stacks)

    def create_spheric_coupling(self, r, R):
        return SphericCoupling(r, R, self.slices, self.stacks)

    def create_cap(self, r, l):
        return Cap(r, l, self.slices, self.stacks)
        # return Coupling(r, l, self.slices, self.stacks)

    def create_tee(self, r):
        return Tee(r, self.slices, self.stacks)

    def create_coupling_path(self, r, points):
        return CouplingPath(r, points, self.slices, self.stacks)
