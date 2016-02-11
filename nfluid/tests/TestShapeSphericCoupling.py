#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from nfluid.core.channel_assembly import ChannelAssembly, create_channel
from nfluid.elements.circle_coupling import CircleCoupling
from nfluid.elements.spheric_coupling import SphericCoupling
from nfluid.tests.TestBase import MakeTest1
from nfluid.util.vector import Vector

print os.path.basename(__file__), '------------------------\n'

if len(sys.argv) == 1:
    print '0: All'
    print '1: Test 1'
    print '2: Test 2'

    exit(0)

n_tests = 2

assembly = ChannelAssembly()

if sys.argv[1] == '1':
    print 'Test_1'
    create_channel(CircleCoupling(1, 5, PosH=Vector(0, 20, 0),
                                  Normal=Vector(0, 0, 1))
                   .link(SphericCoupling(R=1, RS=5))
                   .link(CircleCoupling(L=10)))

elif sys.argv[1] == '2':
    print 'Test_2'
    create_channel(CircleCoupling(10, 20, PosH=Vector(0, 20, 30),
                                  Normal=Vector(1, 0, 0))
                   .link(SphericCoupling(R=10, RS=50))
                   .link(CircleCoupling(L=125)))

elif sys.argv[1] == '0':
    for i in range(1, n_tests+1):
        os.system('python ' + sys.argv[0] + ' ' + str(i))
    exit(0)

else:
    print 'Incorrect argument value'
    exit(0)

MakeTest1(assembly)
