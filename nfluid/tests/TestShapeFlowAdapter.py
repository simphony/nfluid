#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys

from nfluid.core.channel_assembly import ChannelAssembly, create_channel
from nfluid.elements.circle_coupling import CircleCoupling
from nfluid.elements.flow_adapter import FlowAdapter
from nfluid.tests.TestBase import MakeTest1
from nfluid.util.vector import Vector

print os.path.basename(__file__), '------------------------\n'

if len(sys.argv) == 1:
    print '0: Normal (0,0,1)'
    print '1: Normal (1,0,0)'
    print '2: All'

    exit(0)

n_tests = 2

assembly = ChannelAssembly()

if sys.argv[1] == '0':
    print 'Test_0'

    create_channel(CircleCoupling(R=10, L=20, PosH=Vector(0, 20, 30),
                                  Normal=Vector(0, 0, 1))). \
        link(FlowAdapter(L=15)). \
        link(CircleCoupling(R=45, L=125))
elif sys.argv[1] == '1':

    print 'Test_1'

    create_channel(CircleCoupling(R=10, L=20, PosH=Vector(0, 20, 30),
                                  Normal=Vector(1, 0, 0))). \
        link(FlowAdapter(L=15)). \
        link(CircleCoupling(R=45, L=125))
elif sys.argv[1] == '2':

    for i in range(0, n_tests):
        os.system('TestShapeFlowAdapter.py ' + str(i))
    exit(0)
else:

    print 'Incorrect argument value'
    exit(0)

MakeTest1(assembly)
