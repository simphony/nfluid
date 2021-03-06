#!/usr/bin/python
# -*- coding: utf-8 -*-
from nfluid.shapes.shapes import CreateShape
from nfluid.core.channel_element_2g import ChannelElement2G
from nfluid.core.gates import GateCircle
from nfluid.util.vector import Vector
from nfluid.geometry.auxiliar_geometry import Arithmetic_Polygon
import math
import copy
# Class of ElbowAngle


class LongElbowAngle(ChannelElement2G):

    def __init__(
        self,
        RC,
        Angle=90,
        R=None,
        PosH=None,
        PosT=None,
        NormalH=None,
        NormalT=None,
    ):
        """
        Parameters
        ----------
        RC : real
            the outter radius of the elbow
        Angle : real
            the angle between head and tail positions
        R : real
            the radius of the piece
        PosH : Vector
            the position of the center of the head
        PosT : Vector
            the position of the center of the tail
        NormalH : Vector
            normal vector of the head
        NormalT : Vector
            normal vector of the tail

        """
        ChannelElement2G.__init__(self)

        self.IsEqualGateSize = True

        self.heads.append(GateCircle(self))
        self.tails.append(GateCircle(self))

        self.angle = Angle
        self.RadiusCurvature = RC

        self.length = 2*math.pi*RC * Angle/360.0
        self.volume = None

        # TODO Correct NormalT if both NormalH and NormalT are defined

        self.get_head_gate().set_normal_def(copy.copy(NormalH))
        self.get_tail_gate().set_normal_def(copy.copy(NormalT))

        self.get_head_gate().set_pos_def(copy.copy(PosH))
        self.get_tail_gate().set_pos_def(copy.copy(PosT))

        self.get_head_gate().set_size_def(R)
        self.get_tail_gate().set_size_def(R)

        # Initial position along Z and X

        self.cos = math.cos(math.radians(self.angle))
        self.sin = math.sin(math.radians(self.angle))

        self.get_head_gate().NormalElement = Vector(0, 0, 1)
        self.get_tail_gate().NormalElement = Vector(-self.sin, 0, self.cos)

        # Move to resolve own
        self.get_head_gate().PosElement = Vector(0, 0, 0)
        self.get_tail_gate().PosElement = Vector((self.cos - 1) * RC,
                                                 0, self.sin * RC)

    def get_name(self):
        return 'LongElbowAngle'

    def get_r(self):
        return self.get_head_gate().get_r()

    def get_r_curv(self):
        return self.RadiusCurvature

    def get_volume(self):
        return self.volume

    def get_angle(self):
        return self.angle

    def calculate_volume(self):
        slices = ChannelElement2G.slices
        poly = Arithmetic_Polygon(self.get_r(), slices)
        self.volume = poly.area() * self.get_len()

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
        print 'LongElbowAngle radius Rdef =', \
            self.get_head_gate().get_r_def(), 'RH =', \
            self.get_gate_size_h(), 'RT =', self.get_gate_size_t()

    def create_shape_child(self):
        print 'create_shape LongElbowAngle'
        # check geometry data

        return CreateShape('long_elbow_angle', self.CenterPos,
                           self.RotationOperator,
                           self.get_r_curv(),
                           self.angle,
                           self.get_r(),
                           self.get_pos_head(),
                           self.get_pos_tail(),
                           self.get_normal_head(),
                           self.get_normal_tail())
