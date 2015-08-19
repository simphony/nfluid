#!/usr/bin/python
# -*- coding: utf-8 -*-

from nfluid.core.channel_element_2g import *
from nfluid.core.gates import *


# Class of Elbow

class ShortElbow(ChannelElement2G):

    def __init__(
        self,
        R=None,
        PosH=None,
        PosT=None,
        NormalH=None,
        NormalT=None,
    ):
        ChannelElement2G.__init__(self)

        self.IsEqualGateSize = True

        self.heads.append(GateCircle(self))
        self.tails.append(GateCircle(self))

        self.angle = 90  # Could vary in future

        # TODO Correct NormalT if both NormalH and NormalT are defined

        self.get_head_gate().set_normal_def(NormalH)
        self.get_tail_gate().set_normal_def(NormalT)

        self.get_head_gate().set_pos_def(PosH)
        self.get_tail_gate().set_pos_def(PosT)

        self.get_head_gate().set_size_def(R)
        self.get_tail_gate().set_size_def(R)

        # Initial position along Z and X

        self.get_head_gate().NormalElement = Vector(0, 0, 1)
        self.get_tail_gate().NormalElement = Vector(1, 0, 0)

    def get_name(self):
        return 'ShortElbow'

    def get_r(self):
        return self.get_head_gate().get_r()

    def get_r_curv(self):
        return self.get_head_gate().get_r()

    def resolve_geometry_child(self):

        R = self.get_r()
        if R is not None:
            self.get_head_gate().PosElement = Vector(0, 0, -R)
            self.get_tail_gate().PosElement = Vector(R, 0, 0)
        return ''

    def print_info(self):
        ChannelElement2G.print_info(self)
        print 'ShortElbow radius Rdef =', \
            self.get_head_gate().get_r_def(), 'RH =', \
            self.get_gate_size_h(), 'RT =', self.get_gate_size_t(), \
            'PosH =', self.get_pos_head(), 'PosT =', self.get_pos_tail()

    def create_shape(self):

        # check geometry data

        self.shape = ShapeShortElbow(self.get_r(), self.get_pos_head(),
                                     self.get_pos_tail())
        print 'create_shape ShortElbow'
        return ''
