#!/usr/bin/python
# -*- coding: utf-8 -*-
# from nfluid.ui.main_module import start_gui


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

    # res = assembly.create_shapes()
    if res == '':
        print 'Shapes created'
    else:
        print '-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-'
        print 'Shapes creation error res = ', res
        print '-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-'

    # res = assembly.export_shapes('Test1.stl')
    if res == '':
        print 'Shapes exported'
    else:
        print '-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-'
        print 'Shapes export error res = ', res
        print '-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-'

    # assembly.show_shapes()

    # start_gui()

    # Testing is_inside algorithm:

    # mesh = assembly.extract_simphony_mesh()
    # print mesh

    # from nfluid.shapes.shapes import Shape

    # mesh = Shape.total_mesh
    # mesh.close()

    # print "mesh.coord_limits"
    # limits = mesh.coord_limits()
    # print limits

    # cube = mesh.generate_cubic_mesh(limits['x_min'],
    # limits['x_max'],limits['y_min'],limits['y_max'],
    # limits['z_min'],limits['z_max'], 0.5)

    # # print cube.vertices
    # inside = []
    # for v in cube.vertices.itervalues():
        # inside_r = mesh.is_inside(v)
        # # print inside_r
        # if inside_r is True:
        #     inside.append(v)

    # filename = 'inside_shapeall.xyz'
    # file_out = open(filename, 'w')

    # total_v = len(inside)
    # file_out.write('{}\n'.format(total_v))
    # file_out.write('---------------\n')
    # spec = 'O'
    # for v in inside:
        # file_out.write('{0} {1} {2} {3}\n'.format(spec, v[0], v[1], v[2]))

    # file_out.close()

    assembly.print_info_file('Assembly_info_after.txt')

    tree = assembly.get_tree_structure()
    print tree
    amplitude = tree.walk_amplitude()
    depth = tree.walk_depth()

    print "AMPLITUDE"
    for elem in amplitude:
        print elem.data

    print "DEPTH"
    for elem in depth:
        print elem.data

    from nfluid.ui.main_module import start_gui
    start_gui()

    # assembly.release_shapes()
