import random
import numpy as np
from nfluid.external.transformations import unit_vector

class Line3D():
    def __init__(self, a, normal, b=None):
        """a and b are points of the line"""
        self.a = a
        self.normal = normal
        f = 1.0
        self.b = (a[0] + normal[0]*f,
                  a[1] + normal[1]*f,
                  a[2] + normal[2]*f)

    # def _get_normal(self):
        # v = (b[0]-a[0],b[1]-a[1],b[2]-a[2])
        # return unit_vector(v)
    
    # normal = property(self._get_normal)
    
    def get_point(self,t,b=None):
        if b is None:
            b = self.b
        x = self.a[0] + (b[0]-self.a[0]) * t
        y = self.a[1] + (b[1]-self.a[1]) * t
        z = self.a[2] + (b[2]-self.a[2]) * t
        return (x,y,z)
    
    def intersection(self, plane):
        return plane.intersection(self)

class Plane():
    def __init__(self, point, normal):
        self.point = point
        self.normal = normal
    
    def get_point(self):
        if self.normal[0] != 0:
            z = random.random()
            y = random.random()
            x = self.point[0] - \
               (
                    (self.normal[1]*(y-self.point[1])+self.normal[2]*(z-self.point[2])) /\
                     self.normal[0]
               )
            return (x,y,z)
        elif self.normal[1] != 0:
            x = random.random()
            z = random.random()
            y = self.point[1] - \
               (
                    (self.normal[0]*(x-self.point[0])+self.normal[2]*(z-self.point[2])) /\
                     self.normal[1]
               )
            return (x,y,z)
        else:
            x = random.random()
            y = random.random()
            z = self.point[2] - \
               (
                    (self.normal[1]*(y-self.point[1])+self.normal[0]*(x-self.point[0])) /\
                     self.normal[2]
               )
            return (x,y,z)
         
    
    def intersection(self, line):
        x1 = self.point
        x2 = self.get_point()
        x3 = self.get_point()
        x4 = line.a
        x5 = line.b
        print 'x1',x1
        print 'x2',x2
        print 'x3',x3
        print 'x4',x4
        print 'x5',x5
        num = [[1,     1,     1,     1],
               [x1[0], x2[0], x3[0], x4[0]],
               [x1[1], x2[1], x3[1], x4[1]],
               [x1[2], x2[2], x3[2], x4[2]]]
        den = [[1,     1,     1,     0],
               [x1[0], x2[0], x3[0], x5[0]-x4[0]],
               [x1[1], x2[1], x3[1], x5[1]-x4[1]],
               [x1[2], x2[2], x3[2], x5[2]-x4[2]]]
        print 'num',num
        print 'den',den
        num_det = np.linalg.det(num)
        den_det = np.linalg.det(den)
        t = - (num_det / den_det)
        return line.get_point(t,x5)

