#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from nfluid.core.channel_assembly import *
from nfluid.elements.circle_coupling import *
from nfluid.elements.spheric_coupling import *
from nfluid.tests.TestBase import *

print os.path.basename(__file__), '------------------------\n'

if len(sys.argv) == 1:
    print '0: '
    print '1: '
    print '2: '

    exit(0)

n_tests = 3

assembly = ChannelAssembly()

if sys.argv[1] == '0':
    print 'Test_0'

    create_channel(Coupling(10, 20, PosH=Vector(0, 20, 30),
                            Normal=Vector(0, 0, 1))).link(SphericCoupling(R=10, RS=50)). \
        link(Coupling(L=125))
elif sys.argv[1] == '1':

    print 'Test_1'

    create_channel(Coupling(10, 20, PosH=Vector(0, 20, 30),
                            Normal=Vector(1, 0, 0))). \
        link(SphericCoupling(R=10, RS=50)). \
        link(Coupling(L=125))

elif sys.argv[1] == '2':

    print 'Test_2'
elif sys.argv[1] == '*':

    for i in range(0, n_tests):
        os.system('TestShapeSphericCoupling.py ' + str(i))
    exit(0)
else:

    print 'Incorrect argument value'
    exit(0)

MakeTest1(assembly)
