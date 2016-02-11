#!/usr/bin/python
# -*- coding: utf-8 -*-
from nfluid.shapes.shapes import CreateShape
from nfluid.core.channel_element import ChannelElement
from nfluid.core.gates import GateCircle
from nfluid.util.vector import Vector


class CircleTee(ChannelElement):

    def __init__(
        self,
        R=None,
        PosH=None,
        PosT0=None,
        PosT1=None,
        NormalH=None,
        NormalT0=None,
        NormalT1=None,
    ):

        # NormalH, NormalT0 must be orthogonal
        # NormalT should be corrected to respect that

        ChannelElement.__init__(self)

        self.IsEqualGateSize = True

        self.length = R

        self.heads.append(GateCircle(self))
        self.tails.append(GateCircle(self))
        self.tails.append(GateCircle(self))

        self.get_head_gate().set_size_def(R)
        self.get_tail_gate(0).set_size_def(R)
        self.get_tail_gate(1).set_size_def(R)

        self.get_head_gate().set_pos_def(PosH)
        self.get_tail_gate(0).set_pos_def(PosT0)
        self.get_tail_gate(1).set_pos_def(PosT1)

        self.get_head_gate().set_normal_def(NormalH)
        self.get_tail_gate(0).set_normal_def(NormalT0)
        self.get_tail_gate(1).set_normal_def(NormalT1)

        # Initial position along Z and X

        self.get_head_gate().NormalElement = Vector(0, 0, 1)
        self.get_tail_gate(0).NormalElement = Vector(1, 0, 0)
        self.get_tail_gate(1).NormalElement = Vector(-1, 0, 0)

    def get_name(self):
        return 'CircleTee'

    def get_gate_size_h(self, n=0):
        return self.get_head_gate().Size[n]

    def set_gate_size_h(
        self,
        s0,
        s1=None,
        s2=None,
        s3=None,
    ):
        return self.get_head_gate().set_size_arg(s0, s1, s2, s3)

    def get_r(self):
        return self.get_head_gate().get_r()

    def get_len(self):
        return self.length

    def resolve_geometry_child(self):

        R = self.get_r()
        if R is not None:
            self.get_head_gate().PosElement = Vector(0, 0, -R)
            self.get_tail_gate(0).PosElement = Vector(R, 0, 0)
            self.get_tail_gate(1).PosElement = Vector(-R, 0, 0)

        return ''

    def create_shape_child(self):
        # check geometry data
        print 'create_shape CircleTee'

        return CreateShape('circle_tee', self.CenterPos, self.RotationOperator,
                           self.get_head_gate().get_r(),
                           self.get_pos_head(), self.get_pos_tail(0),
                           self.get_pos_tail(1), self.get_head_gate(0).Normal,
                           self.get_tail_gate(0).Normal)
