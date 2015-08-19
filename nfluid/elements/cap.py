#!/usr/bin/python
# -*- coding: utf-8 -*-

from nfluid.core.channel_element_2g import *
from nfluid.core.gates import *


# Class of Cap

class Cap(ChannelElement):

    def __init__(
        self,
        L,
        R=None,
        PosH=None,
        NormalH=None,
    ):
        ChannelElement.__init__(self)

        self.IsAxialSym = True

        self.length = L

        self.heads.append(GateCircle(self))

        self.get_head_gate().set_normal_def(NormalH)

        self.get_head_gate().set_pos_def(PosH)

        self.get_head_gate().set_size_def(R)

        self.get_head_gate().NormalElement = Vector(0, 0, 1)
        self.get_head_gate().PosElement = Vector(0, 0, 0)

    def get_name(self):
        return 'Cap'

    def get_r(self):
        return self.get_head_gate().get_r()

    def resolve_geometry_child(self):
        if self.get_r() is None:
            return ''
        if self.get_r() < self.length:
            return 'Incorrect Cup length'
        else:
            return ''

    def print_info(self):
        ChannelElement.print_info(self)
        print 'Cap radius Rdef =', self.get_head_gate().get_r_def(), \
              'R =', self.get_head_gate().get_r()

    def create_shape(self):

        # check geometry data

        self.shape = ShapeCap(self.get_head_gate().get_r(),
                              self.length, 0)

        print 'create_shape Cap'
        return ''
