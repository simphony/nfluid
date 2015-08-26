#!/usr/bin/python
# -*- coding: utf-8 -*-

from nfluid.visualisation.show import show
from nfluid.geometry.generator import GeometryGenerator
_generator = GeometryGenerator()


def SetListElement(list, elt, n):
    for i in xrange(len(list), n + 1):
        list.append(None)
    list[n] = elt
#    print 'SetListElement', list

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

#WORKFLOW init, add_shape, add_shape ... , finalize,  ...use..., release
    @classmethod
    def init(cls):
        cls.shapes = ShapeContainer()
        cls.total_mesh = None

    @classmethod
    def finalize(cls):
        initial = cls.shapes.get_head()
        final = cls.shapes.get_tail()
        initial_mesh = initial.mesh
        
        cursor = initial
        cls.total_mesh = initial_mesh
        count = 0
        print "SHAPES!!!!"
        print cls.shapes
        print "initial"
        print initial
        print "final"
        print final
        while len(cursor.links_tail) != 0:
            # WE ASSUME FOR THE MOMENT THAT WE DONT HAVE TEE PIECES
            print "THE MEEEEHHHH {}".format(count)
            print "cursor"
            print cursor
            tail = cursor.links_tail[0]
            print "tail"
            print tail
            # HERE WE SHOULD MAKE ALL THE OPERATIONS RELATED WITH ORIENTATION
            cls.total_mesh = cls.total_mesh.link(tail.mesh)
            count += 1
            cursor = tail
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
        cls.total_mesh.export(file_name)

    @classmethod
    def show(cls):
        if cls.total_mesh is None:
            raise Exception('Total mesh not generated!')
        show([cls.total_mesh])

    def __init__(self):
        # Geometric mesh
        self.mesh = None
        print 'Shape.__init__'
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

    # def export(self, file):
        # file.write('Shape export\n')
        # print 'Shape.export'

    # def show(self):
        # print 'Shape.show'


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
        print 'ShapeCap'


class ShapeCircleCoupling(Shape):

    def __init__(
        self, R, L,
        PosH, PosT
    ):
        Shape.__init__(self)        
        self.Radius = R
        self.Length = L
        self.mesh = _generator.create_coupling(self.Radius, self.Length)
        self.PosH = PosH
        self.PosT = PosT
        print 'ShapeCircleCoupling'

class ShapeTee(Shape):

    def __init__(
        self, R,
        PosH, PosT0, PosT1
    ):
        Shape.__init__(self)        
        self.Radius = R
        self.PosH = PosH
        self.PosT0 = PosT0
        self.PosT1 = PosT1
        print 'ShapeTee'

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
        print 'ShapeTee3'
        
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
        print 'ShapeTee4'


class ShapeFlowAdapter(Shape):

    def __init__(
        self, RH, RT, L,
        PosH, PosT
    ):
        Shape.__init__(self)        
        self.RadiusH = RH
        self.RadiusT = RT
        self.Length = L
        self.PosH = PosH
        self.PosT = PosT
        self.mesh = _generator.create_flow_adapter(self.RadiusH,
                                                   self.RadiusT,
                                                   self.Length)
        print 'ShapeFlowAdapter'


# TODO R, RC vs R1, R2

class ShapeLongElbow(Shape):

    def __init__(
        self, RC, R,
        PosH, PosT,
    ):
        Shape.__init__(self)        
        # Curvature radius
        self.RadiusCurvature = RC
        # Gate radius
        self.Radius = R
        self.PosH = PosH
        self.PosT = PosT
        self.mesh = _generator.create_long_elbow(self.Radius,
                                                 self.RadiusCurvature)
        print 'ShapeLongElbow'

class ShapeLongElbowAngle(Shape):

    def __init__(
        self, RC, Angle, R,
        PosH, PosT,
    ):
        Shape.__init__(self)        
        # Curvature radius
        self.RadiusCurvature = RC
        self.angle = Angle
        # Gate radius
        self.Radius = R
        self.PosH = PosH
        self.PosT = PosT
        self.mesh = _generator.create_long_elbow(self.Radius,
                                                 self.RadiusCurvature,
                                                 self.angle)
        print 'ShapeLongElbow'


class ShapeShortElbow(Shape):

    def __init__(
        self, R,
        PosH, PosT,
    ):
        Shape.__init__(self)        
        self.Radius = R
        self.PosH = PosH
        self.PosT = PosT
        self.mesh = _generator.create_short_elbow(self.Radius)
        print 'ShapeShortElbow'

class ShapeShortElbowAngle(Shape):

    def __init__(
        self, Angle, R,
        PosH, PosT,
    ):
        self.Radius = R
        self.angle = Angle
        self.PosH = PosH
        self.PosT = PosT
        self.mesh = _generator.create_short_elbow(self.Radius, self.angle)
        print 'ShapeShortElbow'



class ShapeSphericCoupling(Shape):

    def __init__(
        self, RS, R,
        PosH, PosT
    ):
        Shape.__init__(self)        
        # Sphere radius
        self.RadiusSphere = RS
        # Gate radius equal for both gates
        self.Radius = R
        self.PosH = PosH
        self.PosT = PosT
        self.mesh = _generator.create_spheric_coupling(self.Radius,
                                                       self.RadiusSphere)
        print 'ShapeSphericCoupling'


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
        print 'ShapeSquareCoupling'


def CreateShape(type, center, rotation, 
    par0 = None, par1 = None, par2 = None, 
    par3 = None, par4 = None, par5 = None):
    
    shape = None

    if type == 'cap':
        shape = ShapeCap(par0, par1, par2)
    elif type == 'circle_coupling':
        shape = ShapeCircleCoupling(par0, par1, par2, par3)
    elif type == 'circle_tee':
        shape = ShapeTee(par0, par1, par2, par3)
    elif type == 'circle_tee3':
        shape = ShapeTee3(par0, par1, par2, par3, par4)
    elif type == 'circle_tee4':
        shape = ShapeTee4(par0, par1, par2, par3, par4, par5)
    elif type == 'flow_adapter':
        shape = ShapeFlowAdapter(par0, par1, par2, par3, par4)
    elif type == 'long_elbow':
        shape = ShapeLongElbow(par0, par1, par2, par3)
    elif type == 'long_elbow_angle':
        shape = ShapeLongElbowAngle(par0, par1, par2, par3, par4)
    elif type == 'short_elbow':
        shape = ShapeShortElbow(par0, par1, par2)
    elif type == 'spheric_coupling':
        shape = ShapeSphericCoupling(par0, par1, par2, par3)
    elif type == 'square_coupling':
        shape = ShapeSquareCoupling(par0, par1, par2, par3, par4)
    else:
        print 'Unknown shape type'

    return shape
