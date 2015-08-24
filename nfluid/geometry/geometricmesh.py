import copy
import math

from visvis import OrientableMesh, Point, Pointset
from nfluid.external.transformations import rotation_matrix
from nfluid.external.transformations import translation_matrix
from nfluid.external.transformations import angle_between_vectors
# from nfluid.geometry.functions import angle_between_vectors
from nfluid.external.transformations import vector_product
from nfluid.external.transformations import unit_vector
from nfluid.external.transformations import vector_norm
from nfluid.geometry.functions import cos_table, sin_table, equal_vertices
from nfluid.geometry.functions import normal_of, center_of
from nfluid.geometry.auxiliar_geometry import Plane
import numpy as np
import visvis as vv


class GeometricMesh(object):
    """Simple class to specify a geometrical mesh:
       collection of vertices, its normals and triangles.
       Note: elements are always in order.
    """
    def __init__(self):
       self.vertex_count = 0
       self.normals_count = 0
       self.triangles_count = 0
       self.vertices = {}
       self.normals = {}
       self.triangles = {}

    def vertex(self, i):
        return self.vertices[i]

    def add_vertex(self, vertex, id=None):
        if id:
            index = id
        else:
            index = self.vertex_count
        self.vertices[index] = tuple(vertex)
        self.vertex_count += 1
        return index
        
    def update_vertex(self, index, vertex):
        self.vertices[index] = tuple(vertex)
        
    def remove_vertex(self, index):
        del self.vertices[index]
 
    def normal(self, i):
        return self.normals[i]

    def add_normal(self, index, normal):
        index = self.normals_count
        self.normals[index] = tuple(normal)
        self.normals_count += 1
        return index
    
    def update_normal(self, index, normal):
        self.normals[index] = tuple(normal)
        
    def remove_normal(self, index):
        del self.normals[index]
        
    def triangle(self, i):
        return self.triangles[i]

    def add_triangle(self, triangle):
        index = self.triangles_count
        self.triangles[index] = triangle
        self.triangles_count += 1
        return index
        
    def update_triangle(self, index, triangle):
        self.triangles[index] = triangle
       
    def remove_triangle(self, index):
        del self.triangles[index]
        
    def to_visvis_mesh(self):
        vertices = self.vertices.values()
        if len(self.normals) is not 0:
            normals = self.normals.values()
        else:
            normals = None
        if len(self.triangles) is not 0:
            faces = self.triangles.values()
        else:
            faces = None
        res = OrientableMesh(parent=vv.gca(), vertices=vertices, normals=normals,
                             faces=faces, verticesPerFace=3)
        return res

    def export(self, filename):
        vv.meshWrite(filename, self.to_visvis_mesh(), bin=False)
        
    def n_vertices(self):
        return len(self.vertices)
        
    def n_normals(self):
        return len(self.normals)
        
    def n_triangles(self):
        return len(self.triangles)

    def move(self, point, direction):
        pass

    def _move(self, point, direction, p, n):
        """center == True means that we do the movement in reference
        to the center of the mesh
        center == False means that we do the movement in reference to the
        center of the head circle.
        This method implies a traslation and a rotation.
        """
        angle = angle_between_vectors(direction, n)
        if angle == math.pi:
            aux_plane = Plane(p,n)
            aux_point = aux_plane.get_point()
            vect = unit_vector((aux_point[0]-p[0],
                               aux_point[1]-p[1],
                               aux_point[2]-p[2]))
        else:
            vect = unit_vector(vector_product(direction, n))

        rot_m = rotation_matrix(angle, vect)
        d = (point[0]-p[0],point[1]-p[1],point[2]-p[2])
        t = (-p[0],-p[1],-p[2])
        for k,v in self.vertices.iteritems():
            n_v = (v[0]+t[0],v[1]+t[1],v[2]+t[2])
            if angle != 0.0 and angle != 2*math.pi and math.isnan(angle) is False:
                n_v = np.dot(n_v+(1,), rot_m)
            n_v = (n_v[0]+d[0]-t[0],n_v[1]+d[1]-t[1],n_v[2]+d[2]-t[2])
            self.update_vertex(k, n_v)
            # print n_v

    def _set_orientation(self, angle, dir, center):
        v_rot = dir
        t = (-center[0],-center[1],-center[2])
        if angle != 0.0 and math.isnan(angle) is False:
            rot_m = rotation_matrix(angle, v_rot)
            for k,v in self.vertices.iteritems():
                n_v = (v[0]+t[0],v[1]+t[1],v[2]+t[2])
                n_v = np.dot(n_v+(1,), rot_m)
                n_v = (n_v[0]-t[0],n_v[1]-t[1],n_v[2]-t[2])
                self.update_vertex(k,n_v)

    def attach(self, figure):
        """Means to move the head face of 'figure' to
        the tail head of self, first step to link the two
        meshes into one."""
        pass
        
    def adapt(self, figure):
        """This method is necessary to make coincident all the vertices
        of the two faces of the figures we are linking. This means that
        to adapt we must have attached self and 'figure'."""
        pass
        
    def connect(self, figure):
        """This connect means that:
            - 3D polygon with 3D polygon: new triangles will be created,
              that will generate a 3D solid return by this method.
            - 3D solid with 3D polygon: mew triangles will be created,
              that will generate a 3D solid return by this method.
            - 3D solid with 3D solid: if two faces are coincidents (this
              means they have all their vertices in common - same position)
              they will be merged, creating a new 3D solid returned by this
              method.
              
            Note: this method does not alter the geometry of any of the
            meshes, it will always generate a new indepent one.
        """
        pass

    def twist(self, angle):
        """Intermediate method used to adap; giving and angle, it will rotate
        all the circles of self around its correspondant normals.
        """

    @property
    def resolution(self):
        return self.vertex_count
        
class Arc3D(GeometricMesh):
    """Internal class for generator, mainly used to help constructing the
    coupling path piece (since and arc can't be connected to a circle or
    cylindric part).
    Points formula:
        P = midpoint + (sin(alpha-beta)*u + sin(beta)*v) / (sin(angle))
        where u and v are the two vectors defined by the midpoint
        and the two other points,
        alpha is the angle between u and v and
        beta is an angle between 0 and alpha.
    
    Note: this arc will not work if the three points are colinear
         (which is not a problem ATM).
    """
    def __init__(self, slices, p1, p2, midpoint):
        super(Arc3D, self).__init__()
        u = (p1[0]-midpoint[0],
                         p1[1]-midpoint[1],
                         p1[2]-midpoint[2])
        v = (p2[0]-midpoint[0],
                         p2[1]-midpoint[1],
                         p2[2]-midpoint[2])
        alpha = angle_between_vectors(u,v)
        step = alpha / slices
        for i in xrange(slices+1):
            beta = i*step
            x = (midpoint[0] +
                    (
                     (math.sin(alpha-beta)*u[0] + math.sin(beta)*v[0]) / 
                     (math.sin(alpha))
                    )
                )
            y = (midpoint[1] + 
                   (
                     (math.sin(alpha-beta)*u[1] + math.sin(beta)*v[1]) / 
                     (math.sin(alpha))
                   )
                )
            z = (midpoint[2] + 
                   (
                     (math.sin(alpha-beta)*u[2] + math.sin(beta)*v[2]) / 
                     (math.sin(alpha))
                   )
                )
            p = (x,y,z)
            self.add_vertex(p)
        # IMPORTANT: AS A GEOMETRICMESH, IT SHOULD CALCULATE NORMALS
        # TOO; NOT IMPLEMENTED ATM
        
    def connect(self, figure):
        pass
        
class Circle3D(GeometricMesh):
    """Internal primary private class for the generator. It makes easier to
    construct complex 3D figures.
    
    P = R * cos(A) * U + R * sin(A) * V
           
    where:  R ==> Radius
            A ==> current angle of the circle in the loop
            U ==> Perpendicular vector to the normal of the circle
            V ==> Another perpendicular vector
    """
    def __init__(self, radius, slices, pos=(0.0,0.0,0.0),
                 normal=(0.0,0.0,1.0),
                 filled=False):
        super(Circle3D, self).__init__()
        self.radius = radius
        self.slices = slices
        self.center = pos
        self.normal_v = tuple(unit_vector(normal))
        # WE DONT SUPPORT IT FTM
        self.filled = False
        # Generate the cosine and sinus tables to obtain the points
        cos_t = cos_table(slices)
        sin_t = sin_table(slices)

        # Vectors inside the circle, same orientation for all the points
        v1 = unit_vector((1,0,0))
        v2 = unit_vector((0,1,0))
        points = ()
        # Generate the points: 
        for i in xrange(slices):
            p = (radius*cos_t[i]*v1[0] + radius*sin_t[i]*v2[0],
                 radius*cos_t[i]*v1[1] + radius*sin_t[i]*v2[1],
                 radius*cos_t[i]*v1[2] + radius*sin_t[i]*v2[2]
                )
            points = points + (p,)
        # Rotate the points if needed (i.e. the normal is not (0,0,1)
        rot_points = ()
        angle_z = angle_between_vectors((0,0,1), self.normal_v)
        if angle_z != 0:
            if angle_z != math.pi:
                rot_vect = unit_vector(np.cross(self.normal_v, (0,0,1)))
            else:
                rot_vect = (1,0,0)
            rot_matrix = rotation_matrix(angle_z, rot_vect)
            for p in points:
                new_p = p
                new_p = new_p + (1,)
                new_p = np.dot(new_p, rot_matrix)
                rot_points = rot_points + (new_p[:-1],)
        else:
            rot_points = points
        # Translate the points to the center of the circle and added them
        for p in rot_points:
            index = self.add_vertex(tuple(map(lambda x, y: x + y, p, self.center)))
            self.add_normal(index, p)
        # If the circle is filled we need to create an additional point and triangles
        if self.filled:
            self.center = self.add_vertex(self.center)
            self.add_normal(self.center, self.normal_v)
            for i in xrange(slices+1):
                self.add_triangle((i, self.center, (i + 1) % slices))

    def _connect_to_point(self, point):
        # FIX THIS! COPY METHODS!
        
        res = copy.deepcopy(self)
        cap = res.add_vertex(point)
        res.add_normal(cap, point)
        print res.slices
        print res.vertices
        
        for i in xrange(res.slices):
            res.add_triangle((i, cap, (i + 1) % res.slices))
        print res.triangles
        return res

    def _flip(self):
        """This changes the orientation of the vertices without modifying the circle.
        The 1st vertex is the pivot."""
        n_vertices = self.vertex_count
        for i in xrange(1, n_vertices / 2):
            i0 = i
            i1 = n_vertices-i
            p0 = self.vertex(i0)
            p1 = self.vertex(i1)
            self.update_vertex(i0,p1)
            self.update_vertex(i1,p0)

    def set_orientation(self, angle):
        angle = np.radians(angle)
        self._set_orientation(angle, self.normal_v, self.center)
        # update normal and center
        self.normal_v = normal_of(self.vertex(0),self.vertex(1),self.vertex(2))
        self.center = center_of([p for p in self.vertices.itervalues()])

    def move(self, point, direction, center=False):
        if center:
            raise NotImplementedError()
        else:
            self._move(point,direction,self.center,self.normal_v)
            self.normal_v = normal_of(self.vertex(0),self.vertex(1),self.vertex(2))
            self.center = center_of([p for p in self.vertices.itervalues()])
        
    def adapt(self, figure):
        if isinstance(figure, Circle3D):
            print 'HEY! BEEN TRYING TO MEET YOU!!!!!!', '+++'*30
            org_center, org_normal = figure.center, figure.normal_v
            # figure.move(self.center, figure.normal_v)
            figure.move(self.center, self.normal_v)
            print "after move!"
            p0 = self.vertex(0)
            v0 = unit_vector((p0[0]-self.center[0],p0[1]-self.center[1],p0[2]-self.center[2]))
            p1 = figure.vertex(0)
            v1 = unit_vector((p1[0]-figure.center[0],p1[1]-figure.center[1],p1[2]-figure.center[2]))
            angle = angle_between_vectors(v0,v1)
            print 'p0, p1'
            print p0, p1
            print 'v0, v1'
            print v0, v1
            print 'angle'
            print angle
            print
            # print '.'*30
            print
            # if not equal_vertices(v0, v1):
                # print "FLIP                               FLIP" 
                # figure._flip()
            # else:
                # print "NOT A FLIP                               FLIP" 
            #twist the figure (can we use set_orientation? In the case of Circle3D twist == set_orientation)
            figure.set_orientation(np.degrees(angle))
            #check if we need to keep twisting (since the angle between the two vectors
            #was greater than 180
            p0 = self.vertex(0)
            p1 = figure.vertex(0)
            center1 = self.center
            center2 = figure.center
            v0c = unit_vector((-center1[0]+p0[0],-center1[1]+p0[1],-center1[2]+p0[2]))
            v1c = unit_vector((-center2[0]+p1[0],-center2[1]+p1[1],-center2[2]+p1[2]))
            #twist a second time (twitst method wont do anything if the angle is 0)
            angle2 = angle_between_vectors(tuple(v1c),tuple(v0c))
            print 'p0, p1 2'
            print p0, p1
            print 'v0, v1'
            print v0c, v1c
            print 'angle2'
            print angle2
            figure.set_orientation(np.degrees(angle2))
            p0 = self.vertex(0)
            p1 = figure.vertex(0)
            print 'p0, p1 3'
            print p0, p1
            # print 'just debugging'
            # p2 = self.vertex(3)
            # p3 = figure.vertex(3)
            # print 'p2 p3'
            # print p2, p3
            # if not equal_vertices(p2, p3):
                # figure._flip()
                # print "FLIP FLIP FLIP"
                # p2 = self.vertex(3)
                # p3 = figure.vertex(3)
                # print 'p2 p3 2'
                # print p2, p3
            figure.move(org_center, org_normal)
            print 'GIGANTIC! A BIG BIG LOVE!!!!!'
        return figure

    # ORIGINAL NOT WORKING XD --------------------------------------------------------------------------------------
    # def adapt(self, figure):
        # if isinstance(figure, Circle3D):
            # # make the circles co-planars
            # p1 = figure.vertex(0)
            # v1 = unit_vector((p1[0]-figure.center[0],p1[1]-figure.center[1],p1[2]-figure.center[2]))
            # # angle_pl = angle_between_vectors(self.normal_v, v1)
            # angle_pl = angle_between_vectors(self.normal_v,figure.normal_v)
            # rot_points = {}
            # print 'adapt vectors: {0}  {1}'.format(self.normal_v, figure.normal_v)
            # print 'angle_pl', angle_pl
            # rot_vect_pl = vector_product(self.normal_v, figure.normal_v)
            # # rot_vect_pl = vector_product(self.normal_v, v1)
            # # rot_vect_pl = v1
            # if angle_pl != 0 and math.isnan(angle_pl) is False:
                # print 'figure.normal_v', figure.normal_v
                # # rot_matrix = rotation_matrix(angle_pl, rot_vect)
                # rot_matrix = rotation_matrix(angle_pl, (rot_vect_pl[0], rot_vect_pl[1], rot_vect_pl[2]))
                # for k, p in figure.vertices.iteritems():
                    # print 'this p! ...k, p : ', k, p
                    # new_p = (p[0]-figure.center[0],p[1]-figure.center[1],p[2]-figure.center[2])
                    # new_p = new_p + (1,)
                    # new_p = np.dot(new_p, rot_matrix)
                    # new_p = tuple(new_p[:-1])
                    # new_p = (new_p[0]+figure.center[0],new_p[1]+figure.center[1],new_p[2]+figure.center[2])
                    # rot_points[k] = new_p
                    # # Update normals!!!
                # figure.vertices = dict(rot_points)
            
            # # # make both vectors coincident
            # # p0 = self.vertex(0)
            # # print 'this p0 ,,,,,', p0
            # # v0 = unit_vector((p0[0]-self.center[0],p0[1]-self.center[1],p0[2]-self.center[2]))
            # # p1 = figure.vertex(0)
            # # v1 = unit_vector((p1[0]-figure.center[0],p1[1]-figure.center[1],p1[2]-figure.center[2]))
            # # angle = angle_between_vectors(v0,v1)
            # # rot_points = {}
            # # print 'v0,v1 ', v0,v1
            # # print 'angle', angle
            # # if angle != 0:
                # # # rot_matrix = rotation_matrix(angle, rot_vect)
                # # rot_matrix = rotation_matrix(angle, (rot_vect_pl[0], rot_vect_pl[1], rot_vect_pl[2]))
                # # for k, p in figure.vertices.iteritems():
                    # # print 'this p! ...k, p : ', k, p
                    # # new_p = (p[0]-figure.center[0],p[1]-figure.center[1],p[2]-figure.center[2])
                    # # new_p = new_p + (1,)
                    # # new_p = np.dot(new_p, rot_matrix)
                    # # new_p = tuple(new_p[:-1])
                    # # new_p = (new_p[0]+figure.center[0],new_p[1]+figure.center[1],new_p[2]+figure.center[2])
                    # # rot_points[k] = new_p
                    # # # Update normals!!!
                # # figure.vertices = dict(rot_points)

            # # print 'angle', angle_pl
            # # if angle_pl != 0  and math.isnan(angle_pl) is False:
                # # rot_vect = vector_product(self.normal_v, figure.normal_v)
                # # print 'figure.normal_v', figure.normal_v
                # # # rot_matrix = rotation_matrix(angle_pl, rot_vect)
                # # rot_matrix = rotation_matrix(angle_pl, (rot_vect[0], rot_vect[1], rot_vect[2]))
                # # for k, p in figure.vertices.iteritems():
                    # # print 'this p! ...k, p : ', k, p
                    # # new_p = (p[0]-figure.center[0],p[1]-figure.center[1],p[2]-figure.center[2])
                    # # new_p = new_p + (1,)
                    # # new_p = np.dot(new_p, rot_matrix)
                    # # new_p = tuple(new_p[:-1])
                    # # new_p = (new_p[0]+figure.center[0],new_p[1]+figure.center[1],new_p[2]+figure.center[2])
                    # # rot_points[k] = new_p
                    # # # Update normals!!!
                # # figure.vertices = dict(rot_points)
            # return figure
    # ----------------------------------------------------------------------------------------------------------------
       
    def connect(self, figure):
        res = CylindricalPart()
        n_vertices = self.n_vertices()
        if isinstance(figure, Circle3D):
            for i in xrange(n_vertices):
                res.add_vertex(self.vertex(i))
                res.add_normal(i, self.normal(i))
            for i in xrange(n_vertices):
                res.add_vertex(figure.vertex(i))
                res.add_normal(i+self.slices, figure.normal(i))
            for i in xrange(self.slices):
                res.add_triangle((i, i+self.slices, (i+1) % (self.slices)))
                res.add_triangle(((i+1) % self.slices,
                                   (i+self.slices) % (self.slices*2),
                                  ((i+1) % self.slices) + self.slices))
            res.add_connection_face(tuple([x for x in xrange(n_vertices)]))
            res.add_connection_face(tuple([x+n_vertices for x in xrange(n_vertices)]))
            return res
        elif isinstance(figure, CylindricalPart):
            return figure.connect(self)
        else:
            return self._connect_to_point(figure)


class CylindricalPart(GeometricMesh):
    """Class reprersenting a piece made of circles, whatever its form is.
    """
    def __init__(self):
        super(CylindricalPart, self).__init__()
        self.connection_faces = {}
        self.face_count = 0
    
    def add_connection_face(self, face):
        self.connection_faces[self.face_count] = face
        self.face_count = self.face_count + 1
        
    def connection_face(self, i):
        return self.connection_faces[i]

    def n_faces(self):
        return len(self.connection_faces)
        
    def get_face_info(self, face):
        vertices = self.connection_faces[face]
        vert_coords = []
        for v in vertices:
            vert_coords.append(self.vertex(v))
        v0 = vert_coords[0]
        v1 = vert_coords[1]
        v2 = vert_coords[2]
        n = normal_of(v0, v1, v2)
        c = center_of(vert_coords)
        return (c, n)

    def move(self, point, direction, center=False):
        """center == True means that we do the movement in reference
        to the center of the mesh
        center == False means that we do the movement in reference to the
        center of the head circle.
        This method implies a traslation and a rotation.
        """
        if center:
            raise NotImplementedError()
        else:
            p, n = self.get_face_info(0)
            self._move(point,direction,p,n)
    
    def set_orientation(self, angle):
        # Maybe a better name for it?
        angle = np.radians(angle)
        # We orientate taking into account the base face - head
        center, normal = self.get_face_info(0)
        self._set_orientation(angle, normal, center)

    def link(self, figure):
        res = self.attach(figure)
        res = self.adapt(res)
        res = self.connect(res)
        return res
        # return self.connect(res)

    def attach(self, figure):
        # Last face (considered tail ftm)
        center1, normal1 = self.get_face_info(self.n_faces()-1)
        center2, normal2 = figure.get_face_info(0)
        figure.move(center1, normal1)
        center2, normal2 = figure.get_face_info(0)
        return figure

    def twist(self, angle):
        if angle != 0.0 and math.isnan(angle) is False:
            res = self.resolution
            n_circles = self.n_vertices() / res
            for i in xrange(n_circles):
                cur_indexes = [a+i*res for a in xrange(res)]
                cur_vertices = [self.vertex(index) for index in cur_indexes]
                c_normal = normal_of(cur_vertices[0],
                                     cur_vertices[2],
                                     cur_vertices[1])
                rot_m = rotation_matrix(angle, c_normal)
                center = center_of(cur_vertices)
                t = (-center[0],-center[1],-center[2])
                for k,v in map(None, cur_indexes, cur_vertices):
                    n_v = (v[0]+t[0],v[1]+t[1],v[2]+t[2])
                    n_v = np.dot(n_v+(1,), rot_m)
                    n_v = (n_v[0]-t[0],n_v[1]-t[1],n_v[2]-t[2])
                    self.update_vertex(k,n_v)

    def adapt(self, figure):
        # Calculate angle of twist
        center1, normal1 = self.get_face_info(self.n_faces()-1)
        center2, normal2 = figure.get_face_info(0)
        face1 = self.connection_face(self.n_faces()-1)
        face2 = figure.connection_face(0)
        n_vertices1 = self.n_vertices()
        n_vertices2 = figure.n_vertices()
        v0 = self.vertex(face1[0])
        v1 = figure.vertex(face2[0])
        v0c = unit_vector((-center1[0]+v0[0],-center1[1]+v0[1],-center1[2]+v0[2]))
        v1c = unit_vector((-center2[0]+v1[0],-center2[1]+v1[1],-center2[2]+v1[2]))
        angle = angle_between_vectors(v1c,v0c)
        #twist the figure
        figure.twist(angle)
        #check if we need to keep twisting (since the angle between the two vectors
        #was greater than 180
        v1 = figure.vertex(face2[0])
        v0c = unit_vector((-center1[0]+v0[0],-center1[1]+v0[1],-center1[2]+v0[2]))
        v1c = unit_vector((-center2[0]+v1[0],-center2[1]+v1[1],-center2[2]+v1[2]))
        #twist a second time (twitst method wont do anything if the angle is 0)
        angle2 = angle_between_vectors(tuple(v1c),tuple(v0c))
        figure.twist(angle2)
        return figure

    def connect(self, figure):
        if isinstance(figure, Circle3D):
            return self._connect_to_circle3d(figure,1)  # the 1 means it will connect the tail
        elif isinstance(figure, CylindricalPart):
            return self._connect_to_cylindricalpart(figure)

    def _connect_to_point(self, point):
        pass

    def _connect_to_circle3d(self, circle, face=None):
        res = CylindricalPart()
        n_vertices1 = self.n_vertices()
        n_vertices2 = circle.n_vertices()
        for i in xrange(n_vertices1):
            index = res.add_vertex(self.vertex(i))
            res.add_normal(index, self.normal(i))
        # Copy current triangles in the part
        res.triangles = dict(self.triangles)
        res.triangles_count = self.triangles_count
        cur_index = None
        cur_face = None
        cur_info = None
        cur_distance = 9999
        p2 = circle.center
        if face is None:
            for index, face in self.connection_faces.iteritems():
                info = self.get_face_info(index)
                p1 = info[0]
                d = (p1[0]-p2[0], p1[1]-p2[1], p1[2]-p2[2])
                distance = abs(vector_norm(d))
                if distance < cur_distance:
                    cur_face = face
                    cur_info = info
                    cur_distance = distance
                    cur_index = index
        else:
            cur_face = self.connection_face(face)
            cur_index = face
        new_indexes = {}
        for i in xrange(n_vertices2):
            index = res.add_vertex(circle.vertex(i))
            new_indexes[i] = index
            res.add_normal(index, circle.normal(i))
        # in future, check for optimal vertex connection? (i.e. search
        # for the nearest vertex of each original one
        n_vertices = len(cur_face)
        for i in xrange(n_vertices):
            res.add_triangle(( cur_face[i],
                               new_indexes[i],
                               cur_face[(i+1) % n_vertices]))
            res.add_triangle(( cur_face[(i+1) % n_vertices],
                               new_indexes[i],
                               new_indexes[(i+1) % n_vertices]))
        # Copy this properly!!
        res.connection_faces = dict(self.connection_faces)
        res.connection_faces[cur_index] = new_indexes.values()
        res.face_count = self.face_count
        return res

    def _connect_to_cylindricalpart(self, part):
        # We assume that the two cylinderparts have
        # a face in common, so we look for which faces to merge them.
        # Later we can think about moving the pieces
        res = CylindricalPart()
        n_vertices1 = self.n_vertices()
        n_vertices2 = part.n_vertices()
        face1 = None
        face2 = None
        for i in xrange(self.n_faces()):
            cur_face1 = self.connection_face(i)
            # we check with one of the vertex
            v = self.vertex(cur_face1[0])
            for j in xrange(part.face_count):
                cur_face2 = part.connection_face(j)
                for v_index in cur_face2:
                    vertex = part.vertex(v_index)
                    # if equal_vertices(v,vertex,eps):
                    if equal_vertices(v,vertex):
                        face2 = j
                        break
                if face2 is not None:
                    break
            if face2 is not None:
                face1 = i
                break
        vertices1 = self.connection_face(face1)
        vertices2 = part.connection_face(face2)
        id_check = {}
        for i in xrange(len(vertices1)):
            id_check[vertices2[i]] = vertices1[i]
        for i in xrange(n_vertices1):
            index = res.add_vertex(self.vertex(i))
            res.add_normal(index, self.normal(i))
        # Copy current triangles in the cylinder
        res.triangles = dict(self.triangles)
        res.triangles_count = self.triangles_count
        for i in xrange(n_vertices2):
            if i not in id_check.keys():
                index = res.add_vertex(part.vertex(i))
                id_check[i] = index
                res.add_normal(index, part.normal(i))
        for t in xrange(part.triangles_count):
            current_t = part.triangle(t)
            p1 = id_check[current_t[0]]
            p2 = id_check[current_t[1]]
            p3 = id_check[current_t[2]]
            res.add_triangle((p1,p2,p3))
        # Add the other connection face of this object
        for i in xrange(self.face_count):
            if i != face1:
                cur_f = self.connection_face(i)
                res.add_connection_face(cur_f)
        # Add the other connection face of the part
        for i in xrange(part.face_count):
            if i != face2:
                f = part.connection_face(i)
                cur_f = [ id_check[vertex] for vertex in f ]
                res.add_connection_face(cur_f)
        return res

    @property
    def resolution(self):
        if self.n_faces > 0:
            return len(self.connection_faces[0])
        return 0
        