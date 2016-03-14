#!/usr/bin/python
# -*- coding: utf-8 -*-
from nfluid.shapes.shapes import CreateShape
from nfluid.core.channel_element_2g import ChannelElement2G
from nfluid.core.gates import GateCircle
from nfluid.util.vector import Vector
from nfluid.util.vector import get_vector_angle_grad
from nfluid.geometry.auxiliar_geometry import Arithmetic_Polygon
import math
import copy
# Class of LongElbowNormals


class LongElbowNormals(ChannelElement2G):

    def __init__(
        self,
        RC,
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

        self.angle = None
        self.RadiusCurvature = RC
        self.volume = None

        # TODO Correct NormalT if both NormalH and NormalT are defined

        self.get_head_gate().set_normal_def(copy.copy(NormalH))
        self.get_tail_gate().set_normal_def(copy.copy(NormalT))

        self.get_head_gate().set_pos_def(copy.copy(PosH))
        self.get_tail_gate().set_pos_def(copy.copy(PosT))

        self.get_head_gate().set_size_def(R)
        self.get_tail_gate().set_size_def(R)

        # Initial position along Z and X

        self.get_head_gate().NormalElement = Vector(0, 0, 1)

        # Move to resolve own
        self.get_head_gate().PosElement = Vector(0, 0, 0)

    def get_name(self):
        return 'LongElbowNormals'

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
        if self.get_normal_head() is not None and \
           self.get_normal_tail() is not None:
            self.angle = get_vector_angle_grad(self.get_normal_head(),
                                               self.get_normal_tail())
            print "resolve_geometry_child angle", self.angle, \
                  "radius", self.RadiusCurvature
            self.length = 2*math.pi*self.RadiusCurvature * self.angle/360.0

            self.cos = math.cos(math.radians(self.angle))
            self.sin = math.sin(math.radians(self.angle))
            self.get_tail_gate().NormalElement = Vector(-self.sin, 0,
                                                        self.cos)
            self.get_tail_gate().PosElement = \
                Vector((self.cos - 1) * self.RadiusCurvature, 0,
                       self.sin * self.RadiusCurvature)

        if self.volume is None:
            try:
                self.calculate_volume()
            except:
                pass
        print "-- -- -- THE VOLUME -- -- --", self.volume

        return ''

    def print_info(self):
        ChannelElement2G.print_info(self)
        print 'LongElbowNormals radius Rdef =', \
            self.get_head_gate().get_r_def(), 'RH =', \
            self.get_gate_size_h(), 'RT =', self.get_gate_size_t()

    def create_shape_child(self):
        print 'create_shape LongElbowNormals'
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
