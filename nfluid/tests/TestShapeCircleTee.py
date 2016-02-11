#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from nfluid.core.channel_assembly import ChannelAssembly, create_channel
from nfluid.elements.circle_coupling import CircleCoupling
from nfluid.elements.circle_tee import CircleTee
from nfluid.elements.flow_adapter import FlowAdapter
from nfluid.tests.TestBase import MakeTest1
from nfluid.util.vector import Vector

print os.path.basename(__file__), '------------------------\n'

if len(sys.argv) == 1:
    print '0: All'
    print '1: Test Tee 1'
    print '2: Test Tee 2'

    exit(0)

n_tests = 2

assembly = ChannelAssembly()

if sys.argv[1] == '1':
    print 'Test Tee 1'
    tee = create_channel(CircleCoupling(111, 78, PosH=Vector(11, 22, 33),
                                        Normal=Vector(0, 0, 1))
                         .link(CircleTee(NormalT0=Vector(1, 0, 0))))

    tee.link(FlowAdapter(RT=123, L=20), 0) \
       .link(CircleCoupling(L=200))

    tee.link(FlowAdapter(RT=155, L=27), 1) \
       .link(CircleCoupling(L=120))

elif sys.argv[1] == '2':
    print 'Test Tee 2'
    tee0 = create_channel(CircleCoupling(111, 78, PosH=Vector(11, 22, 33),
                                         Normal=Vector(0, 0, 1))
                          .link(FlowAdapter(RT=220, L=115))
                          .link(CircleCoupling(L=125))
                          .link(CircleTee(220, NormalT0=Vector(1, 0, 0))))

    tee1 = tee0.link(FlowAdapter(RT=123, L=120), 0) \
               .link(CircleCoupling(L=200)) \
               .link(CircleTee(NormalT0=Vector(0, 1, 0)))

    tee0.link(FlowAdapter(RT=155, L=127), 1) \
        .link(CircleCoupling(L=120))

    tee1.link(FlowAdapter(RT=220, L=115), 0) \
        .link(CircleCoupling(L=125))

    tee1.link(FlowAdapter(RT=320, L=125), 1) \
        .link(CircleCoupling(L=125))

elif sys.argv[1] == '0':
    for i in range(1, n_tests+1):
        os.system('python ' + sys.argv[0] + ' ' + str(i))
    exit(0)

else:
    print 'Incorrect argument value'
    exit(0)

MakeTest1(assembly)
