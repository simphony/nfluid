#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from nfluid.core.channel_assembly import ChannelAssembly, create_channel
from nfluid.elements.cap import Cap
from nfluid.elements.circle_coupling import CircleCoupling
from nfluid.elements.circle_tee import CircleTee
from nfluid.elements.flow_adapter import FlowAdapter
from nfluid.elements.long_elbow import LongElbow
from nfluid.elements.short_elbow import ShortElbow
from nfluid.elements.spheric_coupling import SphericCoupling
from nfluid.tests.TestBase import MakeTest1
from nfluid.util.vector import Vector

print os.path.basename(__file__), '------------------------\n'

if len(sys.argv) == 1:
    print '0: All'
    print '1: Test All 1'
    print '2: Test All 2'

    exit(0)

n_tests = 2

assembly = ChannelAssembly()

if sys.argv[1] == '1':
    print 'Test All 1'
    create_channel(CircleCoupling(R=10, L=45, PosH=Vector(20, 0, 30),
                                  Normal=Vector(0, 0, 1))
                   .link(SphericCoupling(RS=50))
                   .link(CircleCoupling(L=30))
                   .link(ShortElbow(NormalT=Vector(-0.45, 0.21, 0)))
                   .link(CircleCoupling(L=42))
                   .link(LongElbow(RC=50, NormalT=Vector(0, 0, 1)))
                   .link(LongElbow(RC=50, NormalT=Vector(1, 1, 0)))
                   .link(LongElbow(RC=50, NormalT=Vector(0, 0, 1)))
                   .link(LongElbow(RC=50, NormalT=Vector(-0.25, 11, 0)))
                   .link(LongElbow(RC=50, NormalT=Vector(0, 0, -1)))
                   .link(CircleCoupling(L=20))
                   .link(FlowAdapter(RT=30, L=20))
                   .link(CircleCoupling(L=30)))

elif sys.argv[1] == '2':
    print 'Test All 2'
    create_channel(CircleCoupling(R=10, L=45, PosH=Vector(20, 0, 30),
                                  Normal=Vector(0, 0, 1))
                   .link(SphericCoupling(RS=50))
                   .link(CircleCoupling(L=30))
                   .link(ShortElbow(NormalT=Vector(0, 1, 0)))
                   .link(CircleCoupling(L=42))
                   .link(FlowAdapter(RT=30, L=20))
                   .link(LongElbow(RC=50, NormalT=Vector(1, 0, 0)))
                   .link(CircleCoupling(L=20))
                   .link(FlowAdapter(RT=30, L=20))
                   .link(CircleCoupling(L=30)))

elif sys.argv[1] == '0':
    for i in range(1, n_tests+1):
        os.system('python ' + sys.argv[0] + ' ' + str(i))
    exit(0)

else:
    print 'Incorrect argument value'
    exit(0)

MakeTest1(assembly)
