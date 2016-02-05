#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from nfluid.tests.TestBase import MakeTest1
from nfluid.core.channel_assembly import ChannelAssembly, create_channel
from nfluid.elements.flow_adapter import FlowAdapter
from nfluid.elements.circle_coupling import CircleCoupling
from nfluid.elements.cap import Cap
from nfluid.elements.circle_tee import CircleTee
from nfluid.elements.long_elbow import LongElbow
from nfluid.elements.short_elbow import ShortElbow
from nfluid.elements.spheric_coupling import SphericCoupling
from nfluid.util.vector import Vector

print os.path.basename(__file__), '------------------------\n'

if len(sys.argv) == 1:
    print '0: All'
    print '1: '
    exit(0)

assembly = ChannelAssembly()

if sys.argv[1] == '0':
    print 'Test All 0'

    tee = create_channel(CircleCoupling(R=10, L=75, PosH=Vector(0, 0, 0),
                                        Normal=Vector(0, 0, 1))). \
        link(CircleTee(NormalT0=Vector(1, 0, 0)))
    tee2 = CircleTee(NormalT0=Vector(0, 0, 1))
    tee3 = CircleTee(NormalT0=Vector(0, 0, 1))
    tee.link(tee2)

    tee.link(tee3, 1)

    tee2.link(CircleCoupling(L=42))
    tee2.link(ShortElbow(NormalT=Vector(1, 1, 0)), 1). \
        link(LongElbow(RC=15, NormalT=Vector(0, 0, 1))). \
        link(FlowAdapter(RT=15, L=20))
    tee3.link(CircleCoupling(L=42)). \
        link(SphericCoupling(RS=20))
    tee3.link(LongElbow(RC=50, NormalT=Vector(-1, -1, 0)), 1)

elif sys.argv[1] == '1':
    print 'Test All 1'
    tee = create_channel(CircleCoupling(R=10, L=45, PosH=Vector(20, 0, 30),
                                        Normal=Vector(0, 0, 1))). \
        link(CircleCoupling(L=20)). \
        link(CircleCoupling(L=30)). \
        link(CircleTee(NormalT0=Vector(1, 0, 0)))

    tee.link(FlowAdapter(RT=23, L=20)). \
        link(ShortElbow(NormalT=Vector(0, 0, -1))). \
        link(CircleCoupling(L=42))

    tee.link(FlowAdapter(RT=15, L=27), 1). \
        link(LongElbow(RC=50, NormalT=Vector(0, 0, 1))). \
        link(CircleCoupling(L=20))

elif sys.argv[1] == '2':
    print 'Test All 2'

    tee = create_channel(CircleCoupling(R=10, L=45, PosH=Vector(20, 0, 30),
                                        Normal=Vector(0, 0, 1))). \
        link(SphericCoupling(RS=50)). \
        link(FlowAdapter(RT=30, L=20)). \
        link(CircleCoupling(L=30)). \
        link(CircleTee(NormalT0=Vector(1, 0, 0)))

    tee.link(FlowAdapter(RT=23, L=20)). \
        link(ShortElbow(NormalT=Vector(0, 0, 1))). \
        link(CircleCoupling(L=42)). \
        link(Cap(L=10))

    tee.link(FlowAdapter(RT=15, L=27), 1). \
        link(LongElbow(RC=50, NormalT=Vector(0, 0, 1))). \
        link(CircleCoupling(L=20)). \
        link(Cap(L=5))

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
else:

    print 'Incorrect argument value'
    exit(0)

MakeTest1(assembly)
