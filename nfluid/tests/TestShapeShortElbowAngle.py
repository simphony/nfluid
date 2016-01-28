#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from nfluid.core.channel_assembly import ChannelAssembly, create_channel
from nfluid.elements.circle_coupling import CircleCoupling
from nfluid.elements.short_elbow_angle import ShortElbowAngle
from nfluid.tests.TestBase import MakeTest1
from nfluid.util.vector import Vector

print os.path.basename(__file__), '------------------------\n'

if len(sys.argv) == 1:
    print '0: Test 0'
    print '1: Test 1'
    print '2: All'

    exit(0)

n_tests = 2

assembly = ChannelAssembly()

if sys.argv[1] == '0':
    print 'Test_0'
    create_channel(
        CircleCoupling(R=10, L=20,
                       PosH=Vector(0, 0, 0), Normal=Vector(0, 0, 1))
        .link(ShortElbowAngle(Angle=45, NormalT=Vector(1, 0, 1)))
        .link(CircleCoupling(L=50))
        .link(ShortElbowAngle(Angle=45, NormalT=Vector(0, 0, 1)))
        .link(CircleCoupling(L=30))
    )

elif sys.argv[1] == '1':
    print 'Test_1'
    create_channel(
        CircleCoupling(
            R=20,
            L=40,
            PosH=Vector(0, 0, 0),
            Normal=Vector(0, 0, 1)
        )
        .link(ShortElbowAngle(
            Angle=135,
            NormalT=Vector(0.707107, 0.707107, -1)
            ))
        .link(CircleCoupling(L=80))
    )

elif sys.argv[1] == '2':
    for i in range(0, n_tests):
        os.system('python ' + sys.argv[0] + ' ' + str(i))
    exit(0)

else:
    print 'Incorrect argument value'
    exit(0)

MakeTest1(assembly)
