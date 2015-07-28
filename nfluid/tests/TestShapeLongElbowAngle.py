#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from nfluid.core.channel_assembly import *
from nfluid.elements.circle_coupling import *
from nfluid.elements.long_elbow import *
from nfluid.elements.long_elbow_angle import *
from nfluid.tests.TestBase import *

print os.path.basename(__file__), '------------------------\n'

if len(sys.argv) == 1:
    print '0: '
    print '1: '
    print '2: '

    exit(0)

n_tests = 3

NormalH0 = Vector(0, 0, 100)

assembly = ChannelAssembly()

if sys.argv[1] == '0':
    print 'Test_0'

    print '%%%%%%%%%%%%%%', NormalH0

    create_channel(Coupling(10, 15, PosH=Vector(0, 77, 130),
                   Normal=Vector(0, 0, 1))). \
        link(LongElbowAngle(RC=50, Angle=135, NormalT=Vector(1, 0, 1))). \
        link(Coupling(L=122))

    print '%%%%%%%%%%%%%%', NormalH0
elif sys.argv[1] == '1':

    print 'Test_1'

    create_channel(Coupling(10, 20, PosH=Vector(0, 20, 30),
                   Normal=Vector(0, 0, 1))). \
        link(LongElbow(RC=50, NormalT=Vector(0, 1, 0))). \
        link(LongElbowAngle(RC=50, Angle=45, NormalT=Vector(1, 0, 0))). \
        link(Coupling(L=100))

    print '%%%%%%%%%%%%%%', NormalH0
elif sys.argv[1] == '2':

    print 'Test_2'
elif sys.argv[1] == '*':

    for i in range(0, n_tests):
        os.system('TestShapeLongElbowAngle.py ' + str(i))
    exit(0)
else:

    print 'Incorrect argument value'
    exit(0)

MakeTest1(assembly)

PosH = Vector(1, 0, 0)
Normal = Vector(5, 5, 0)
angle = get_vector_angle_grad(PosH, Normal)
print 'angle = ', angle
