import random
import numpy as np
from nfluid.geometry.functions import distance, equal_vertices


class Segment3D():
    def __init__(self, a, b, normal):
        """a and b are the limits of the segment."""
        self.a = a
        self.b = b
        self.normal = normal

    def intersection(self, geometry):
        if isinstance(geometry, Line3D):
            line = Line3D(self.a, self.normal)
            inter = line.intersection(geometry)
            if inter is None:
                return None
            else:
                if (distance(self.a, inter) < distance(self.a, self.b) and
                   distance(self.b, inter) < distance(self.a, self.b) and
                   distance(line.a, inter) < distance(line.a, line.b) and
                   distance(line.b, inter) < distance(line.a, line.b)):
                    return inter
                else:
                    return None
        if isinstance(geometry, Segment3D):
            line = Line3D(self.a, self.normal)
            geo = Line3D(geometry.a, geometry.normal, geometry.b)
            inter = line.intersection(geo)
            if inter is None:
                return None
            else:
                if (distance(self.a, inter) < distance(self.a, self.b) and
                   distance(self.b, inter) < distance(self.a, self.b) and
                   distance(geo.a, inter) < distance(geo.a, geo.b) and
                   distance(geo.b, inter) < distance(geo.a, geo.b)):
                        return inter
                else:
                    return None


class Line3D():
    def __init__(self, a, normal, b=None):
        """a and b are points of the line"""
        self.a = a
        self.normal = normal
        if b is None:
            f = 1.0
            self.b = (a[0] + normal[0]*f,
                      a[1] + normal[1]*f,
                      a[2] + normal[2]*f)
        else:
            self.b = b

    def get_point(self, t=None, b=None):
        if b is None:
            b = self.b
        if t is None:
            t = random.random()
        x = self.a[0] + (b[0]-self.a[0]) * t
        y = self.a[1] + (b[1]-self.a[1]) * t
        z = self.a[2] + (b[2]-self.a[2]) * t
        return (x, y, z)

    def intersection(self, geometry):
        if isinstance(geometry, Plane):
            return geometry.intersection(self)
        if isinstance(geometry, Segment3D):
            return geometry.intersection(self)
        if isinstance(geometry, Line3D):
            p0 = geometry.a
            v0 = geometry.normal
            p1 = self.a
            v1 = self.normal
            matrix = [[v0[0], -v1[0]],
                      [v0[1], -v1[1]]]
            ind = [p1[0]-p0[0], p1[1]-p0[1]]
            x0 = 0
            y0 = 0
            z0 = 0
            x1 = 0
            y1 = 0
            z1 = 0
            try:
                s = np.linalg.solve(matrix, ind)
                x0 = p0[0]+v0[0]*s[0]
                y0 = p0[1]+v0[1]*s[0]
                z0 = p0[2]+v0[2]*s[0]
                x1 = p1[0]+v1[0]*s[1]
                y1 = p1[1]+v1[1]*s[1]
                z1 = p1[2]+v1[2]*s[1]
            except np.linalg.linalg.LinAlgError:
                matrix = [[v0[0], -v1[0]],
                          [v0[2], -v1[2]]]
                ind = [p1[0]-p0[0], p1[2]-p0[2]]
                try:
                    s = np.linalg.solve(matrix, ind)
                    x0 = p0[0]+v0[0]*s[0]
                    y0 = p0[1]+v0[1]*s[0]
                    z0 = p0[2]+v0[2]*s[0]
                    x1 = p1[0]+v1[0]*s[1]
                    y1 = p1[1]+v1[1]*s[1]
                    z1 = p1[2]+v1[2]*s[1]
                except np.linalg.linalg.LinAlgError:
                    matrix = [[v0[2], -v1[2]],
                              [v0[1], -v1[1]]]
                    ind = [p1[2]-p0[2], p1[1]-p0[1]]
                    try:
                        s = np.linalg.solve(matrix, ind)
                        x0 = p0[0]+v0[0]*s[0]
                        y0 = p0[1]+v0[1]*s[0]
                        z0 = p0[2]+v0[2]*s[0]
                        x1 = p1[0]+v1[0]*s[1]
                        y1 = p1[1]+v1[1]*s[1]
                        z1 = p1[2]+v1[2]*s[1]
                    except np.linalg.linalg.LinAlgError:
                        print "ERROR; CANT CALCULATE INTERSECTION"
                        return None
            if equal_vertices((x0, y0, z0), (x1, y1, z1)):
                return (x0, y0, z0)
            else:
                return None


class Plane():
    def __init__(self, point, normal):
        self.point = point
        self.normal = normal

    def get_point(self):
        if self.normal[0] != 0:
            z = random.random()
            y = random.random()
            x = self.point[0] - \
                ((self.normal[1]*(y-self.point[1]) +
                 self.normal[2]*(z-self.point[2])) /
                 self.normal[0])
            return (x, y, z)
        elif self.normal[1] != 0:
            x = random.random()
            z = random.random()
            y = self.point[1] - \
                ((self.normal[0]*(x-self.point[0]) +
                 self.normal[2]*(z-self.point[2])) /
                 self.normal[1])
            return (x, y, z)
        else:
            x = random.random()
            y = random.random()
            z = self.point[2] - \
                ((self.normal[1]*(y-self.point[1]) +
                 self.normal[0]*(x-self.point[0])) /
                 self.normal[2])
            return (x, y, z)

    def intersection(self, line):
        a_line = line.a
        b_line = line.b
        a0 = a_line[0]
        a1 = a_line[1]
        a2 = a_line[2]
        b0 = b_line[0]
        b1 = b_line[1]
        b2 = b_line[2]
        a = self.normal[0]
        b = self.normal[1]
        c = self.normal[2]
        x0 = self.point[0]
        y0 = self.point[1]
        z0 = self.point[2]
        t = ((a*x0 + b*y0 + c*z0 - a*a0 - b*a1 - c*a2) /
             ((a*b0 - a*a0 + b*b1 - b*a1 + c*b2 - c*a2))+0.0000000001)
        return line.get_point(t, b_line)
