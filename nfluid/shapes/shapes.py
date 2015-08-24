#!/usr/bin/python
# -*- coding: utf-8 -*-

from nfluid.geometry.generator import GeometryGenerator
_generator = GeometryGenerator()

class Shape(object):

    def __init__(self):
        # Geometric mesh
        self.mesh = None
        print 'Shape.__init__'

    def export(self, file):
        file.write('Shape export\n')
        print 'Shape.export'

    def show(self):
        print 'Shape.show'


class ShapeCap(Shape):

    def __init__(
        self, R, L,
        PosH
    ):
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
        self.SideA = A
        self.SideB = B
        self.length = L
        self.PosH = PosH
        self.PosT = PosT
        self.mesh = None
        print 'ShapeSquareCoupling'

