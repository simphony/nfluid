#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import copy

import nfluid.visualisation.show as show_mod
from nfluid.geometry.generator import GeometryGenerator
from nfluid.geometry.functions import angle_between_vectors
_generator = GeometryGenerator()


def SetListElement(list, elt, n):
    for i in xrange(len(list), n + 1):
        list.append(None)
    list[n] = elt


class ShapeContainer(list):
    """Extended list class for Shape elements to make algorithms easier.

    """
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
    """Base exchange class between Channel Assembly and Elements and the
    Geometry Generator (final triangular meshes). It contains the
    minimum info for the geometry generator to work.

    Also has the algorithms to obtain the full assembly structure in
    s single mesh, using the geometry generator and its methods.

    Class Attributes
    ----------------
        shapes : ShapeContainer
            iterable of the shapes
        total_mesh : GeometricMesh
            the full triangular mesh of the assembly
        slices : int
            the vertical divisions of each element in the assembly
        stacks : int
            the horizontal divisions of each element in the assembly

    Attributes
    ----------
        mesh : GeometricMesh
            the triangular mesh of the shape
        links_head : iterable
            the pieces linked to the head of the shape
        links_tail : iterable
            the pieces linked to the tail of the shape

    """
    shapes = ShapeContainer()
    total_mesh = None

# WORKFLOW init, add_shape, add_shape ... , finalize,  ...use..., release
    @classmethod
    def init(cls, gates_sides, elements_divisions):
        """Initiates the data structures so they are ready to work with

        Parameters
        ----------
        gates_sides : int
            vertical slices
        elements_divisions : int
            horizontal slices

        """
        cls.shapes = ShapeContainer()
        cls.total_mesh = None
        cls.slices = gates_sides
        cls.stacks = elements_divisions
        _generator.slices = gates_sides
        _generator.stacks = elements_divisions

    @classmethod
    def connect_next_piece(cls, cursor, initial_gate=0):
        """Connects the pieces linked to the current piece, this means:
            - create the meshes of the pieces linked, in order
            - "link" them (in the geometry generator: attach, adapt, connect)
            - take care of the special orientations of certain pieces (like
              the elbows, or circle path)
            - keep connecting the rest of the pieces

        It keeps updating the total_mesh class attribute.

        Parameters
        ----------
        cursor : Shape
            current piece in the chain
        initial_gate : int
            this indicates in which gate of the total mesh its going to be
            added the first piece linked to the current piece


        """
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
                        isinstance(tail, ShapeShortElbowAngle) or
                        isinstance(tail, ShapeTee) or
                        isinstance(tail, ShapeCirclePath)):
                    if isinstance(tail, ShapeTee):
                        normal_tail = (tail.NormalT0.X(0), tail.NormalT0.X(1),
                                       tail.NormalT0.X(2))
                    else:
                        normal_tail = (tail.NormalT.X(0), tail.NormalT.X(1),
                                       tail.NormalT.X(2))
                    tail.mesh = cls.total_mesh.attach(tail.mesh, gate)
                    c, normal_tail_current = tail.mesh.get_face_info(1)
                    angle = angle_between_vectors(normal_tail,
                                                  normal_tail_current)
                    iter = 100
                    while angle > 0.001 and iter:
                        tail.mesh.set_orientation(math.degrees(angle))
                        c, normal_tail_current = tail.mesh.get_face_info(1)
                        angle = angle_between_vectors(normal_tail,
                                                      normal_tail_current)
                        iter -= 1
                    # if iter == 0:
                    #   iter = 100
                    # while angle > 0.001 and iter:
                    #   angle = math.pi - angle
                    #   tail.mesh.set_orientation(math.degrees(angle))
                    #   c, normal_tail_current = tail.mesh.get_face_info(1)
                    #   angle = angle_between_vectors(normal_tail,
                    #                           normal_tail_current)
                    #   iter -= 1
                    #   print angle
                    #   print normal_tail_current
                    tail.mesh = cls.total_mesh.adapt(tail.mesh, gate)
                    cls.total_mesh = cls.total_mesh.connect(tail.mesh, gate)
                else:
                    cls.total_mesh = cls.total_mesh.link(tail.mesh, gate)
                cur_gate = gate
                gate += 1
                if isinstance(tail, ShapeTee):
                    # gate += 1
                    new_paths += 1
                if isinstance(tail, ShapeCap):
                    new_paths -= 1
                new_paths += Shape.connect_next_piece(tail, cur_gate)
                gate += new_paths
            else:
                gate += 1
        return new_paths

    @classmethod
    def finalize(cls):
        """Method that sets up the things to start building the total
        triangular mesh of the assembly. It calls connect_next_piece method
        with the first piece of the assembly after positioning it in the
        space.

        """
        if len(cls.shapes) != 0:
            initial = cls.shapes.get_head()
            initial_mesh = initial.mesh
            pos = (initial.PosH.X(0), initial.PosH.X(1), initial.PosH.X(2))
            dir = (initial.NormalH.X(0), initial.NormalH.X(1),
                   initial.NormalH.X(2))
            initial_mesh.move(point=pos, direction=dir)
            if (isinstance(initial, ShapeLongElbowAngle) or
                    isinstance(initial, ShapeShortElbowAngle) or
                    isinstance(initial, ShapeTee) or
                    isinstance(initial, ShapeCirclePath)):
                if isinstance(initial, ShapeTee):
                    normal_tail = (initial.NormalT0.X(0),
                                   initial.NormalT0.X(1),
                                   initial.NormalT0.X(2))
                else:
                    normal_tail = (initial.NormalT.X(0), initial.NormalT.X(1),
                                   initial.NormalT.X(2))
                c, normal_tail_current = initial_mesh.get_face_info(1)
                angle = angle_between_vectors(normal_tail,
                                              normal_tail_current)
                iter = 100
                while angle > 0.001 and iter:
                    initial_mesh.set_orientation(math.degrees(angle))
                    c, normal_tail_current = initial_mesh.get_face_info(1)
                    angle = angle_between_vectors(normal_tail,
                                                  normal_tail_current)
                    iter -= 1

            cursor = initial
            cls.total_mesh = initial_mesh
            cls.connect_next_piece(cursor, 0)
        return ''

    @classmethod
    def release(cls):
        """Clears the shapes and the full triangular mesh.

        """
        cls.shapes = ShapeContainer()
        cls.total_mesh = None

    @classmethod
    def add_shape(cls, shape):
        """Adds a new shape to the container.

        Parameters
        ----------
        shape : Shape
            new shape to be added

        """
        if shape is not None:
            cls.shapes.append(shape)

    @classmethod
    def export(cls, file_name, close=False):
        """Exports the total mesh to STL format.

        Parameters
        ----------
            file_name : string
                name of the file to export to
            close : boolean
                indicates if the mesh should be close in all its gates
                or not before exporting it

        """
        if cls.total_mesh is None:
            raise Exception('Total mesh not generated!')
        res = copy.deepcopy(cls.total_mesh)
        if close is True:
            res.close()
        res.export(file_name)
        res = None

    @classmethod
    def simphony_mesh(cls):
        """Extracts the SimPhoNy Mesh of the current total mesh.

        """
        if cls.total_mesh is None:
            raise Exception('Total mesh not generated!')
        return cls.total_mesh.to_simphony_mesh()

    @classmethod
    def show(cls):
        """Opens a visvis visualizer with the total mesh.

        """
        if cls.total_mesh is None:
            raise Exception('Total mesh not generated!')
        show_mod.show([cls.total_mesh])

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
    """Factory function that creates the correct Shape according to
    the parameters sent.

    Parameters
    ----------
        type : string
            indicates which shape should be created
        center : Vector
            center point of the piece
        rotation : Operator
            rotation matrix of all transformations made to the geometry
            of the shape

    Returns
    -------
        A concrete Shape witht the rest of the parameters (par0 to par6)

    """
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
    elif type == 'long_elbow_angle':
        shape = ShapeLongElbowAngle(par0, par1, par2, par3, par4, par5, par6)
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
