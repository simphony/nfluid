#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from nfluid.core.channel_assembly import *
from nfluid.elements.square_coupling import *
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

    create_channel(SquareCoupling(111, 27, 78,
                              PosH=Vector(11, 22, 33),
                              Normal=Vector(0, 0, 1))). \
        link(SquareCoupling(L=20)). \
        link(SquareCoupling(L=100))
elif sys.argv[1] == '1':

    print 'Test_1'
elif sys.argv[1] == '2':

    print 'Test_2'
elif sys.argv[1] == '*':

    for i in range(0, n_tests):
        os.system('TestShapeSquareCoupling.py ' + str(i))
    exit(0)
else:

    print 'Incorrect argument value'
    exit(0)

MakeTest1(assembly)
