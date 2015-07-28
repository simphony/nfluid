#!/usr/bin/python
# -*- coding: utf-8 -*-


class Shape(object):

    def __init__(self):
        print 'Shape.__init__'

    def export(self, file):
        file.write('Shape export\n')
        print 'Shape.export'

    def show(self):
        print 'Shape.show'


class ShapeCircleCoupling(Shape):

    def __init__(
        self, R, L,
        PosH, PosT
    ):
        self.Radius = R
        self.Length = L
        self.PosH = PosH
        self.PosT = PosT
        print 'ShapeCircleCoupling'


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

        print 'ShapeFlowAdapter'


class ShapeShortElbow(Shape):

    def __init__(
        self, R,
        PosH, PosT,
    ):
        self.Radius = R
        self.PosH = PosH
        self.PosT = PosT

        print 'ShapeShortElbow'


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

        print 'ShapeLongElbow'


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

        print 'ShapeSphericCoupling'


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

        print 'ShapeCap'
