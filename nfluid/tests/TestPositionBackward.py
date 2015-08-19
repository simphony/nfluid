#!/usr/bin/python
# -*- coding: utf-8 -*-
from nfluid.core.channel_assembly import *
from nfluid.elements.flow_adapter import *
from nfluid.elements.circle_coupling import *
from nfluid.elements.elbow import *
from nfluid.tests.TestBase import *
import os

print os.path.basename(__file__), '------------------------\n'

assembly = ChannelAssembly()

#    Normal = Vector(0, 0, 1)

create_channel(CircleCoupling(L=78)). \
    link(FlowAdapter(RH=22, L=15)). \
    link(CircleCoupling(L=125)). \
    link(FlowAdapter(RH=12, L=20)). \
    link(CircleCoupling(88, 20, Normal = Vector(0, 0, 1), PosT=Vector(11, 22, 800)))

MakeTest1(assembly)
