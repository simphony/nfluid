#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from nfluid.core.channel_assembly import ChannelAssembly, create_channel
from nfluid.elements.cap import Cap
from nfluid.elements.circle_coupling import CircleCoupling
from nfluid.elements.circle_tee import CircleTee
from nfluid.elements.flow_adapter import FlowAdapter
from nfluid.elements.long_elbow_angle import LongElbowAngle
from nfluid.elements.short_elbow_angle import ShortElbowAngle
from nfluid.elements.spheric_coupling import SphericCoupling
from nfluid.tests.TestBase import MakeTest1
from nfluid.util.vector import Vector

print os.path.basename(__file__), '------------------------\n'

if len(sys.argv) == 1:
    print '0: All'
    print '1: Test All 1'
    print '2: Test All 2'
    print '3: Test All 3'

    exit(0)

n_tests = 3

assembly = ChannelAssembly()

if sys.argv[1] == '1':
    print 'Test All 1'
    tee = create_channel(CircleCoupling(R=10, L=75, PosH=Vector(0, 0, 0),
                                        Normal=Vector(0, 0, 1))
                         .link(CircleTee(NormalT0=Vector(1, 0, 0))))

    tee2 = CircleTee(NormalT0=Vector(0, 0, 1))
    tee3 = CircleTee(NormalT0=Vector(0, 0, 1))
    tee.link(tee2, 0)
    tee.link(tee3, 1)

    tee2.link(CircleCoupling(L=42), 0)
    tee2.link(ShortElbowAngle(NormalT=Vector(1, 1, 0)), 1) \
        .link(LongElbowAngle(RC=15, NormalT=Vector(0, 0, 1))) \
        .link(FlowAdapter(RT=15, L=20))

    tee3.link(CircleCoupling(L=42), 0) \
        .link(SphericCoupling(RS=20))
    tee3.link(LongElbowAngle(RC=50, NormalT=Vector(-1, -1, 0)), 1)

elif sys.argv[1] == '2':
    print 'Test All 2'
    tee = create_channel(CircleCoupling(R=10, L=45, PosH=Vector(20, 0, 30),
                                        Normal=Vector(0, 0, 1))
                         .link(CircleCoupling(L=20))
                         .link(CircleCoupling(L=30))
                         .link(CircleTee(NormalT0=Vector(1, 0, 0))))

    tee.link(FlowAdapter(RT=23, L=20), 0) \
       .link(ShortElbowAngle(NormalT=Vector(0, 0, -1))) \
       .link(CircleCoupling(L=42))

    tee.link(FlowAdapter(RT=15, L=27), 1) \
       .link(LongElbowAngle(RC=50, NormalT=Vector(0, 0, 1))) \
       .link(CircleCoupling(L=20))

elif sys.argv[1] == '3':
    print 'Test All 3'
    tee = create_channel(CircleCoupling(R=10, L=45, PosH=Vector(20, 0, 30),
                                        Normal=Vector(0, 0, 1))
                         .link(SphericCoupling(RS=50))
                         .link(FlowAdapter(RT=30, L=20))
                         .link(CircleCoupling(L=30))
                         .link(CircleTee(NormalT0=Vector(1, 0, 0))))

    tee.link(FlowAdapter(RT=23, L=20), 0) \
       .link(ShortElbowAngle(NormalT=Vector(0, 0, 1))) \
       .link(CircleCoupling(L=42)) \
       .link(Cap(L=10))

    tee.link(FlowAdapter(RT=15, L=27), 1) \
       .link(LongElbowAngle(RC=50, NormalT=Vector(0, 0, 1))) \
       .link(CircleCoupling(L=20)) \
       .link(Cap(L=5))

    print '-----------------------------'
    el1 = assembly.get_element_by_id(1)
    el2 = assembly.get_element_by_id(2)
    el3 = assembly.get_element_by_id(3)

    if el1 is not None:
        print 'Name: ', el1.get_name(), 'get_element_by_id 1: ', \
            el1.print_info()
    if el2 is not None:
        print 'Name: ', el2.get_name(), 'get_element_by_id 2: ', \
            el2.print_info()
    if el3 is not None:
        print 'Name: ', el3.get_name(), 'get_element_by_id 3: ', \
            el3.print_info()

    print el2.get_chain_str()

    if el1 is not None:
        assembly.delete_element(el1)

    new_elt = CircleCoupling(L=125)
    el3.insert_before(new_elt)

    assembly.insert_element_before(new_elt, el3)

elif sys.argv[1] == '0':
    for i in range(1, n_tests+1):
        os.system('python ' + sys.argv[0] + ' ' + str(i))
    exit(0)

else:
    print 'Incorrect argument value'
    exit(0)

MakeTest1(assembly)
