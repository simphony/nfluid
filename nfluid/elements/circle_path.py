#!/usr/bin/python
# -*- coding: utf-8 -*-
from nfluid.shapes.shapes import CreateShape
from nfluid.core.channel_element_2g import ChannelElement2G
from nfluid.core.gates import GateCircle
from nfluid.util.vector import is_colinear
from nfluid.util.rotations import GetRotationMatrixAxisAngleGrad
from nfluid.geometry.auxiliar_geometry import Arithmetic_Polygon
import copy
# Class of CirclePath


class CirclePath(ChannelElement2G):

    def __init__(
        self,
        Points,        # List of points as Vectors
        R=None,        # Gate radius
        PosH=None,     # Position of head gate
        PosT=None,     # Position of tail gate
        NormalH=None,  # Normal at head gate
        NormalT=None,  # Normal at tail gate
        Twist=None,    # Extra parameter (if Normals are collinear)
    ):
    """
    Parameters
    ----------
    R : real
        the radius of the full piece
    Points : iterable
        the points defining the shape of the piece
    PosH : Vector
        the position of the center of the head
    PosT : Vector
        the position of the center of the tail
    NormalH : Vector
        normal vector of the head
    NormalT : Vector
        normal vector of the tail
    Twist : real
        extra parameter indicating a second rotation when the piece is ambiguous

    """
        ChannelElement2G.__init__(self)

        self.IsEqualGateSize = True

        # COLLINEAR CONDITION TO CHECK FOR AXIAL SYMMETRY
        # SHOULD BE SOMETHING LIKE THIS:
        # NormHeadFromPoints = (Points[1]-Points[0]).normalize()
        # NormTailFromPoints = (Points[-1]-Points[-2]).normalize()
        # NormHeadToTailFromPoints = (Points[-1]-Points[0]).normalize()
        # if is_colinear(NormHeadFromPoints, NormTailFromPoints) and \
        #    is_colinear(NormHeadFromPoints, NormHeadToTailFromPoints):
        #     self.IsAxialSym = True
        # else:
        #     self.IsAxialSym = False

        # BUT, WHAT ACTUALLY WORKS IS THIS:
        NormHeadFromPoints = (Points[1]-Points[0]).normalize()
        NormTailFromPoints = (Points[-1]-Points[-2]).normalize()
        if is_colinear(NormHeadFromPoints, NormTailFromPoints):
            self.IsAxialSym = True
        else:
            self.IsAxialSym = False

        Length = 0.0
        for Point in range(1, len(Points)):
            Length += (Points[Point]-Points[Point-1]).get_len()
        self.length = Length
        self.volume = None

        self.heads.append(GateCircle(self))
        self.tails.append(GateCircle(self))

        self.get_head_gate().set_normal_def(copy.copy(NormalH))
        self.get_tail_gate().set_normal_def(copy.copy(NormalT))

        self.get_head_gate().set_pos_def(copy.copy(PosH))
        self.get_tail_gate().set_pos_def(copy.copy(PosT))

        self.get_head_gate().set_size_def(R)
        self.get_tail_gate().set_size_def(R)

        self.angle = Twist
        self.InputPoints = copy.copy(Points)

        # Initial Normals
        self.get_head_gate().NormalElement = copy.copy(
            (Points[1]-Points[0]).normalize())
        self.get_tail_gate().NormalElement = copy.copy(
            (Points[-1]-Points[-2]).normalize())

        # Initial Positions
        self.get_head_gate().PosElement = copy.copy(Points[0])
        self.get_tail_gate().PosElement = copy.copy(Points[-1])

        PosH = self.get_pos_head()
        PosT = self.get_pos_tail()
        if PosH.is_not_none() and PosT.is_none():
            VectorFromHeadToTail = (self.InputPoints[-1]-self.InputPoints[0])
            self.get_tail_gate().Pos = PosH + VectorFromHeadToTail

        # Try put center in the first point
        # centroid = Vector(0.0, 0.0, 0.0)
        # for Point in Points:
        #    centroid += Point
        # centroid = centroid/len(Points)
        # self.get_head_gate().PosElement = copy.copy(Points[0]-centroid)
        # self.get_tail_gate().PosElement = copy.copy(Points[-1]-centroid)

    def get_name(self):
        return 'CirclePath'

    def get_r(self):
        return self.get_head_gate().get_r()

    def get_volume(self):
        return self.volume

    def get_points(self):
        return self.InputPoints

    def calculate_volume(self):
        slices = ChannelElement2G.slices
        vol = 0.0
        r = self.get_r()
        for i in range(1, len(self.InputPoints)):
            l = (self.InputPoints[i]-self.InputPoints[i-1]).get_len()
            vol += Arithmetic_Polygon(r, slices).area() * l
        self.volume = vol

    def resolve_geometry_child(self):
        if self.volume is None:
            try:
                self.calculate_volume()
            except:
                pass
        print "-- -- -- THE VOLUME -- -- --", self.volume
        return ''

    def print_info(self):
        ChannelElement2G.print_info(self)
        print 'CirclePath radius Rdef =', self.get_head_gate().get_r_def(), \
            'RH =', self.get_gate_size_h(), 'RT =', self.get_gate_size_t(), \
            'PosH =', self.get_head_gate().Pos, \
            'PosT =', self.get_tail_gate().Pos

    def create_shape_child(self):
        print 'create_shape CirclePath'
        print "self.CenterPos"
        print self.CenterPos
        print "self.RotationOperator"
        print self.RotationOperator
        # Compute new Points: shift + rotation
        RPoints = []
        for Point in self.InputPoints:
            print Point
            RPoint = self.CenterPos + self.RotationOperator * Point
            RPoints.append(RPoint)

        # Add extra rotation if collinear case and Twist is provided
        if self.IsAxialSym and self.angle is not None:
            axis = (RPoints[1]-RPoints[0]).normalize()
            TwistRotation = GetRotationMatrixAxisAngleGrad(axis, self.angle)
            origin = RPoints[0]
            APoints = []
            for Point in RPoints:
                APoint = origin + TwistRotation * (Point-origin)
                APoints.append(APoint)
            RPoints = APoints
            del APoints

        # Convert from Vector type
        OutputPoints = []
        for Point in RPoints:
            OutputPoints.append((Point.x, Point.y, Point.z))

        return CreateShape('circle_path', self.CenterPos,
                           self.RotationOperator,
                           self.get_r(), OutputPoints,
                           self.get_pos_head(), self.get_pos_tail(),
                           self.get_normal_head(), self.get_normal_tail())
