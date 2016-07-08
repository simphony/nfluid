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
    print '0: All'
    print '1: Test 1'

    exit(0)

n_tests = 1

assembly = ChannelAssembly()

if sys.argv[1] == '1':
    print 'Test_1'
    create_channel(CircleCoupling(L=78)
                   .link(FlowAdapter(RH=22, L=15))
                   .link(CircleCoupling(L=125))
                   .link(FlowAdapter(RH=12, L=20))
                   .link(CircleCoupling(88, 20, Normal=Vector(0, 0, 1),
                                        PosT=Vector(11, 22, 800))))

elif sys.argv[1] == '0':
    for i in range(1, n_tests+1):
        os.system('python ' + sys.argv[0] + ' ' + str(i))
    exit(0)

else:
    print 'Incorrect argument value'
    exit(0)

MakeTest1(assembly)
