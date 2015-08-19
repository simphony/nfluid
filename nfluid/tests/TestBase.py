#!/usr/bin/python
# -*- coding: utf-8 -*-
from nfluid.core.channel_assembly import *
import os


def MakeTest1(assembly):
    print 'resolve_geometry ----------------------------------'
    res = assembly.resolve_geometry()
    if res != '':
        print '-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-'
        print 'resolve_geometry res = ', '|', res, '|'
        print '-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-'

    print '''

print_info Assembly ---------------------------'''
    assembly.print_info()

    print 'Test Geometry -------------------------------------'
    res = assembly.is_resolved_geometry()
    if res == '':
        print 'Geometry resolved'
    else:
        print '-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-'
        print 'Geometry error res = ', res
        print '-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-'
        exit()

    res = assembly.create_shapes()
    if res == '':
        print 'Shapes created'
    else:
        print '-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-'
        print 'Shapes creation error res = ', res
        print '-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-'

    res = assembly.export('Test1.stl')
    if res == '':
        print 'Shapes exported'
    else:
        print '-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-'
        print 'Shapes export error res = ', res
        print '-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-'

    assembly.show_shapes()

    assembly.release_shapes()
