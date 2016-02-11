#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from nfluid.core.channel_assembly import ChannelAssembly, create_channel
from nfluid.elements.circle_coupling import CircleCoupling
from nfluid.elements.circle_path import CirclePath
from nfluid.elements.flow_adapter import FlowAdapter
from nfluid.elements.long_elbow import LongElbow
from nfluid.elements.spheric_coupling import SphericCoupling
from nfluid.tests.TestBase import MakeTest1
from nfluid.util.vector import Vector

print os.path.basename(__file__), '------------------------\n'

if len(sys.argv) == 1:
    print '0: All'
    print '1: Test 1'
    print '2: Test 2'
    print '3: Test 3'
    print '4: Test 4'
    print '5: Test 5'

    exit(0)

n_tests = 5

assembly = ChannelAssembly()

if sys.argv[1] == '1':
    print 'Test_1'
    create_channel(
             CircleCoupling(R=5, L=40, PosH=Vector(0, 0, 0),
                            Normal=Vector(0, 0, 1))
             .link(CirclePath(Points=[Vector(0, 0, 0), Vector(0, 0, 50),
                                      Vector(50, 0, 50), Vector(50, 0, 100),
                                      Vector(100, 0, 100)],
                              NormalT=Vector(1, 0, 0)))
             .link(LongElbow(RC=50, NormalT=Vector(0, 1, 0))))

elif sys.argv[1] == '2':
    print 'Test_2'
    create_channel(
             CircleCoupling(R=2, L=40, PosH=Vector(0, 0, 0),
                            Normal=Vector(0, 0, 1))
             .link(FlowAdapter(RT=5, L=5))
             .link(CirclePath(Points=[Vector(0, 0, 0), Vector(0, 0, 50),
                                      Vector(50, 0, 25), Vector(25, 25, 75),
                                      Vector(50, 0, 100), Vector(50, 50, 100)],
                              NormalT=Vector(-1, 1, 0)))
             .link(SphericCoupling(RS=16))
             .link(LongElbow(RC=50, NormalT=Vector(1, 1, 1))))

elif sys.argv[1] == '3':
    print 'Test_3'
    points = [Vector(0, -2, 0), Vector(0, -1, 0), Vector(0, -1, 1),
              Vector(0, -3, 3), Vector(0, -6, 6), Vector(0, -9, 9),
              Vector(0, -9, 12), Vector(0, -6, 15), Vector(0, -3, 15),
              Vector(0, -3, 12), Vector(0, 0, 9), Vector(0, 3, 12),
              Vector(0, 3, 15), Vector(0, 6, 15), Vector(0, 9, 12),
              Vector(0, 9, 9), Vector(0, 6, 6), Vector(0, 3, 3),
              Vector(0, 1, 1), Vector(0, 1, 0)]
    create_channel(
             CircleCoupling(R=0.5, L=5, PosH=Vector(0, 0, 0),
                            Normal=Vector(0, 1, 0))
             .link(CirclePath(Points=points, NormalT=Vector(0, 0, -1)))
             .link(LongElbow(RC=5, NormalT=Vector(0, 1, 0)))
             .link(SphericCoupling(RS=2))
             .link(CircleCoupling(L=4)))

elif sys.argv[1] == '4':
    print 'Test_4'
    points = [Vector(0, 0, 0), Vector(0, 0, 50), Vector(50, 0, 50),
              Vector(50, 0, 100), Vector(0, 0, 100), Vector(0, 0, 150)]
    create_channel(CircleCoupling(R=5, L=15, PosH=Vector(0, 0, 0),
                                  Normal=Vector(0, 0, 1))
                   .link(CirclePath(Points=points, NormalT=Vector(0, 0, 1),
                                    Twist=30))
                   .link(LongElbow(RC=40, NormalT=Vector(1, 2, 0))))

elif sys.argv[1] == '5':
    print 'Test_5'
    points = [Vector(0, 0, 0), Vector(0, 0, 50), Vector(0, 50, 50),
              Vector(0, 50, 100), Vector(0, 20, 100), Vector(0, 20, 150)]
    create_channel(CircleCoupling(R=5, L=35, PosH=Vector(0, 0, 0),
                                  Normal=Vector(0, 0, 1))
                   .link(LongElbow(RC=25, NormalT=Vector(1, -1, 0)))
                   .link(CirclePath(Points=points, NormalT=Vector(1, -1, 0),
                                    Twist=160))
                   .link(CircleCoupling(L=40)))

elif sys.argv[1] == '0':
    for i in range(1, n_tests+1):
        os.system('python ' + sys.argv[0] + ' ' + str(i))
    exit(0)

else:
    print 'Incorrect argument value'
    exit(0)

MakeTest1(assembly)
