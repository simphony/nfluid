from nfluid.geometry.geometricmesh import Circle3D, CylindricalPart, Arc3D
from nfluid.external.transformations import unit_vector
# from nfluid.external.transformations import angle_between_vectors
from nfluid.geometry.functions import angle_between_vectors
from nfluid.geometry.auxiliar_geometry import Line3D, Plane
from nfluid.external.transformations import vector_norm
import math


class CouplingPath(CylindricalPart):
    def __init__(self, r, points, slices, stacks):
        super(CouplingPath, self).__init__()
        self.r = r
        self.points = list(points)
        params = self._calculate_points(r, points, stacks)
        first_p = params['points'][0]
        first_n = params['normals'][0]
        proc_p = params['points'][1:]
        proc_n = params['normals'][1:]
        res = Circle3D(r, slices, pos=first_p, normal=first_n)
        prev_circle = Circle3D(r, slices, pos=first_p, normal=first_n)
        for i in xrange(len(proc_p)):
            new_circle = Circle3D(r, slices, pos=proc_p[i], normal=proc_n[i])
            new_circle = prev_circle.adapt(new_circle)
            prev_circle = new_circle
            res = res.connect(new_circle)
        part = res
        self.copy_from_cylindricalpart(part)

    def _calculate_points(self, r, points, stacks):
        """Calculates points and normals of the circles that will compound
        the coupling path piece."""
        res = {}
        res['points'] = [points[0]]
        first_v = unit_vector((points[1][0]-points[0][0],
                               points[1][1]-points[0][1],
                               points[1][2]-points[0][2]))
        res['normals'] = [first_v]
        last_p = points[0]
        c_points = points[1:-1]

        for i in xrange(len(c_points)):
            c_p = c_points[i]
            # next point
            f_p = points[i+2]
            # previous point
            b_p = points[i]
            cur_bv = unit_vector((c_p[0]-b_p[0],
                                  c_p[1]-b_p[1],
                                  c_p[2]-b_p[2]))
            cur_fv = unit_vector((f_p[0]-c_p[0],
                                  f_p[1]-c_p[1],
                                  f_p[2]-c_p[2]))
            angle = angle_between_vectors(cur_bv, cur_fv)
            if angle != 0 and angle != math.pi and math.isnan(angle) is False:
                inter_points = self._interporlate(r, b_p, c_p, f_p, stacks)
                for i in xrange(inter_points.n_vertices()):
                    res['points'].append(inter_points.vertex(i))
                res['normals'].append(cur_bv)
                for i in xrange(inter_points.n_vertices()-2):
                    last_p = inter_points.vertex(i)
                    # p = inter_points.vertex(i+1)
                    next_p = inter_points.vertex(i+2)
                    cur_n = unit_vector((next_p[0]-last_p[0],
                                         next_p[1]-last_p[1],
                                         next_p[2]-last_p[2]))
                    res['normals'].append(cur_n)
                res['normals'].append(cur_fv)
            else:
                res['points'].append(c_p)
                res['normals'].append(cur_fv)

        res['points'].append(points[-1])
        last_v = unit_vector((points[-1][0]-points[-2][0],
                              points[-1][1]-points[-2][1],
                              points[-1][2]-points[-2][2]))
        res['normals'].append(last_v)
        return res

    def _interporlate(self, r, p0, p1, p2, stacks):
        """This will separate p1 in two different points"""
        v01 = unit_vector((p1[0]-p0[0], p1[1]-p0[1], p1[2]-p0[2]))
        v10 = unit_vector((p0[0]-p1[0], p0[1]-p1[1], p0[2]-p1[2]))
        v12 = unit_vector((p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2]))

        bisect_normal = unit_vector(((v10[0]+v12[0])/2, (v10[1]+v12[1])/2,
                                    (v10[2]+v12[2])/2))
        bisect_line = Line3D(p1, bisect_normal)
        p01mid = ((p0[0]+p1[0])/2.0, (p0[1]+p1[1])/2.0, (p0[2]+p1[2])/2.0)
        p12mid = ((p2[0]+p1[0])/2.0, (p2[1]+p1[1])/2.0, (p2[2]+p1[2])/2.0)

        plane1 = Plane(p01mid, v01)
        plane2 = Plane(p12mid, v12)

        inter1 = plane1.intersection(bisect_line)
        inter2 = plane2.intersection(bisect_line)

        d1 = abs(vector_norm((p1[0]-inter1[0], p1[1]-inter1[1],
                 p1[2]-inter1[2])))
        d2 = abs(vector_norm((p1[0]-inter2[0], p1[1]-inter2[1],
                 p1[2]-inter2[2])))

        if d1 < d2:
            mid_max = inter1
        else:
            mid_max = inter2

        # this is the minimal distance point that assures a 90 elbow, so the
        angle = angle_between_vectors(v01, v12)
        angle = (math.pi-angle)

        # distance between equidistant point from (p01 and p12)
        d = r / math.sin(angle/2)
        # distance of the points along p01 and p12
        l = d * math.cos(angle/2)

        p01min = (p1[0]-(v01[0]*l), p1[1]-(v01[1]*l), p1[2]-(v01[2]*l))
        # p12min = (p1[0]+(v12[0]*l), p1[1]+(v12[1]*l), p1[2]+(v12[2]*l))
        plane1 = Plane(p01min, v01)
        mid_min = plane1.intersection(bisect_line)

        # to avoid problems, me calculate as a midpoint another point along
        # the line bisector line
        b_vector = (mid_min[0]-mid_max[0], mid_min[1]-mid_max[1],
                    mid_min[2]-mid_max[2])
        # factor between 0 and 1: closer to 0 means more curve
        factor = 0.2
        midpoint = (mid_max[0]+b_vector[0]*factor,
                    mid_max[1]+b_vector[1]*factor,
                    mid_max[2]+b_vector[2]*factor)

        # recalculate starting and ending points of the arc:
        line1 = Line3D(p0, v01)
        line2 = Line3D(p1, v12)
        plane1 = Plane(midpoint, v01)
        plane2 = Plane(midpoint, v12)
        p01 = plane1.intersection(line1)
        p12 = plane2.intersection(line2)

        return Arc3D(stacks, p01, p12, midpoint)
