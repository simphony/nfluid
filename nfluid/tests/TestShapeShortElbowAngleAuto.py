#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from nfluid.core.channel_assembly import ChannelAssembly, create_channel
from nfluid.elements.circle_coupling import CircleCoupling
from nfluid.elements.long_elbow import LongElbow
from nfluid.elements.short_elbow_angle_auto import ShortElbowAngleAuto
from nfluid.tests.TestBase import MakeTest1
from nfluid.util.vector import Vector

print os.path.basename(__file__), '------------------------\n'

if len(sys.argv) == 1:
    print '0: Test 0'
    print '1: Test 1'
    print '2: Test 2'
    print '3: All'

    exit(0)

n_tests = 3

assembly = ChannelAssembly()

if sys.argv[1] == '0':
    print 'Test_0'
    create_channel(
        CircleCoupling(R=10, L=33,
                       PosH=Vector(0, 0, 0), Normal=Vector(0, 0, 1))
        .link(ShortElbowAngleAuto(NormalT=Vector(1, 0, -1)))
        .link(CircleCoupling(L=122))
    )

elif sys.argv[1] == '1':
    print 'Test_1'
    create_channel(
        CircleCoupling(R=10, L=20,
                       PosH=Vector(0, 0, 0), Normal=Vector(0, 0, 1))
        .link(LongElbow(RC=50, NormalT=Vector(0, 1, 0)))
        .link(ShortElbowAngleAuto(NormalT=Vector(1, 1, -1)))
        .link(CircleCoupling(L=100))
    )

elif sys.argv[1] == '2':
    print 'Test_2'
    create_channel(
        CircleCoupling(R=5, L=40,
                       PosH=Vector(0, 0, 0), Normal=Vector(1, 1, 0))
        .link(ShortElbowAngleAuto(NormalT=Vector(0, -1, 1)))
        .link(CircleCoupling(L=50))
        .link(ShortElbowAngleAuto(NormalT=Vector(3, 2, 1)))
        .link(CircleCoupling(L=60))
        .link(ShortElbowAngleAuto(NormalT=Vector(-1, -2, -3)))
        .link(CircleCoupling(L=50))
        .link(ShortElbowAngleAuto(NormalT=Vector(-2, 3, 1)))
        .link(CircleCoupling(L=80))
    )

elif sys.argv[1] == '3':
    for i in range(0, n_tests):
        os.system('python ' + sys.argv[0] + ' ' + str(i))
    exit(0)

else:
    print 'Incorrect argument value'
    exit(0)

MakeTest1(assembly)
