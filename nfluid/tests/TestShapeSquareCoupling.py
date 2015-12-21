#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from nfluid.core.channel_assembly import ChannelAssembly, create_channel
from nfluid.elements.square_coupling import SquareCoupling
from nfluid.tests.TestBase import MakeTest1
from nfluid.util.vector import Vector

print os.path.basename(__file__), '------------------------\n'

assembly = ChannelAssembly()

create_channel(SquareCoupling(111, 27, 78,
                              PosH=Vector(11, 22, 33),
                              Normal=Vector(0, 0, 1))). \
    link(SquareCoupling(L=20)). \
    link(SquareCoupling(L=100))


MakeTest1(assembly)
