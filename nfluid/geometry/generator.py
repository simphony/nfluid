from nfluid.geometry.geometricmesh import GeometricMesh, Circle3D, CylindricalPart, Arc3D
from nfluid.external.transformations import rotation_matrix
from nfluid.external.transformations import angle_between_vectors
# from nfluid.geometry.functions import angle_between_vectors
from nfluid.external.transformations import vector_product
from nfluid.external.transformations import unit_vector
from nfluid.external.transformations import vector_norm
from nfluid.geometry.functions import cos_table, sin_table
from nfluid.geometry.auxiliar_geometry import Line3D, Plane
import random
import math
import copy
from math import pow
import numpy as np


class GeometryGenerator():
    """Class to create and generate the vertices, normals and triangles of
    the different pieces of nfluid.
    """
    
    def __init__(self, slices=30, stacks=15):
        # BOTH SHOULD BE NON-WRITE!!!!
        self.slices = slices
        self.stacks = stacks

    # def create_coupling(self, r, l):
        # circle1 = Circle3D(r, self.slices)
        # circle2 = Circle3D(r, self.slices, pos=(l*2,l,l), normal=(-0.5,-0.5,-0.5))
        # circle2 = circle1.adapt(circle2)
        # return circle1.connect(circle2)
        
            # ORG!!!!!!!!!!!!!!!!!
    def create_coupling(self, r, l):
        circle1 = Circle3D(r, self.slices)
        circle2 = Circle3D(r, self.slices, pos=(0,0,l))
        # circle1 = Circle3D(r, self.slices, normal=unit_vector((1,1,1)))
        # circle2 = Circle3D(r, self.slices, normal=unit_vector((1,1,1)), pos=(3,3,3))
        # # TEST!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # rot = rotation_matrix(math.pi/2, (0,-1,0))
        # new_vertices = {}
        # for k,v in circle1.vertices.iteritems():
            # new_v = np.dot(v+(1,),rot)
            # new_vertices[k] = new_v[:-1]
        # circle1.vertices = new_vertices
        # rot = rotation_matrix(math.pi/2, (0,-1,0))
        # new_vertices = {}
        # for k,v in circle2.vertices.iteritems():
            # new_v = np.dot(v+(1,),rot)
            # new_vertices[k] = new_v[:-1]
        # circle2.vertices = new_vertices
        # # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return circle1.connect(circle2)
        
    # def create_coupling(self, r, l):
        # d = float(l) / (self.stacks)
        # res = Circle3D(r, self.slices)
        # for i in xrange(self.stacks):
            # res = res.connect(Circle3D(r, self.slices, pos=(0,0,d*(i+1))))
        # return res

    def create_short_elbow(self, r, angle=90):
        return self.create_long_elbow(0, r, angle)

    def create_long_elbow(self, r1, r2, angle=90):
        cos_t = cos_table(self.stacks, np.radians(angle))
        sin_t = sin_table(self.stacks, np.radians(angle))
        v1 = (1,0,0)
        res = None
        for i in xrange(len(sin_t)):
            c_sin = sin_t[i]
            c_cos = cos_t[i]
            cur_pos = (0, c_cos * r2 + c_cos * r1, c_sin * r2 + c_sin * r1)
            v2 = unit_vector(cur_pos) 
            cur_n = unit_vector(vector_product(v1,v2))
            circle = Circle3D(r2, self.slices, pos=cur_pos, normal=cur_n)
            if res is not None:
                res = res.connect(circle)
            else:
                res = circle
        return res

    def create_flow_adapter(self, r1, r2, l):
        circle1 = Circle3D(r1, self.slices)
        circle2 = Circle3D(r2, self.slices, pos=(0,0,l))
        return circle1.connect(circle2)

    def create_tee(self, r):
        pass
    
    def create_spheric_coupling(self, r, R):
        l = math.sqrt(R*R - r*r)
        top = Circle3D(r, self.slices, pos=(0,0,l))
        bottom = Circle3D(r, self.slices, pos=(0,0,-l))
        p1 = top.vertex(0)
        sphere_r = vector_norm(p1)
        cos_t = cos_table(self.stacks, angle=math.pi)
        sin_t = sin_table(self.stacks, angle=math.pi)
        res = bottom
        for i in xrange(self.stacks):
            c_sin = sin_t[i]
            c_cos = cos_t[i]
            cur_r = abs(sphere_r * c_sin)
            cur_pos = (0,0,-c_cos*sphere_r)
            # print cur_pos
            if cur_r > r:
                circle = Circle3D(cur_r, self.slices, pos=cur_pos)
                res = res.connect(circle)
        return res.connect(top)
    
    # def create_spheric_coupling(self, r, R):
        # l = math.sqrt(R*R - r*r)
        # top = Circle3D(r, self.slices, pos=(0,0,l))
        # bottom = Circle3D(r, self.slices, pos=(0,0,-l))
        # p1 = top.vertex(0)
        # sphere_r = vector_norm(p1)
        # cos_t = cos_table(self.stacks, angle=math.pi)
        # sin_t = sin_table(self.stacks, angle=math.pi)
        # res = top
        # for i in xrange(self.stacks):
            # c_sin = sin_t[i]
            # c_cos = cos_t[i]
            # cur_r = abs(sphere_r * c_sin)
            # cur_pos = (0,0,c_cos*sphere_r)
            # if cur_r > r:
                # circle = Circle3D(cur_r, self.slices, pos=cur_pos)
                # res = res.connect(circle)
        # return res.connect(bottom)

    def create_cap(self, r, l):
        circle = Circle3D(r, self.slices)
        point = (0,0,l)
        return circle.connect(point)
        
    # def create_auto_angle(self, r, points):
        # p0 = points[0]
        # p1 = points[1]
        # p2 = points[2]
        # v01 = unit_vector((p1[0]-p0[0],p1[1]-p0[1],p1[2]-p0[2]))
        # v12 = unit_vector((p2[0]-p1[0],p2[1]-p1[1],p2[2]-p1[2]))
        # angle = angle_between_vectors(v01,v12)
        # angle = (math.pi-angle)
        # print angle
        # angle = 0.785398
        # # d = ( 2 * (angle+1.5707963) * r ) / math.pi
        # # d = ( math.pi * r ) / ( 2 * (angle+1.5707963) ) 
        # # d = ( math.pi * r ) / ( 2 * ((math.pi)-angle) ) 
        # # (pi, pi/2) --> (0, 1)
        # slope = (1.0 - 0.0) / ((math.pi/2) - math.pi)
        # d = 0 + slope * (angle - math.pi)
        # f = d
        # print '*'*10
        # print f
        # v10 = unit_vector((p0[0]-p1[0],p0[1]-p1[1],p0[2]-p1[2]))
        # p01 = (p1[0]-(v01[0]*f*r),p1[1]-(v01[1]*f*r),p1[2]-(v01[2]*f*r))
        # p12 = (p1[0]+(v12[0]*f*r),p1[1]+(v12[1]*f*r),p1[2]+(v12[2]*f*r))
        # c3_n = (p2[0]-p12[0],p2[1]-p12[1],p2[2]-p12[2])
        # # n_cent = (p12[0]-p01[0],p12[1]-p01[1],p12[2]-p01[2])
        # # c_cent = Circle3D(r, self.slices, pos=p1, normal=n_cent)
        # c1 = Circle3D(r, self.slices, pos=p0, normal=(0,1,0))
        # c2 = Circle3D(r, self.slices, pos=p01, normal=(0,1,0))
        # c3 = Circle3D(r, self.slices, pos=p12, normal=c3_n)
        # c4 = Circle3D(r, self.slices, pos=p2, normal=c3_n)
        # res = c1.connect(c2).connect(c3).connect(c4)
        # print p01,p12
        # return res
        
        
    # def create_coupling_path(self, r, points):
        # p0 = points[0]
        # p1 = points[1]
        # p2 = points[2]
        # v01 = unit_vector((p1[0]-p0[0],p1[1]-p0[1],p1[2]-p0[2]))
        # v10 = unit_vector((p0[0]-p1[0],p0[1]-p1[1],p0[2]-p1[2]))
        # v12 = unit_vector((p2[0]-p1[0],p2[1]-p1[1],p2[2]-p1[2]))
        # angle = angle_between_vectors(v01,v12)
        # angle = (math.pi-angle)
        # # distance between equidistant point from (p01 and p12)
        # d = r / math.sin(angle/2)
        # # distance of the points along p01 and p12
        # l = d * math.cos(angle/2)
        # p01 = (p1[0]-(v01[0]*l),p1[1]-(v01[1]*l),p1[2]-(v01[2]*l))
        # p12 = (p1[0]+(v12[0]*l),p1[1]+(v12[1]*l),p1[2]+(v12[2]*l))
        # c3_n = (p2[0]-p12[0],p2[1]-p12[1],p2[2]-p12[2])
        # # aux circle to compute crossection point to make an arc
        # aux_slices = 100
        # aux_c = Circle3D(r, 100, pos=p01, normal=v01)
        # p = None
        # eps = 0.0001
        # for point in aux_c.vertices.itervalues():
            # cur_v = (point[0]-p12[0], point[1]-p12[1], point[2]-p12[2])
            # distance = abs(vector_norm(cur_v))
            # if abs(r-distance) < eps:
                # p = point
                # break
        # print p
        # # now we calculate points along the curve between p01 and p12
        # aux_n = vector_product(v10, v12)
        # vp01 = unit_vector((p01[0]-p[0],p01[1]-p[1],p01[2]-p[2]))
        # vp12 = unit_vector((p12[0]-p[0],p12[1]-p[1],p12[2]-p[2]))
        # aux_angle = angle_between_vectors(vp01, vp12)
        # angle_points = aux_angle / float(self.stacks)
        # angles_list = [angle_points*(i+1) for i in xrange(self.stacks-1)]
        # p_list = []
        # vp01 = unit_vector((p01[0]-p[0],p01[1]-p[1],p01[2]-p[2]))
        # vp12 = unit_vector((p12[0]-p[0],p12[1]-p[1],p12[2]-p[2]))
        # for c_p in angles_list:
            # add_p = (r*math.cos(c_p)*vp01[0] + r*math.sin(c_p)*vp12[0],
                     # r*math.cos(c_p)*vp01[1] + r*math.sin(c_p)*vp12[1],
                     # r*math.cos(c_p)*vp01[2] + r*math.sin(c_p)*vp12[2])
            # add_p = (add_p[0] + p[0],
                     # add_p[1] + p[1],
                     # add_p[2] + p[2])
            # p_list.append(add_p)
        
        
        # c1 = Circle3D(r, self.slices, pos=p0, normal=v01)
        # c2 = Circle3D(r, self.slices, pos=p01, normal=v01)
        # c3 = Circle3D(r, self.slices, pos=p12, normal=v12)
        # c4 = Circle3D(r, self.slices, pos=p2, normal=v12)
        # res = c1.connect(c2)
        # f_list = p_list[1:]
        # f_list.append(p12)
        # cnt = 0
        # for point in p_list:
            # f_p = f_list[cnt]
            # # cur_n = unit_vector((point[0]-f_p[0],point[1]-f_p[1],point[2]-f_p[2]))
            # cur_n = unit_vector((-point[0]+f_p[0],-point[1]+f_p[1],-point[2]+f_p[2]))
            # circle = Circle3D(r, self.slices, pos=point, normal=cur_n)
            # res = res.connect(circle)
            # cnt += 1
        # res = res.connect(c3).connect(c4)
        
        # return res
        
    def create_coupling_path(self, r, points):
        # p0 = points[0]
        # p1 = points[1]
        # p2 = points[2]
        # v01 = unit_vector((p1[0]-p0[0],p1[1]-p0[1],p1[2]-p0[2]))
        # v10 = unit_vector((p0[0]-p1[0],p0[1]-p1[1],p0[2]-p1[2]))
        # v12 = unit_vector((p2[0]-p1[0],p2[1]-p1[1],p2[2]-p1[2]))
        # angle = angle_between_vectors(v01,v12)
        # angle = (math.pi-angle)
        # # distance between equidistant point from (p01 and p12)
        # d = r / math.sin(angle/2)
        # # distance of the points along p01 and p12
        # l = d * math.cos(angle/2)
        # p01 = (p1[0]-(v01[0]*l),p1[1]-(v01[1]*l),p1[2]-(v01[2]*l))
        # p12 = (p1[0]+(v12[0]*l),p1[1]+(v12[1]*l),p1[2]+(v12[2]*l))
        # c1 = Circle3D(r, self.slices, pos=p0, normal=v01)
        # c2 = Circle3D(r, self.slices, pos=p01, normal=v01)
        # c3 = Circle3D(r, self.slices, pos=p12, normal=v12)
        # c4 = Circle3D(r, self.slices, pos=p2, normal=v12)
        # res = c1.connect(c2).connect(c3).connect(c4)
        circles_file = open('circles.txt','w')
        params = self._calculate_points(r,points)
        print '*-'*30
        print params['points']
        print '*_'*30
        print params['normals']
        print '*o'*30
        first_p = params['points'][0]
        first_n = params['normals'][0] 
        proc_p = params['points'][1:]
        proc_n = params['normals'][1:]
        res = Circle3D(r, self.slices, pos=first_p, normal=first_n)
        prev_circle = Circle3D(r, self.slices, pos=first_p, normal=first_n)
        for i in xrange(len(proc_p)):
            print 'inb4'
            print i,proc_p[i],proc_n[i]
            circles_file.write('prev_circle c, n {0}, {1}\n'.format(prev_circle.center, prev_circle.normal_v))
            circles_file.write('{0}\n'.format(prev_circle.vertices))
            new_circle = Circle3D(r,self.slices,pos=proc_p[i],normal=proc_n[i])
            circles_file.write('new_circle c, n {0}, {1}\n'.format(new_circle.center, new_circle.normal_v))
            circles_file.write('{0}\n'.format(new_circle.vertices))
            new_circle = prev_circle.adapt(new_circle)
            # prev_circle = copy.deepcopy(new_circle)
            prev_circle = new_circle
            # circles_file.write('new_circle c, n {0}, {1}\n'.format(new_circle.center, new_circle.normal_v))
            # circles_file.write('{0}\n'.format(new_circle.vertices))
            res = res.connect(new_circle)
            print 'inbafter'
        circles_file.close()
        return res
        
    # def _compute_midpoint(self, d, b, e):
        # """Shared point between the two 3D circles."""
        # dx = d[0]
        # dy = d[1]
        # dz = d[2]
        # bx = b[0]
        # by = b[1]
        # bz = b[2]
        # ex = e[0]
        # ey = e[1]
        # ez = e[2]
        # a1 = (ey-by)*dx + (by-dy)*ex + (dy-ey)*bx
        # b1 = (ez-bz)*dx + (bz-dz)*ex + (dz-ez)*bx
        # c1 = ((ex*ex+ey*ey+ez*ez-bx*bx-by*by-bz*bz)*dx 
            # +(bx*bx+by*by+bz*bz-dx*dx-dy*dy-dz*dz)*ex 
            # +(dx*dx+dy*dy+dz*dz-ex*ex-ey*ey-ez*ez)*bx)
        # d1 = (ey-by)*dx + (by-dy)*ex + (dy-ey)*bx
        # e1 = (ez-bz)*dx + (bz-dz)*ex + (dz-ez)*bx
        # f1 = ((ex*ex+ey*ey+ez*ez-bx*bx-by*by-bz*bz)*dx 
            # +(bx*bx+by*by+bz*bz-dx*dx-dy*dy-dz*dz)*ex 
            # +(dx*dx+dy*dy+dz*dz-ex*ex-ey*ey-ez*ez)*bx)
        # pzn1 = c1 * a1
        # pzn2 = f1 * d1
        # pzd1 = e1 * a1
        # pzd2 = d1 * b1
        # pzn = pzn1 - pzn2
        # pzd = pzd1 - pzd2
        # print 'a1',a1
        # print 'b1',b1
        # print 'c1',c1
        # print 'd1',d1
        # print 'e1',e1
        # print 'f1',f1
        # print 'pzn,pzd', pzn,pzd
        # pz = pzn / pzd
        
        # py = 0.0
        # px = 0.0
        # return (px,py,pz)
        
        
    def _interporlate(self, r, p0, p1, p2):
        """This will separate p1 in two different points"""
        v01 = unit_vector((p1[0]-p0[0],p1[1]-p0[1],p1[2]-p0[2]))
        v10 = unit_vector((p0[0]-p1[0],p0[1]-p1[1],p0[2]-p1[2]))
        v12 = unit_vector((p2[0]-p1[0],p2[1]-p1[1],p2[2]-p1[2]))

        # ORG "WORKING" -----------------------------------------------------------
        # # aux circle to compute shared point to make an arc of points
        # aux_slices = 500
        # aux_c = Circle3D(curve_factor*r, aux_slices, pos=p01, normal=v01)
        # midpoint = None
        # eps = 0.0000001
        # for point in aux_c.vertices.itervalues():
            # cur_v = (point[0]-p12[0], point[1]-p12[1], point[2]-p12[2])
            # distance = abs(vector_norm(cur_v))
            # if abs(curve_factor*r-distance) < eps:
                # midpoint = point
                # break
        # print 'midpoint', midpoint
        # --------------------------------------------------------------------------
        # print 'p01 before', p01
        # print 'p12 before', p12
        # bisect_normal = unit_vector((midpoint[0]-p1[0],midpoint[1]-p1[1],midpoint[2]-p1[2]))
        bisect_normal = unit_vector(((v10[0]+v12[0])/2,(v10[1]+v12[1])/2,(v10[2]+v12[2])/2))
        bisect_line = Line3D(p1,bisect_normal)
        print 'bisect_normal',bisect_normal
        print 'p1',p1
        p01mid = ((p0[0]+p1[0])/2.0,(p0[1]+p1[1])/2.0,(p0[2]+p1[2])/2.0)
        p12mid = ((p2[0]+p1[0])/2.0,(p2[1]+p1[1])/2.0,(p2[2]+p1[2])/2.0)
        print 'p01mid',p01mid
        print 'p12mid',p12mid
        print 'v01',v01
        print 'v12',v12
        plane1 = Plane(p01mid, v01)
        plane2 = Plane(p12mid, v12)
        
        inter1 = plane1.intersection(bisect_line)
        inter2 = plane2.intersection(bisect_line)
        print 'inter1',inter1
        print 'inter2',inter2
        d1 = abs(vector_norm((p1[0]-inter1[0],p1[1]-inter1[1],p1[2]-inter1[2])))
        d2 = abs(vector_norm((p1[0]-inter2[0],p1[1]-inter2[1],p1[2]-inter2[2])))
        print 'd1',d1
        print 'd2',d2
        if d1 < d2:
            mid_max = inter1
        else:
            mid_max = inter2

        # this is the minimal distance point that assures a 90º elbow, so the
        angle = angle_between_vectors(v01,v12)
        angle = (math.pi-angle)
        print 'angle', angle
        # distance between equidistant point from (p01 and p12)
        d = r / math.sin(angle/2)
        # distance of the points along p01 and p12
        l = d * math.cos(angle/2)
        print 'd, l', d, l
        p01min = (p1[0]-(v01[0]*l),p1[1]-(v01[1]*l),p1[2]-(v01[2]*l))
        p12min = (p1[0]+(v12[0]*l),p1[1]+(v12[1]*l),p1[2]+(v12[2]*l))
        plane1 = Plane(p01min,v01)
        mid_min = plane1.intersection(bisect_line)
        
        # to avoid problems, me calculate as a midpoint another point along
        # the line bisector line
        b_vector = (mid_min[0]-mid_max[0],mid_min[1]-mid_max[1],mid_min[2]-mid_max[2])
        # factor between 0 and 1: closer to 0 means more curve
        factor = 0.2
        midpoint = (mid_max[0]+b_vector[0]*factor,
                    mid_max[1]+b_vector[1]*factor,
                    mid_max[2]+b_vector[2]*factor)
        
        
        # recalculate starting and ending points of the arc:
        line1 = Line3D(p0,v01)
        line2 = Line3D(p1,v12)
        plane1 = Plane(midpoint,v01)
        plane2 = Plane(midpoint,v12)
        p01 = plane1.intersection(line1)
        p12 = plane2.intersection(line2)
        print 'p01 after', p01
        print 'p12 after', p12
        print 'midpoint after', midpoint
        
        # print 'THE TEST!','lo'*30
        # planet = Plane((0,0,0),(1,1,1))
        # linet = Line3D((0,0,0),(0,1,0))
        # print planet.intersection(linet)
        # print 'lo'*34
        
        # # TEMP TEST: --------------------------------------------------------------------
        # d0 = abs(vector_norm((p0[0]-midpoint[0],p0[1]-midpoint[1],p0[2]-midpoint[2])))
        # d1 = abs(vector_norm((p2[0]-midpoint[0],p2[1]-midpoint[1],p2[2]-midpoint[2])))
        
        
        # if d0 > d1:
            # d = d1
        # else:
            # d = d0
        # new_r = math.sin(angle/2)*d
        # # distance of the points along p01 and p12
        # l = d * math.cos(angle/2)
        # print 'd, l', d, l
        # p01 = (p1[0]-(v01[0]*l),p1[1]-(v01[1]*l),p1[2]-(v01[2]*l))
        # p12 = (p1[0]+(v12[0]*l),p1[1]+(v12[1]*l),p1[2]+(v12[2]*l))
        # # aux circle to compute shared point to make an arc of points
        # aux_slices = 5000
        # aux_c = Circle3D(new_r, aux_slices, pos=p01, normal=v01)
        # midpoint = None
        # eps = 0.00001
        # for point in aux_c.vertices.itervalues():
            # cur_v = (point[0]-p12[0], point[1]-p12[1], point[2]-p12[2])
            # distance = abs(vector_norm(cur_v))
            # if abs(new_r-distance) < eps:
                # midpoint = point
                # break
        # print 'midpoint', midpoint
        # # -------------------------------------------------------------------------------
        
        
        return Arc3D(self.stacks, p01, p12, midpoint)
        
        # return [p01, p12]
        
    def _calculate_points(self, r, points):
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
            print "THE COLOSSEUM!",i,b_p,c_p,f_p
            cur_bv = unit_vector((c_p[0]-b_p[0],
                                  c_p[1]-b_p[1],
                                  c_p[2]-b_p[2]))
            cur_fv = unit_vector((f_p[0]-c_p[0],
                                  f_p[1]-c_p[1],
                                  f_p[2]-c_p[2]))
            angle = angle_between_vectors(cur_bv,cur_fv)
            if angle != 0 and angle != math.pi and math.isnan(angle) is False:
                inter_points = self._interporlate(r,b_p,c_p,f_p)
                for i in xrange(inter_points.n_vertices()):
                    res['points'].append(inter_points.vertex(i))
                # for p in inter_points:
                    # res['points'].append(p)
                res['normals'].append(cur_bv)
                # OPTIMIZE THIS!!
                # last_p = inter_points[0]
                # last_p = inter_points.vertex(0)
                print 'process of points beg'
                for i in xrange(inter_points.n_vertices()-2):
                    # p = inter_points.vertex(i+1)
                    
                    # next_p = inter_points.vertex(i+2)
                    last_p = inter_points.vertex(i)
                    print 'last_p', last_p
                    p = inter_points.vertex(i+1)
                    print 'p', p
                    next_p = inter_points.vertex(i+2)
                    print 'next_p', next_p
                    # cur_n = unit_vector((p[0]-next_p[0],p[1]-next_p[1],p[2]-next_p[2]))
                    cur_n = unit_vector((next_p[0]-last_p[0],next_p[1]-last_p[1],next_p[2]-last_p[2]))
                    print 'cur_n', cur_n
                    res['normals'].append(cur_n)
                print 'process of points end'
                # for p in inter_points[1:-1]:
                    # cur_n = unit_vector((p[0]-last_p[0],p[1]-last_p[1],p[2]-last_p[2]))
                    # res['normals'].append(cur_n)
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
        
