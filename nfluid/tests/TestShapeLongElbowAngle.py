#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from nfluid.core.channel_assembly import ChannelAssembly, create_channel
from nfluid.elements.circle_coupling import CircleCoupling
from nfluid.elements.long_elbow import LongElbow
from nfluid.elements.long_elbow_angle import LongElbowAngle
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
    create_channel(CircleCoupling(10, 15, PosH=Vector(0, 0, 0),
                                  Normal=Vector(0, 0, 1))
                   .link(LongElbowAngle(RC=50, Angle=135,
                                        NormalT=Vector(1, 0, -1)))
                   .link(CircleCoupling(L=122)))

elif sys.argv[1] == '2':
    print 'Test_2'
    create_channel(CircleCoupling(10, 20, PosH=Vector(0, 0, 0),
                                  Normal=Vector(0, 0, 1))
                   .link(LongElbow(RC=50, NormalT=Vector(0, 1, 0)))
                   .link(LongElbowAngle(RC=50, Angle=45,
                                        NormalT=Vector(0, 1, 1)))
                   .link(CircleCoupling(L=100)))

elif sys.argv[1] == '0':
    for i in range(0, n_tests):
        os.system('python ' + sys.argv[0] + ' ' + str(i))
    exit(0)

else:
    print 'Incorrect argument value'
    exit(0)

MakeTest1(assembly)
