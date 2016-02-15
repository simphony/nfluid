#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
from nfluid.shapes.shapes import CreateShape
from nfluid.core.channel_element_2g import ChannelElement2G
from nfluid.core.gates import GateCircle
from nfluid.util.vector import Vector
from nfluid.geometry.auxiliar_geometry import Arithmetic_Polygon
# Class of FlowAdapter


class FlowAdapter(ChannelElement2G):

    def __init__(
        self,
        RH=None,
        RT=None,
        L=None,
        PosH=None,
        PosT=None,
        Normal=None,
    ):
        ChannelElement2G.__init__(self)

        self.IsAxialSym = True

        self.heads.append(GateCircle(self))
        self.tails.append(GateCircle(self))

        self.length = L
        self.volume = None
        self.set_normal_def(Normal)
        self.get_head_gate().set_pos_def(PosH)
        self.get_tail_gate().set_pos_def(PosT)
        self.get_head_gate().set_size_def(RH)
        self.get_tail_gate().set_size_def(RT)

        # Initial position along Z

        self.get_head_gate().NormalElement = Vector(0, 0, 1)
        self.get_tail_gate().NormalElement = Vector(0, 0, 1)

    def get_name(self):
        return 'FlowAdapter'

    def get_r(self):
        return self.get_head_gate().get_r()

    def get_rh(self):
        return self.get_head_gate().get_r()

    def get_rt(self):
        return self.get_tail_gate().get_r()

    def get_volume(self):
        return self.volume

    def calculate_volume(self):
        slices = ChannelElement2G.slices
        poly_top = Arithmetic_Polygon(self.get_rh(), slices)
        poly_bottom = Arithmetic_Polygon(self.get_rt(), slices)
        l = self.get_len()
        a_t = poly_top.area()
        a_p = poly_bottom.area()
        self.volume = l/3.0 * (a_t + a_p + math.sqrt(a_t * a_p))

    def resolve_geometry_child(self):
        if self.get_len() is not None:
            self.get_head_gate().PosElement = Vector(0, 0,
                                                     -self.get_len() / 2.0)
            self.get_tail_gate().PosElement = Vector(0, 0,
                                                     self.get_len() / 2.0)
        if self.volume is None:
            try:
                self.calculate_volume()
            except:
                pass
        print "-- -- -- THE VOLUME -- -- --", self.volume
        return ''

    def print_info(self):
        ChannelElement2G.print_info(self)
        print 'FlowAdapter RHdef =', self.get_head_gate().get_r_def(), \
            'radiusTail RTdef=', self.get_tail_gate().get_r_def(), \
            'length =', self.length, 'RH =', self.get_gate_size_h(), \
            'RT =', self.get_gate_size_t(), 'PosH =', \
            self.get_pos_head(), 'PosT =', self.get_pos_tail()

    def create_shape_child(self):
        print 'create_shape FlowAdapter'

        # check geometry data

        return CreateShape('flow_adapter', self.CenterPos,
                           self.RotationOperator,
                           self.get_rh(), self.get_rt(),
                           self.get_len(),
                           self.get_pos_head(),
                           self.get_pos_tail(),
                           self.get_normal_head())
