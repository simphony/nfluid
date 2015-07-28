#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from nfluid.core.channel_assembly import *
from nfluid.elements.flow_adapter import *
from nfluid.elements.circle_coupling import *
from nfluid.elements.circle_tee import *
from nfluid.tests.TestBase import *

print os.path.basename(__file__), '------------------------\n'

if len(sys.argv) == 1:
    print '0: '
    print '1: '
    print '2: '
    print '3: '
    exit(0)

n_tests = 3

assembly = ChannelAssembly()

if sys.argv[1] == '0':
    print 'Test Tee 0'

    tee = create_channel(Coupling(111, 78, PosH=Vector(11, 22, 33),
                                  Normal=Vector(0, 0, 1))). \
        link(TeeCircle(NormalT0=Vector(1, 0, 0)))

    tee.link(FlowAdapter(RT=123, L=20), 0). \
        link(Coupling(L=200))

    tee.link(FlowAdapter(RT=155, L=27), 1). \
        link(Coupling(L=120))

elif sys.argv[1] == '1':

    print 'Test Tee 1'
elif sys.argv[1] == '2':

    print 'Test Tee 2'

    tee0 = create_channel(Coupling(111, 78, PosH=Vector(11, 22, 33),
                                   Normal=Vector(0, 0, 1))). \
        link(FlowAdapter(RT=220, L=15)). \
        link(Coupling(L=125)). \
        link(TeeCircle(220, NormalT0=Vector(1, 0, 0)))

    tee1 = tee0.link(FlowAdapter(RT=123, L=20)). \
        link(Coupling(L=200)). \
        link(TeeCircle(NormalT0=Vector(1, 0, 0)))

    tee0.link(FlowAdapter(RT=155, L=27), 1). \
        link(Coupling(L=120))

    tee1.link(FlowAdapter(RT=220, L=15)). \
        link(Coupling(L=125))

    tee1.link(FlowAdapter(RT=320, L=25), 1). \
        link(Coupling(L=25))
elif sys.argv[1] == '*':

    for i in range(0, n_tests):
        os.system('TestShapeCircleTee.py ' + str(i))
    exit(0)
else:

    print 'Incorrect argument value'
    exit(0)

MakeTest1(assembly)
