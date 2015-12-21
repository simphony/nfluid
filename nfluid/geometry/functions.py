from math import cos, sin, pi, asin
from nfluid.external.transformations import vector_product
from nfluid.external.transformations import unit_vector
from nfluid.external.transformations import vector_norm

global_eps = 0.0001


def cos_table(size, angle=2.0*pi):
    # initial = pi*0.25
    initial = pi
    step_angle = angle / size
    return [cos(x*step_angle + initial) for x in xrange(size+1)]


def sin_table(size, angle=2.0*pi):
    # initial = pi*0.25
    initial = pi
    step_angle = angle / size
    return [sin(x*step_angle + initial) for x in xrange(size+1)]


def equal_vertices(v1, v2, eps=global_eps):
    return ((abs(v1[0]-v2[0]) <= eps) and
            (abs(v1[1]-v2[1]) <= eps) and
            (abs(v1[2]-v2[2]) <= eps))


def normal_of(p1, p2, p3):
    v1 = (p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2])
    v2 = (p3[0]-p1[0], p3[1]-p1[1], p3[2]-p1[2])
    return unit_vector(vector_product(v1, v2))


def center_of(points):
    tx = 0.0
    ty = 0.0
    tz = 0.0
    for p in points:
        tx += p[0]
        ty += p[1]
        tz += p[2]
    n_points = len(points)
    return (tx/n_points, ty/n_points, tz/n_points)


def angle_between_vectors(v0, v1):
    n_mod = vector_norm(vector_product(v0, v1))
    v0_mod = vector_norm(v0)
    v1_mod = vector_norm(v1)
    return asin(n_mod/(v0_mod*v1_mod))


def distance(p0, p1):
    v = [p1[0]-p0[0], p1[1]-p0[1], p1[2]-p0[2]]
    return vector_norm(v)
