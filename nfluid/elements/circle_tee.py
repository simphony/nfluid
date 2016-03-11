#!/usr/bin/python
# -*- coding: utf-8 -*-
from nfluid.shapes.shapes import CreateShape
from nfluid.core.channel_element import ChannelElement
from nfluid.core.gates import GateCircle
from nfluid.util.vector import Vector
from nfluid.geometry.auxiliar_geometry import Arithmetic_Polygon


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
    """
    Parameters
    ----------
    R : real
        the radius of the piece
    PosH : Vector
        the position of the center of the head
    PosT0 : Vector
        position of the first tail of the tee
    PosT1 : Vector
        position of the second tail of the tee
    NormalH : Vector
        normal vector of the head
    NormalT0 : Vector
        normal vector of the first tail of the tee
    NormalT1 : Vector
        normal vector of the second tail of the tee

    """
        # NormalH, NormalT0 must be orthogonal
        # NormalT should be corrected to respect that

        ChannelElement.__init__(self)

        self.IsEqualGateSize = True

        self.volume = None

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

    def get_volume(self):
        return self.volume

    def calculate_volume(self):
        slices = ChannelElement.slices
        poly = Arithmetic_Polygon(self.get_r(), slices)
        v_cyl = poly.area() * self.get_len()
        r = self.get_r()
        v_gate = (16.0 / 3.0) * r * r * r
        self.volume = v_gate + ((3.0 / 2.0) * (v_cyl - v_gate))

    def resolve_geometry_child(self):

        R = self.get_r()
        if R is not None:
            self.length = 3.0 * R

            self.get_head_gate().PosElement = Vector(0, 0, -R)
            self.get_tail_gate(0).PosElement = Vector(R, 0, 0)
            self.get_tail_gate(1).PosElement = Vector(-R, 0, 0)

        if self.volume is None:
            try:
                self.calculate_volume()
            except Exception as e:
                print e
                pass
        print "-- -- -- THE VOLUME -- -- --", self.volume
        return ''

    def create_shape_child(self):
        # check geometry data
        print 'create_shape CircleTee'

        return CreateShape('circle_tee', self.CenterPos, self.RotationOperator,
                           self.get_head_gate().get_r(),
                           self.get_pos_head(), self.get_pos_tail(0),
                           self.get_pos_tail(1), self.get_head_gate(0).Normal,
                           self.get_tail_gate(0).Normal)
