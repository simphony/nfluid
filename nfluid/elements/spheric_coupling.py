#!/usr/bin/python
# -*- coding: utf-8 -*-
from nfluid.shapes.shapes import CreateShape
from nfluid.core.channel_element_2g import ChannelElement2G
from nfluid.core.gates import GateCircle
from nfluid.util.vector import Vector
from nfluid.geometry.auxiliar_geometry import Arithmetic_Polygon
import math
# Class of SphericCoupling


class SphericCoupling(ChannelElement2G):

    def __init__(
        self,
        RS,
        R=None,
        PosH=None,
        PosT=None,
        Normal=None
    ):
        ChannelElement2G.__init__(self)

        self.IsEqualGateSize = True

        self.heads.append(GateCircle(self))
        self.tails.append(GateCircle(self))

        self.RadiusSphere = RS
        self.IsAxialSym = True

        self.volume = None

        self.set_normal_def(Normal)

        self.get_head_gate().set_pos_def(PosH)
        self.get_tail_gate().set_pos_def(PosT)

        self.get_head_gate().set_size_def(R)
        self.get_tail_gate().set_size_def(R)

        # Initial position along Z

        self.get_head_gate().NormalElement = Vector(0, 0, 1)
        self.get_tail_gate().NormalElement = Vector(0, 0, 1)

    def get_name(self):
        return 'SphericCoupling'

    def get_r(self):
        return self.get_head_gate().get_r()

    def get_volume(self):
        return self.volume

    def calculate_volume(self):
        slices = ChannelElement2G.slices
        poly_top = Arithmetic_Polygon(self.get_r(), slices)
        poly_bottom = Arithmetic_Polygon(self.RadiusSphere, slices)
        l = self.get_len()
        a_t = poly_top.area()
        a_p = poly_bottom.area()
        v = l/3.0 * (a_t + a_p + math.sqrt(a_t * a_p))
        self.volume = v * 2.0

    def resolve_geometry_child(self):
        if self.get_r() is not None:
            if self.get_r() > self.RadiusSphere:
                return 'Incorrect Sphere radius'

            length = math.sqrt(self.RadiusSphere ** 2 -
                               self.get_r() ** 2)

            self.get_head_gate().PosElement = Vector(0, 0, -length)
            self.get_tail_gate().PosElement = Vector(0, 0, length)

            self.length = length * 2

        if self.volume is None:
            try:
                self.calculate_volume()
            except:
                pass
        print "-- -- -- THE VOLUME -- -- --", self.volume

        return ''

    def print_info(self):
        ChannelElement2G.print_info(self)
        print 'SphericCoupling radius Rdef =', \
            self.get_head_gate().get_r_def(), 'RH =', \
            self.get_gate_size_h(), 'RT =', self.get_gate_size_t(), \
            'RadiusSphere =', self.RadiusSphere, 'PosH = ', \
            self.get_pos_head(), 'PosT =', self.get_pos_tail()

    def create_shape_child(self):
        print 'create_shape SphericCoupling'
        # check geometry data

        return CreateShape('spheric_coupling', self.CenterPos,
                           self.RotationOperator,
                           self.RadiusSphere,
                           self.get_r(),
                           self.get_pos_head(),
                           self.get_pos_tail(),
                           self.get_normal_head())
