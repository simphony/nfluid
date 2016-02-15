#!/usr/bin/python
# -*- coding: utf-8 -*-
from nfluid.shapes.shapes import CreateShape
from nfluid.core.channel_element_2g import ChannelElement2G
from nfluid.core.gates import GateCircle
from nfluid.util.vector import Vector
from nfluid.util.vector import get_vector_angle_grad
import math
import copy
# Class of ShortElbowNormals


class ShortElbowNormals(ChannelElement2G):

    def __init__(
        self,
        R=None,        # Gate radius
        PosH=None,     # Position of head gate
        PosT=None,     # Position of tail gate
        NormalH=None,  # Normal at head gate
        NormalT=None,  # Normal at tail gate
    ):
        ChannelElement2G.__init__(self)

        self.IsEqualGateSize = True
        self.IsAxialSym = False

        self.heads.append(GateCircle(self))
        self.tails.append(GateCircle(self))

        # TODO Correct NormalT if both NormalH and NormalT are defined
        self.get_head_gate().set_normal_def(copy.copy(NormalH))
        self.get_tail_gate().set_normal_def(copy.copy(NormalT))

        self.get_head_gate().set_pos_def(copy.copy(PosH))
        self.get_tail_gate().set_pos_def(copy.copy(PosT))

        self.get_head_gate().set_size_def(R)
        self.get_tail_gate().set_size_def(R)

        self.angle = None

        self.get_head_gate().PosElement = Vector(0, 0, 0)
        self.get_head_gate().NormalElement = Vector(0, 0, 1)

    def get_name(self):
        return 'ShortElbowNormals'

    def get_r(self):
        return self.get_head_gate().get_r()

    def resolve_geometry_child(self):
        R = self.get_r()
        if self.get_normal_head() is not None and \
           self.get_normal_tail() is not None and \
           R is not None:
            self.angle = get_vector_angle_grad(self.get_normal_head(),
                                               self.get_normal_tail())
            print "resolve_geometry_child angle", self.angle
            self.length = 2*math.pi*R * self.angle/360.0

            self.cos = math.cos(math.radians(self.angle))
            self.sin = math.sin(math.radians(self.angle))
            self.get_tail_gate().PosElement = Vector((self.cos - 1) * R,
                                                     0, self.sin * R)
            self.get_tail_gate().NormalElement = Vector(-self.sin, 0, self.cos)

        return ''

    def print_info(self):
        ChannelElement2G.print_info(self)
        print 'ShortElbowNormals radius Rdef =', \
            self.get_head_gate().get_r_def(), \
            'RH =', self.get_gate_size_h(), 'RT =', self.get_gate_size_t(), \
            'PosH =', self.get_head_gate().Pos, \
            'PosT =', self.get_tail_gate().Pos, \
            'NormH =', self.get_head_gate().NormalElement, \
            'NormT =', self.get_tail_gate().NormalElement

    def create_shape_child(self):
        print 'create_shape ShortElbowNormals'
        return CreateShape('short_elbow_angle', self.CenterPos,
                           self.RotationOperator,
                           self.get_r(), self.angle,
                           self.get_pos_head(), self.get_pos_tail(),
                           self.get_normal_head(), self.get_normal_tail())
