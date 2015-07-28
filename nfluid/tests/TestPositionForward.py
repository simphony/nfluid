#!/usr/bin/python
# -*- coding: utf-8 -*-
from nfluid.core.channel_assembly import *
from nfluid.elements.flow_adapter import *
from nfluid.elements.circle_coupling import *
from nfluid.elements.square_coupling import *
from nfluid.elements.elbow import *
from nfluid.tests.TestBase import *
import os

print os.path.basename(__file__), '------------------------\n'

assembly = ChannelAssembly()

create_channel(Coupling(111, 78, PosH=Vector(11, 22, 33),
                        Normal=Vector(0, 0, 1))). \
    link(FlowAdapter(RT=222, L=15)). \
    link(Coupling(L=125)). \
    link(FlowAdapter(RT=123, L=20)). \
    link(Coupling(L=200))

#  link(FlowAdapter(RT =123, L = 30)). \
#  link(Coupling(L = 20)). \

MakeTest1(assembly)
