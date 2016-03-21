#!/usr/bin/python
# -*- coding: utf-8 -*-
from nfluid.shapes.shapes import CreateShape
from nfluid.core.channel_element_2g import ChannelElement2G
from nfluid.core.gates import GateCircle
from nfluid.util.vector import Vector
from nfluid.geometry.auxiliar_geometry import Arithmetic_Polygon
# Class of CircleCoupling


class CircleCoupling(ChannelElement2G):
    """Class representing a cylindrical element with one head and one tail.

    """
    def __init__(
        self,
        R=None,
        L=None,
        PosH=None,
        PosT=None,
        Normal=None
    ):
        """
        Parameters
        ----------
        R : real
            the radius of the cylinder
        L : real
            the length of the cylinder
        PosH : Vector
            the position of the center of the head
        PosT : Vector
            the position of the center of the tail
        Normal : Vector
            normal vector of the cylinder (in which direction are its head
            and tail facing

        """
        ChannelElement2G.__init__(self)

        self.IsEqualGateSize = True

        self.length = L
        self.volume = None
        self.IsAxialSym = True
        self.heads.append(GateCircle(self))
        self.tails.append(GateCircle(self))

        self.set_normal_def(Normal)
        self.get_head_gate().set_pos_def(PosH)
        self.get_tail_gate().set_pos_def(PosT)
        self.get_head_gate().set_size_def(R)
        self.get_tail_gate().set_size_def(R)

        # Initial position along Z

        self.get_head_gate().NormalElement = Vector(0, 0, 1)
        self.get_tail_gate().NormalElement = Vector(0, 0, 1)

    def get_name(self):
        return 'CircleCoupling'

    def get_r(self):
        return self.get_head_gate().get_r()

    def get_volume(self):
        return self.volume

    def calculate_volume(self):
        slices = ChannelElement2G.slices
        poly = Arithmetic_Polygon(self.get_r(), slices)
        self.volume = poly.area() * self.get_len()

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
        print 'CircleCoupling radius Rdef =', \
            self.get_head_gate().get_r_def(), 'length =', self.length, \
            'RH =', self.get_gate_size_h(), 'RT =', \
            self.get_gate_size_t(), 'PosH =', self.get_head_gate().Pos, \
            'PosT =', self.get_pos_tail()

    def create_shape_child(self):
        print 'create_shape CircleCoupling'
        # check geometry data
        return CreateShape('circle_coupling', self.CenterPos,
                           self.RotationOperator,
                           self.get_r(), self.get_len(),
                           self.get_pos_head(),
                           self.get_pos_tail(),
                           self.get_normal_head())
