#!/usr/bin/python
# -*- coding: utf-8 -*-
from nfluid.shapes.shapes import CreateShape
from nfluid.core.channel_element_2g import ChannelElement2G
from nfluid.core.gates import GateCircle
from nfluid.util.vector import Vector
import copy
# Class of CirclePath


class CirclePath(ChannelElement2G):

    def __init__(
        self,
        Points,        # List of elements as Vectors
        R=None,        # Gate radius
        PosH=None,     # Position of head gate
        PosT=None,     # Position of tail gate
        NormalH=None,  # Normal at head gate
        NormalT=None,  # Normal at tail gate
        Angle=None,    # Extra angle (if Normals are collinear)
    ):
        ChannelElement2G.__init__(self)

        self.IsEqualGateSize = True

        # self.length = (Points[-1]-Points[0]).get_len()

        self.heads.append(GateCircle(self))
        self.tails.append(GateCircle(self))

        self.get_head_gate().set_normal_def(copy.copy(NormalH))
        self.get_tail_gate().set_normal_def(copy.copy(NormalT))

        self.get_head_gate().set_pos_def(copy.copy(PosH))
        self.get_tail_gate().set_pos_def(copy.copy(PosT))

        self.get_head_gate().set_size_def(R)
        self.get_tail_gate().set_size_def(R)

        self.angle = Angle
        self.InputPoints = copy.copy(Points)

        # Initial Normals
        self.get_head_gate().NormalElement = copy.copy((Points[1]-Points[0]).normalize())
        self.get_tail_gate().NormalElement = copy.copy((Points[-1]-Points[-2]).normalize())

        # Initial Positions
        self.get_head_gate().PosElement = copy.copy(Points[0])
        self.get_tail_gate().PosElement = copy.copy(Points[-1])

        # Try put center in the first point
        # centroid = Vector(0.0, 0.0, 0.0)
        # for Point in Points:
            # centroid += Point
        # centroid = centroid/len(Points)
        # print 'centroid = ',centroid
        # self.get_head_gate().PosElement = copy.copy(Points[0]-centroid)
        # self.get_tail_gate().PosElement = copy.copy(Points[-1]-centroid)

        # print 'self.get_head_gate().PosElement = ',self.get_head_gate().PosElement
        # print 'self.get_tail_gate().PosElement = ',self.get_tail_gate().PosElement

    def get_name(self):
        return 'CirclePath'

    def get_r(self):
        return self.get_head_gate().get_r()

    def resolve_geometry_child(self):
        return ''

    def print_info(self):
        ChannelElement2G.print_info(self)
        print 'CirclePath radius Rdef =', self.get_head_gate().get_r_def(), \
            'RH =', self.get_gate_size_h(), 'RT =', self.get_gate_size_t(), \
            'PosH =', self.get_head_gate().Pos, 'PosT =', self.get_tail_gate().Pos

    def create_shape_child(self):
        print 'create_shape CirclePath'

        # Compute new Points: shift + rotation
        OutputPoints = []
        for Point in self.InputPoints:
            # print ' Point=',Point
            RPoint = self.CenterPos + self.RotationOperator * Point
            # print 'RPoint=',RPoint
            OutputPoints.append((RPoint.x, RPoint.y, RPoint.z))
        # Check result
        # print 'OutputPoints = ',OutputPoints

        return CreateShape('circle_path', self.CenterPos, self.RotationOperator,
                           self.get_r(), OutputPoints,
                           self.get_pos_head(), self.get_pos_tail(),
                           self.get_normal_head(), self.get_normal_tail())

