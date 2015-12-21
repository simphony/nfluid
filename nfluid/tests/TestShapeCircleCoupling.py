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
    print '0: Normal - forward, Pos - backward'
    print '1: Normal - forward, Pos - backward'
    print '2: negative Normal'

    exit(0)

n_tests = 3

assembly = ChannelAssembly()

# print "sys.argv ", sys.argv
# print "len(sys.argv) ", len(sys.argv)

if sys.argv[1] == '0':
    print 'Test_0'
    print 'Test Normal - forward, Pos - backward'

    create_channel(CircleCoupling(R=10, L=45, PosH=Vector(0, 20, 30),
                                  Normal=Vector(0, 0, 1))). \
        link(CircleCoupling(PosT=Vector(400, 20, 0)))
elif sys.argv[1] == '1':

    print 'Test_1'
    print 'Test Two positions, Pos - backward'

    create_channel(CircleCoupling(R=10, PosH=Vector(0, 20, 30),
                                  PosT=Vector(0, 20, 150))). \
        link(CircleCoupling(PosT=Vector(0, 20, 400)))
elif sys.argv[1] == '2':

    print 'Test_2'
    print 'Test negative Normal'

    create_channel(CircleCoupling(R=10, L=45, PosH=Vector(0, 20, 30),
                                  Normal=Vector(0, 0, -1))). \
        link(CircleCoupling(PosT=Vector(400, 20, 0)))
elif sys.argv[1] == '*':

    for i in range(0, n_tests):
        os.system('TestShapeCircleCoupling.py ' + str(i))
    exit(0)
else:

    print 'Incorrect argument value'
    exit(0)

#  link (CircleCoupling(PosH = Vector(0, 20, 50), PosT = Vector(0, 20, 400)) )

MakeTest1(assembly)
