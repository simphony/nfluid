#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from nfluid.core.channel_assembly import ChannelAssembly, create_channel
from nfluid.elements.circle_coupling import CircleCoupling
from nfluid.tests.TestBase import MakeTest1
from nfluid.util.vector import Vector

print os.path.basename(__file__), '------------------------\n'

if len(sys.argv) == 1:
    print '0: All'
    print '1: Normal - forward, Pos - backward'
    print '2: Two positions, Pos - backward'
    print '3: negative Normal'

    exit(0)

n_tests = 3

assembly = ChannelAssembly()

if sys.argv[1] == '1':
    print 'Test_1'
    print 'Test Normal - forward, Pos - backward'
    create_channel(CircleCoupling(R=10, L=45, PosH=Vector(0, 20, 30),
                                  Normal=Vector(0, 0, 1))
                   .link(CircleCoupling(PosT=Vector(400, 20, 0))))

elif sys.argv[1] == '2':
    print 'Test_2'
    print 'Test Two positions, Pos - backward'
    create_channel(CircleCoupling(R=10, PosH=Vector(0, 20, 30),
                                  PosT=Vector(0, 20, 150))
                   .link(CircleCoupling(PosT=Vector(0, 20, 400))))

elif sys.argv[1] == '3':
    print 'Test_3'
    print 'Test negative Normal'
    create_channel(CircleCoupling(R=10, L=45, PosH=Vector(0, 20, 30),
                                  Normal=Vector(0, 0, -1))
                   .link(CircleCoupling(PosT=Vector(400, 20, 0))))

elif sys.argv[1] == '0':
    for i in range(1, n_tests+1):
        os.system('python ' + sys.argv[0] + ' ' + str(i))
    exit(0)

else:
    print 'Incorrect argument value'
    exit(0)

MakeTest1(assembly)
