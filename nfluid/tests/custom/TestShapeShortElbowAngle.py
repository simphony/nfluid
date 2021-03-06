#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from nfluid.core.channel_assembly import ChannelAssembly, create_channel
from nfluid.elements.circle_coupling import CircleCoupling
from nfluid.elements.short_elbow_angle import ShortElbowAngle
from nfluid.tests.TestBase import MakeTest1
from nfluid.util.vector import Vector
import math

print os.path.basename(__file__), '------------------------\n'

if len(sys.argv) == 1:
    print '0: All'
    print '1: Test 1'
    print '2: Test 2'
    print '3: Test 3'
    print '4: Test 4'
    print '5: Test 5'
    print '6: Test 6'

    exit(0)

n_tests = 6

assembly = ChannelAssembly()

if sys.argv[1] == '1':
    print 'Test_1'
    create_channel(CircleCoupling(10, 20, PosH=Vector(0, 27, 30),
                                  Normal=Vector(0, 0, 1))
                   .link(ShortElbowAngle(NormalT=Vector(1, 0, 0)))
                   .link(CircleCoupling(L=125)))

elif sys.argv[1] == '2':
    print 'Test_2'
    create_channel(CircleCoupling(10, 20, PosH=Vector(0, 27, 30),
                                  Normal=Vector(1, 0, 0))
                   .link(ShortElbowAngle(NormalT=Vector(0, 1, 0)))
                   .link(CircleCoupling(L=125)))

elif sys.argv[1] == '3':
    print 'Test_3'
    create_channel(CircleCoupling(R=10, L=20, PosH=Vector(0, 0, 0),
                                  Normal=Vector(0, 0, 1))
                   .link(ShortElbowAngle(Angle=45, NormalT=Vector(1, 0, 1)))
                   .link(CircleCoupling(L=50))
                   .link(ShortElbowAngle(Angle=45, NormalT=Vector(0, 0, 1)))
                   .link(CircleCoupling(L=30)))

elif sys.argv[1] == '4':
    print 'Test_4'
    create_channel(CircleCoupling(R=20, L=40, PosH=Vector(0, 0, 0),
                                  Normal=Vector(0, 0, 1))
                   .link(ShortElbowAngle(Angle=45, NormalT=Vector(0, 1, 1)))
                   .link(CircleCoupling(L=80)))

elif sys.argv[1] == '5':
    print 'Test_5'
    sqrt2 = math.sqrt(2)
    create_channel(CircleCoupling(R=5, L=30, PosH=Vector(0, 0, 0),
                                  Normal=Vector(0, 0, 1))
                   .link(ShortElbowAngle(Angle=135,
                                         NormalT=Vector(1, 1, -sqrt2)))
                   .link(CircleCoupling(L=80)))

elif sys.argv[1] == '6':
    print 'Test_6'
    create_channel(CircleCoupling(R=10, L=20, PosH=Vector(0, 0, 0),
                                  Normal=Vector(0, 0, 1))
                   .link(ShortElbowAngle(Angle=90, NormalT=Vector(1, 0, 0)))
                   .link(CircleCoupling(L=50))
                   .link(ShortElbowAngle(Angle=90, NormalT=Vector(0, 0, 1)))
                   .link(CircleCoupling(L=30)))

elif sys.argv[1] == '0':
    for i in range(1, n_tests+1):
        os.system('python ' + sys.argv[0] + ' ' + str(i))
    exit(0)

else:
    print 'Incorrect argument value'
    exit(0)

MakeTest1(assembly)
