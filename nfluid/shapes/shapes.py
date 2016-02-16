#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import copy

from nfluid.visualisation.show import show
from nfluid.geometry.generator import GeometryGenerator
from nfluid.geometry.functions import angle_between_vectors
_generator = GeometryGenerator()


def SetListElement(list, elt, n):
    for i in xrange(len(list), n + 1):
        list.append(None)
    list[n] = elt


class ShapeContainer(list):
    def get_head(self):
        for e in self:
            if len(e.links_head) == 0:
                return e
        return None

    def get_tail(self):
        tails = []
        for e in self:
            if len(e.links_tail) == 0:
                tails.append(e)
        return tails


class Shape(object):
    shapes = ShapeContainer()
    total_mesh = None

# WORKFLOW init, add_shape, add_shape ... , finalize,  ...use..., release
    @classmethod
    def init(cls, gates_sides, elements_divisions):
        cls.shapes = ShapeContainer()
        cls.total_mesh = None
        cls.slices = gates_sides
        cls.stacks = elements_divisions
        _generator.slices = gates_sides
        _generator.stacks = elements_divisions

    @classmethod
    def connect_next_piece(cls, cursor, initial_gate=0):
        gate = initial_gate
        # current_element = type(cursor).__name__
        # linked_elements = ''
        # for tail in cursor.links_tail:
        #     linked_elements = linked_elements + type(tail).__name__ + ' '
        # if not cursor.links_tail:
        #     linked_elements = 'None'
        # print 'Gate', gate, 'at', current_element, \
        #       'linked to', linked_elements

        # We accumulate and return the number of new paths opened, so the
        # connections in upper levels will be done correctly
        new_paths = 0
        for tail in cursor.links_tail:
            if tail is not None:
                if (isinstance(tail, ShapeLongElbowAngle) or
                        isinstance(tail, ShapeTee) or
                        isinstance(tail, ShapeShortElbowAngle) or
                        isinstance(tail, ShapeCirclePath)):
                    if isinstance(tail, ShapeTee):
                        normal_tail = (tail.NormalT0.X(0), tail.NormalT0.X(1),
                                       tail.NormalT0.X(2))
                    else:
                        normal_tail = (tail.NormalT.X(0), tail.NormalT.X(1),
                                       tail.NormalT.X(2))
                    tail.mesh = cls.total_mesh.attach(tail.mesh, gate)
                    c, normal_tail_current = tail.mesh.get_face_info(1)
                    print "normal_tail", normal_tail
                    print "normal_tail_current", normal_tail_current
                    angle = angle_between_vectors(normal_tail,
                                                  normal_tail_current)
                    iter = 100
                    print "angle beg"
                    print angle
                    print normal_tail_current
                    while angle > 0.001 and iter:
                        tail.mesh.set_orientation(math.degrees(angle))
                        c, normal_tail_current = tail.mesh.get_face_info(1)
                        angle = angle_between_vectors(normal_tail,
                                                      normal_tail_current)
                        iter -= 1
                        print angle
                        print normal_tail_current
                    print "angle_end"
                    if iter == 0:
                        iter = 100
                    # while angle > 0.001 and iter:
                        # angle = math.pi - angle
                        # tail.mesh.set_orientation(math.degrees(angle))
                        # c, normal_tail_current = tail.mesh.get_face_info(1)
                        # angle = angle_between_vectors(normal_tail,
                        #                             normal_tail_current)
                        # iter -= 1
                    tail.mesh = cls.total_mesh.adapt(tail.mesh, gate)
                    cls.total_mesh = cls.total_mesh.connect(tail.mesh, gate)
                else:
                    cls.total_mesh = cls.total_mesh.link(tail.mesh, gate)
                cur_gate = gate
                gate += 1
                if isinstance(tail, ShapeTee):
                    # gate += 1
                    new_paths += 1
                new_paths += Shape.connect_next_piece(tail, cur_gate)
                gate += new_paths
            else:
                gate += 1
        return new_paths

    @classmethod
    def finalize(cls):
        if len(cls.shapes) != 0:
            initial = cls.shapes.get_head()
            initial_mesh = initial.mesh
            pos = (initial.PosH.X(0), initial.PosH.X(1), initial.PosH.X(2))
            dir = (initial.NormalH.X(0), initial.NormalH.X(1),
                   initial.NormalH.X(2))
            initial_mesh.move(point=pos, direction=dir)
            
            if (isinstance(initial, ShapeLongElbowAngle) or
                    isinstance(initial, ShapeShortElbowAngle) or
                    isinstance(initial, ShapeLongElbow) or
                    isinstance(initial, ShapeTee) or
                    isinstance(initial, ShapeShortElbow) or
                    isinstance(initial, ShapeCirclePath)):
                if isinstance(initial, ShapeTee):
                    normal_tail = (initial.NormalT0.X(0), initial.NormalT0.X(1),
                                   initial.NormalT0.X(2))
                else:
                    normal_tail = (initial.NormalT.X(0), initial.NormalT.X(1),
                                   initial.NormalT.X(2))
                c, normal_tail_current = initial_mesh.get_face_info(1)
                print "normal_tail", normal_tail
                print "normal_tail_current", normal_tail_current
                angle = angle_between_vectors(normal_tail,
                                              normal_tail_current)
                iter = 100
                print "angle beg"
                print angle
                print normal_tail_current
                while angle > 0.001 and iter:
                    initial_mesh.set_orientation(math.degrees(angle))
                    c, normal_tail_current = initial_mesh.get_face_info(1)
                    angle = angle_between_vectors(normal_tail,
                                                  normal_tail_current)
                    iter -= 1
                    print angle
                    print normal_tail_current
                print "angle_end"
            
            cursor = initial
            cls.total_mesh = initial_mesh
            cls.connect_next_piece(cursor, 0)
        return ''

    @classmethod
    def release(cls):
        cls.shapes = ShapeContainer()
        cls.total_mesh = None

    @classmethod
    def add_shape(cls, shape):
        if shape is not None:
            cls.shapes.append(shape)

    @classmethod
    def export(cls, file_name):
        if cls.total_mesh is None:
            raise Exception('Total mesh not generated!')
        res = copy.deepcopy(cls.total_mesh)
        res.close()
        res.export(file_name)

    @classmethod
    def simphony_mesh(cls):
        if cls.total_mesh is None:
            raise Exception('Total mesh not generated!')
        return cls.total_mesh.to_simphony_mesh()

    @classmethod
    def show(cls):
        if cls.total_mesh is None:
            raise Exception('Total mesh not generated!')
        show([cls.total_mesh])

    def __init__(self):
        # Geometric mesh
        self.mesh = None
        self.links_head = []
        self.links_tail = []

    def add_link_head(self, shape):
        self.links_head.append(shape)

    def add_link_tail(self, shape):
        self.links_tail.append(shape)

    def set_link_head(self, n, shape):
        SetListElement(self.links_head, shape, n)

    def set_link_tail(self, n, shape):
        SetListElement(self.links_tail, shape, n)


class ShapeCap(Shape):

    def __init__(
        self, R, L,
        PosH
    ):
        Shape.__init__(self)
        # Gate radius
        self.Radius = R
        # Cap length
        self.Length = L
        self.PosH = PosH
        self.mesh = _generator.create_cap(self.Radius, self.Length)


class ShapeCircleCoupling(Shape):

    def __init__(
        self, R, L,
        PosH, PosT,
        NormalH
    ):
        Shape.__init__(self)
        self.Radius = R
        self.Length = L
        self.mesh = _generator.create_coupling(self.Radius, self.Length)
        self.PosH = PosH
        self.PosT = PosT
        self.NormalH = NormalH


class ShapeTee(Shape):

    def __init__(
        self, R,
        PosH, PosT0, PosT1, NormalH,
        NormalT0
    ):
        Shape.__init__(self)
        self.Radius = R
        self.PosH = PosH
        self.PosT0 = PosT0
        self.PosT1 = PosT1
        self.NormalH = NormalH
        self.NormalT0 = NormalT0
        self.mesh = _generator.create_tee(self.Radius)


class ShapeTee3(Shape):

    def __init__(
        self, R,
        PosH, PosT0, PosT1, PosT2
    ):
        Shape.__init__(self)
        self.Radius = R
        self.PosH = PosH
        self.PosT0 = PosT0
        self.PosT1 = PosT1
        self.PosT2 = PosT2


class ShapeTee4(Shape):

    def __init__(
        self, R,
        PosH, PosT0, PosT1, PosT2, PosT3
    ):
        Shape.__init__(self)
        self.Radius = R
        self.PosH = PosH
        self.PosT0 = PosT0
        self.PosT1 = PosT1
        self.PosT2 = PosT2
        self.PosT3 = PosT3


class ShapeFlowAdapter(Shape):

    def __init__(
        self, RH, RT, L,
        PosH, PosT,
        NormalH
    ):
        Shape.__init__(self)
        self.RadiusH = RH
        self.RadiusT = RT
        self.Length = L
        self.PosH = PosH
        self.PosT = PosT
        self.NormalH = NormalH
        self.mesh = _generator.create_flow_adapter(self.RadiusH,
                                                   self.RadiusT,
                                                   self.Length)


class ShapeLongElbow90(Shape):

    def __init__(
        self, RC, R,
        PosH, PosT,
        NormalH, NormalT
    ):
        Shape.__init__(self)
        # Curvature radius
        self.RadiusCurvature = RC
        # Gate radius
        self.Radius = R
        self.PosH = PosH
        self.PosT = PosT
        self.NormalH = NormalH
        self.NormalT = NormalT
        self.mesh = _generator.create_long_elbow(self.RadiusCurvature,
                                                 self.Radius
                                                 )


class ShapeLongElbowAngle(Shape):

    def __init__(
        self, RC, Angle, R,
        PosH, PosT,
        NormalH, NormalT
    ):
        Shape.__init__(self)
        # Curvature radius
        self.RadiusCurvature = RC
        self.angle = Angle
        # Gate radius
        self.Radius = R
        self.PosH = PosH
        self.PosT = PosT
        self.NormalH = NormalH
        self.NormalT = NormalT
        self.mesh = _generator.create_long_elbow(self.RadiusCurvature,
                                                 self.Radius,
                                                 self.angle)


class ShapeShortElbow90(Shape):

    def __init__(
        self, R,
        PosH, PosT,
        NormalH, NormalT
    ):
        Shape.__init__(self)
        self.Radius = R
        self.PosH = PosH
        self.PosT = PosT
        self.NormalH = NormalH
        self.NormalT = NormalT
        self.mesh = _generator.create_short_elbow(self.Radius)


class ShapeShortElbowAngle(Shape):

    def __init__(
        self, R, Angle,
        PosH, PosT,
        NormalH, NormalT
    ):
        Shape.__init__(self)
        self.Radius = R
        self.angle = Angle
        self.PosH = PosH
        self.PosT = PosT
        self.NormalH = NormalH
        self.NormalT = NormalT
        self.mesh = _generator.create_short_elbow(self.Radius, self.angle)


class ShapeSphericCoupling(Shape):

    def __init__(
        self, RS, R,
        PosH, PosT,
        NormalH
    ):
        Shape.__init__(self)
        # Sphere radius
        self.RadiusSphere = RS
        # Gate radius equal for both gates
        self.Radius = R
        self.PosH = PosH
        self.PosT = PosT
        self.NormalH = NormalH
        self.mesh = _generator.create_spheric_coupling(self.Radius,
                                                       self.RadiusSphere)


class ShapeCirclePath(Shape):

    def __init__(
        self, R, P,
        PosH, PosT,
        NormalH, NormalT
    ):
        Shape.__init__(self)
        self.Radius = R  # Gate radius equal for both gates
        self.Points = P  # List of points in the path
        self.PosH = PosH
        self.PosT = PosT
        self.NormalH = NormalH
        self.NormalT = NormalT
        self.mesh = _generator.create_coupling_path(self.Radius, self.Points)


class ShapeSquareCoupling(Shape):

    def __init__(
        self, A, B, L,
        PosH, PosT
    ):
        Shape.__init__(self)
        self.SideA = A
        self.SideB = B
        self.length = L
        self.PosH = PosH
        self.PosT = PosT
        self.mesh = None


def CreateShape(type, center, rotation,
                par0=None, par1=None, par2=None,
                par3=None, par4=None, par5=None,
                par6=None):

    shape = None

    if type == 'cap':
        shape = ShapeCap(par0, par1, par2)
    elif type == 'circle_coupling':
        shape = ShapeCircleCoupling(par0, par1, par2, par3, par4)
    elif type == 'circle_tee':
        shape = ShapeTee(par0, par1, par2, par3, par4, par5)
    elif type == 'circle_tee3':
        shape = ShapeTee3(par0, par1, par2, par3, par4)
    elif type == 'circle_tee4':
        shape = ShapeTee4(par0, par1, par2, par3, par4, par5)
    elif type == 'flow_adapter':
        shape = ShapeFlowAdapter(par0, par1, par2, par3, par4, par5)
    elif type == 'long_elbow_90':
        shape = ShapeLongElbow90(par0, par1, par2, par3, par4, par5)
    elif type == 'long_elbow_angle':
        shape = ShapeLongElbowAngle(par0, par1, par2, par3, par4, par5, par6)
    elif type == 'short_elbow_90':
        shape = ShapeShortElbow90(par0, par1, par2, par3, par4)
    elif type == 'short_elbow_angle':
        shape = ShapeShortElbowAngle(par0, par1, par2, par3, par4, par5)
    elif type == 'spheric_coupling':
        shape = ShapeSphericCoupling(par0, par1, par2, par3, par4)
    elif type == 'circle_path':
        shape = ShapeCirclePath(par0, par1, par2, par3, par4, par5)
    elif type == 'square_coupling':
        shape = ShapeSquareCoupling(par0, par1, par2, par3, par4)
    else:
        print 'Unknown shape type'

    return shape
