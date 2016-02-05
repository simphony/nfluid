import math
import numpy as np
import bisect

from visvis import OrientableMesh
from simphony.cuds.mesh import Point, Face, Cell, Mesh
from nfluid.external.transformations import rotation_matrix
# from nfluid.external.transformations import angle_between_vectors
from nfluid.external.transformations import vector_product
from nfluid.external.transformations import unit_vector
from nfluid.external.transformations import vector_norm
from nfluid.geometry.functions import cos_table, sin_table
from nfluid.geometry.functions import angle_between_vectors
from nfluid.geometry.functions import normal_of, center_of, distance
from nfluid.geometry.auxiliar_geometry import Plane, Line3D
import visvis as vv
import copy

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

    def copy_from_geometricmesh(self, geommesh):
        self.vertex_count = geommesh.vertex_count
        self.normals_count = geommesh.normals_count
        self.triangles_count = geommesh.triangles_count
        self.vertices = dict(geommesh.vertices)
        self.normals = dict(geommesh.normals)
        self.triangles = dict(geommesh.triangles)

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
        # if len(self.normals) is not 0:
        #     normals = self.normals.values()
        # else:
        #     normals = None
        normals = None
        if len(self.triangles) is not 0:
            faces = self.triangles.values()
        else:
            faces = None
        res = OrientableMesh(parent=vv.gca(), vertices=vertices,
                             normals=normals,
                             faces=faces, verticesPerFace=3)
        return res

    def to_simphony_mesh(self):
        res = Mesh('new_mesh')
        v_ids_matching = {}
        t_ids_matching = {}
        for id, v_coords in self.vertices.iteritems():
            new_id = res.add_points([Point(v_coords)])
            v_ids_matching[id] = new_id
        for id, triangle in self.triangles.iteritems():
            new_id = res.add_faces([Face((v_ids_matching[triangle[0]],
                                          v_ids_matching[triangle[1]],
                                          v_ids_matching[triangle[2]]))])
            t_ids_matching[id] = new_id
        res.add_cells([Cell(v_ids_matching.values())])
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
        if angle == math.pi or angle == 0:
            aux_plane = Plane(p, n)
            aux_point = aux_plane.get_point()
            vect = unit_vector((aux_point[0]-p[0],
                               aux_point[1]-p[1],
                               aux_point[2]-p[2]))
        else:
            vect = unit_vector(vector_product(direction, n))

        rot_m = rotation_matrix(angle, vect)
        d = (point[0]-p[0], point[1]-p[1], point[2]-p[2])
        t = (-p[0], -p[1], -p[2])
        for k, v in self.vertices.iteritems():
            n_v = (v[0]+t[0], v[1]+t[1], v[2]+t[2])
            if (angle != 0.0 and angle != 2*math.pi and
                    math.isnan(angle) is False):
                n_v = np.dot(n_v+(1,), rot_m)
            n_v = (n_v[0]+d[0]-t[0], n_v[1]+d[1]-t[1], n_v[2]+d[2]-t[2])
            self.update_vertex(k, n_v)

    def _set_orientation(self, angle, dir, center):
        v_rot = dir
        t = (-center[0], -center[1], -center[2])
        if angle != 0.0 and math.isnan(angle) is False:
            rot_m = rotation_matrix(angle, v_rot)
            for k, v in self.vertices.iteritems():
                n_v = (v[0]+t[0], v[1]+t[1], v[2]+t[2])
                n_v = np.dot(n_v+(1,), rot_m)
                n_v = (n_v[0]-t[0], n_v[1]-t[1], n_v[2]-t[2])
                self.update_vertex(k, n_v)

    def link(self, figure, conn_face=0):
        pass

    def attach(self, figure, conn_face=0):
        """Means to move the head face of 'figure' to
        the tail head of self, first step to link the two
        meshes into one."""
        pass

    def adapt(self, figure, conn_face=0):
        """This method is necessary to make coincident all the vertices
        of the two faces of the figures we are linking. This means that
        to adapt we must have attached self and 'figure'."""
        pass

    def connect(self, figure, conn_face=0):
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

    def connected(self, v0, v1):
        """Checks if the two given vertex are connected or not."""
        for t in self.triangles.itervalues():
            if v0 in t and v1 in t:
                return True
        return False

    def compute_normals(self):
        # we make a dictionary containing all the triangles in which
        # each vertex is involved in
        triangles_of = {}
        for id, vertex_ids in self.triangles.iteritems():
            for v_id in vertex_ids:
                try:
                    triangles_of[v_id].append(id)
                except:
                    triangles_of[v_id] = []
                    triangles_of[v_id].append(id)
        # now we compute the normal of each vertex, using the average of
        # the normals of surrounding triangles
        for v_id, triangles in triangles_of.iteritems():
            vt_ids = [self.triangle(t_id) for t_id in triangles]
            normals = [normal_of(self.vertex(t[0]),
                       self.vertex(t[1]), self.vertex(t[2])) for t in vt_ids]
            new_normal = self._avg_normal(normals)
            self.update_normal(v_id, new_normal)

    def _avg_normal(self, normals):
        res = [0, 0, 0]
        for n in normals:
            res[0] += n[0]
            res[1] += n[1]
            res[2] += n[2]
        n_normals = len(normals)
        return (res[0]/n_normals, res[1]/n_normals, res[2]/n_normals)

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
        alpha = angle_between_vectors(u, v)
        step = alpha / slices
        for i in xrange(slices+1):
            beta = i*step
            x = (midpoint[0] +
                 ((math.sin(alpha-beta)*u[0] + math.sin(beta)*v[0]) /
                  (math.sin(alpha)))
                 )
            y = (midpoint[1] +
                 ((math.sin(alpha-beta)*u[1] + math.sin(beta)*v[1]) /
                  (math.sin(alpha)))
                 )
            z = (midpoint[2] +
                 ((math.sin(alpha-beta)*u[2] + math.sin(beta)*v[2]) /
                  (math.sin(alpha)))
                 )
            p = (x, y, z)
            self.add_vertex(p)
        # IMPORTANT: AS A GEOMETRICMESH, IT SHOULD CALCULATE NORMALS
        # TOO; NOT IMPLEMENTED ATM


class Circle3D(GeometricMesh):
    """Internal primary private class for the generator. It makes easier to
    construct complex 3D figures.

    P = R * cos(A) * U + R * sin(A) * V

    where:  R ==> Radius
            A ==> current angle of the circle in the loop
            U ==> Perpendicular vector to the normal of the circle
            V ==> Another perpendicular vector
    """
    def __init__(self, radius, slices, pos=(0.0, 0.0, 0.0),
                 normal=(0.0, 0.0, 1.0),
                 filled=False):
        super(Circle3D, self).__init__()
        self.radius = radius
        self.slices = slices
        self.center = pos
        self.normal_v = tuple(unit_vector(normal))
        # WE DONT SUPPORT IT WELL FTM
        self.filled = filled
        # Generate the cosine and sinus tables to obtain the points
        cos_t = cos_table(slices)
        sin_t = sin_table(slices)

        # Vectors inside the circle, same orientation for all the points
        v1 = unit_vector((1, 0, 0))
        v2 = unit_vector((0, 1, 0))
        points = ()
        # Generate the points:
        for i in xrange(slices):
            p = (radius*cos_t[i]*v1[0] + radius*sin_t[i]*v2[0],
                 radius*cos_t[i]*v1[1] + radius*sin_t[i]*v2[1],
                 radius*cos_t[i]*v1[2] + radius*sin_t[i]*v2[2])
            points = points + (p,)
        # Rotate the points if needed (i.e. the normal is not (0,0,1)
        rot_points = ()
        angle_z = angle_between_vectors((0, 0, 1), self.normal_v)
        if angle_z != 0:
            if angle_z != math.pi:
                rot_vect = unit_vector(np.cross(self.normal_v, (0, 0, 1)))
            else:
                rot_vect = (1, 0, 0)
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
            index = self.add_vertex(tuple(map(lambda x, y: x + y, p,
                                    self.center)))
            self.add_normal(index, p)
        # If the circle is filled we need to create an additional point
        # and triangles
        if self.filled:
            self.center = self.add_vertex(self.center)
            self.add_normal(self.center, self.normal_v)
            for i in xrange(slices+1):
                self.add_triangle((i, self.center, (i + 1) % slices))

    def _connect_to_point(self, point):
        # FIX THIS! COPY METHODS!

        res = CylindricalPart()
        res.vertices = dict(self.vertices)
        res.n_vertices = self.n_vertices
        res.normals = dict(self.normals)
        res.triangles = dict(self.triangles)
        res.n_triangles = self.triangles
        cap = res.add_vertex(point)
        res.add_normal(cap, point)

        for i in xrange(self.slices):
            res.add_triangle((i, cap, (i + 1) % self.slices))
        return res

    def flip(self):
        """This changes the orientation of the vertices without modifying the circle.
        The 1st vertex is the pivot."""
        n_vertices = self.vertex_count
        for i in xrange(1, n_vertices / 2):
            i0 = i
            i1 = n_vertices-i
            p0 = self.vertex(i0)
            p1 = self.vertex(i1)
            self.update_vertex(i0, p1)
            self.update_vertex(i1, p0)

    def set_orientation(self, angle):
        angle = np.radians(angle)
        self._set_orientation(angle, self.normal_v, self.center)
        # update normal and center
        self.normal_v = normal_of(self.vertex(0), self.vertex(1),
                                  self.vertex(2))
        self.center = center_of([p for p in self.vertices.itervalues()])

    def move(self, point=None, direction=None, center=False):
        if center:
            raise NotImplementedError()
        else:
            if point is None:
                point = self.center
            if direction is None:
                direction = self.normal_v
            self._move(point, direction, self.center, self.normal_v)
            self.normal_v = normal_of(self.vertex(0), self.vertex(1),
                                      self.vertex(2))
            self.center = center_of([p for p in self.vertices.itervalues()])

    def adapt(self, figure, conn_face=0):
        if isinstance(figure, Circle3D):
            org_center, org_normal = figure.center, figure.normal_v
            figure.move(self.center, self.normal_v)
            p0 = self.vertex(0)
            v0 = unit_vector((p0[0]-self.center[0], p0[1]-self.center[1],
                             p0[2]-self.center[2]))
            p1 = figure.vertex(0)
            v1 = unit_vector((p1[0]-figure.center[0], p1[1]-figure.center[1],
                             p1[2]-figure.center[2]))
            angle = angle_between_vectors(v0, v1)
            iterations = 100
            while angle > 0 and iterations:
                figure.set_orientation(np.degrees(angle))
                prev_angle = angle
                # twist the figure
                p0 = self.vertex(0)
                p1 = figure.vertex(0)
                center1 = self.center
                center2 = figure.center
                v0c = unit_vector((-center1[0]+p0[0], -center1[1]+p0[1],
                                   -center1[2]+p0[2]))
                v1c = unit_vector((-center2[0]+p1[0], -center2[1]+p1[1],
                                   -center2[2]+p1[2]))
                # twist a second time (twitst method wont do anything
                # if the angle is 0)
                angle = angle_between_vectors(tuple(v1c), tuple(v0c))
                if angle > prev_angle:
                    angle = 2*math.pi - angle
                iterations -= 1
            figure.move(org_center, org_normal)
        return figure

    def connect(self, figure, conn_face=0):
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
            res.add_connection_face(
                tuple([x+n_vertices for x in xrange(n_vertices)]))
            return res
        elif isinstance(figure, StructuredCylindricalPart):
            return figure.connect(self)
        elif isinstance(figure, CylindricalPart):
            return figure.connect(self)
        else:
            return self._connect_to_point(figure)


class CylindricalPart(GeometricMesh):
    """Class representing a piece made of circles, whatever its form is.
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

    def move(self, point=None, direction=None, center=False):
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
            if point is None:
                point = p
            if direction is None:
                direction = n
            self._move(point, direction, p, n)

    def set_orientation(self, angle):
        # Maybe a better name for it?
        angle = np.radians(angle)
        # We orientate taking into account the base face - head
        center, normal = self.get_face_info(0)
        self._set_orientation(angle, normal, center)

    def link(self, figure, conn_face=0):
        res = self.attach(figure, conn_face)
        res = self.adapt(res, conn_face)
        res = self.connect(res, conn_face)
        return res

    def attach(self, figure, conn_face=0):
        # Last face (considered tail ftm)
        # with the conn_face modification, there is no conflict with tees
        center1, normal1 = self.get_face_info(1+conn_face)
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
                t = (-center[0], -center[1], -center[2])
                for k, v in map(None, cur_indexes, cur_vertices):
                    n_v = (v[0]+t[0], v[1]+t[1], v[2]+t[2])
                    n_v = np.dot(n_v+(1,), rot_m)
                    n_v = (n_v[0]-t[0], n_v[1]-t[1], n_v[2]-t[2])
                    self.update_vertex(k, n_v)

    def adapt(self, figure, conn_face=0):
        # We dont adapt tee! stub, maybe we should change this
        print "--- adapt; figure, nfaces: ", figure, figure.n_faces()
        if figure.n_faces() > 2:
            return figure
        # Calculate angle of twist
        center1, normal1 = self.get_face_info(1+conn_face)
        center2, normal2 = figure.get_face_info(0)
        face1 = self.connection_face(1+conn_face)
        face2 = figure.connection_face(0)
        # n_vertices1 = self.n_vertices()
        # n_vertices2 = figure.n_vertices()
        v0 = self.vertex(face1[0])
        v1 = figure.vertex(face2[0])
        v0c = unit_vector((-center1[0]+v0[0], -center1[1]+v0[1],
                           -center1[2]+v0[2]))
        v1c = unit_vector((-center2[0]+v1[0], -center2[1]+v1[1],
                           -center2[2]+v1[2]))
        angle = angle_between_vectors(v1c, v0c)
        iterations = 100
        while angle > 0 and iterations:
            prev_angle = angle
            # twist the figure
            figure.twist(angle)
            v0 = self.vertex(face1[0])
            v1 = figure.vertex(face2[0])
            v0c = unit_vector((-center1[0]+v0[0], -center1[1]+v0[1],
                              -center1[2]+v0[2]))
            v1c = unit_vector((-center2[0]+v1[0], -center2[1]+v1[1],
                              -center2[2]+v1[2]))
            angle = angle_between_vectors(v1c, v0c)
            if angle > prev_angle:
                angle = 2*math.pi - angle
            iterations -= 1
        return figure

    def connect(self, figure, conn_face=0):
        if isinstance(figure, Circle3D):
            # the 1 means it will connect the tail
            return self._connect_to_circle3d(figure, 1)
        elif isinstance(figure, StructuredCylindricalPart):
            return figure._connect_to_structuredcylindricalpart(self)
        elif isinstance(figure, CylindricalPart):
            return self._connect_to_cylindricalpart(figure)

    def _connect_to_point(self, point):
        pass

    def _connect_to_circle3d(self, circle, face=None):
        res = CylindricalPart()
        n_vertices1 = self.n_vertices()
        n_vertices2 = circle.n_vertices()
        # vertex_coordinates = []
        for i in xrange(n_vertices1):
            index = res.add_vertex(self.vertex(i))
            res.add_normal(index, self.normal(i))
        # Copy current triangles in the part
        res.triangles = dict(self.triangles)
        res.triangles_count = self.triangles_count
        cur_index = None
        cur_face = None
        # cur_info = None
        cur_distance = 9999
        p2 = circle.center
        if face is None:
            for index, face in self.connection_faces.iteritems():
                info = self.get_face_info(index)
                p1 = info[0]
                d = (p1[0]-p2[0], p1[1]-p2[1], p1[2]-p2[2])
                c_distance = abs(vector_norm(d))
                if c_distance < cur_distance:
                    cur_face = face
                    # cur_info = info
                    cur_distance = c_distance
                    cur_index = index
        else:
            cur_face = self.connection_face(face)
            cur_index = face
        new_indexes = {}
        for i in xrange(n_vertices2):
            index = res.add_vertex(circle.vertex(i))
            new_indexes[i] = index
            res.add_normal(index, circle.normal(i))
        # calculate intersection of the connection face vertices
        # with plane of the circle, so we obtain the optimal connection
        vertex_coords = [self.vertex(index_) for index_ in cur_face]
        # projected_coords = []
        # center_face = center_of(vertex_coords)
        # center_circle = center_of(circle.vertices.values())
        new_i_connections = []
        picked = []
        connections_dict = {}
        # We search for the minimum distance between the vertices that
        # havent been chosen yet
        # note: can we optimize this??
        for j in xrange(len(vertex_coords)):
            min_distance = 999
            min_index = -1
            v_picked = -1
            for i in xrange(len(vertex_coords)):
                v_coords = vertex_coords[i]
                v_index = cur_face[i]
                if v_index not in picked:
                    for prev_i, cur_i in new_indexes.iteritems():
                        if (cur_i not in new_i_connections):
                            cur_v = res.vertex(cur_i)
                            cur_distance = distance(v_coords, cur_v)
                            if cur_distance < min_distance:
                                min_distance = cur_distance
                                min_index = cur_i
                                v_picked = v_index
            new_i_connections.append(min_index)
            picked.append(v_picked)
            connections_dict[v_picked] = min_index
        n_vertices = len(cur_face)
        for i in xrange(n_vertices):
            res.add_triangle((cur_face[i],
                              connections_dict[cur_face[i]],
                              cur_face[(i+1) % n_vertices]))
            res.add_triangle((cur_face[(i+1) % n_vertices],
                              connections_dict[cur_face[i]],
                              connections_dict[cur_face[(i+1) % n_vertices]]))
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
        min_distance = 9999
        for i in xrange(self.n_faces()):
            cur_face1 = self.connection_face(i)
            # we check with the center of the face
            cur_center1 = center_of([self.vertex(v) for v in cur_face1])
            # v = self.vertex(cur_face1[0])
            for j in xrange(part.face_count):
                cur_face2 = part.connection_face(j)
                cur_center2 = center_of([part.vertex(v) for v in cur_face2])
                cur_distance = distance(cur_center1, cur_center2)
                if cur_distance < min_distance:
                    face1 = i
                    face2 = j
                    min_distance = cur_distance
        vertices1 = self.connection_face(face1)
        vertices2 = part.connection_face(face2)
        id_check = {}
        # Note: we dont need to project the vertices because, after
        # the attach operation, we suposse all the vertex of both faces
        # are coplanar!
        new_vertices1 = []
        vertex_coordinates = [(v, self.vertex(v)) for v in vertices1]
        for v in vertices2:
            v_coords = part.vertex(v)
            min_distance = 999
            min_index = -1
            for vert in vertex_coordinates:
                cur_distance = distance(vert[1], v_coords)
                if (cur_distance < min_distance and
                        vert[0] not in new_vertices1):
                    min_distance = cur_distance
                    min_index = vert[0]
            new_vertices1.append(min_index)

        for i in xrange(len(vertices1)):
            id_check[vertices2[i]] = new_vertices1[i]
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
            res.add_triangle((p1, p2, p3))

        # COMMENT: CONNECTION FACES ORDER DOES MATTER!!!! KEEP IT!!!
        # Add the other connection face of this object
        for i in xrange(self.face_count):
            if i != face1:
                cur_f = self.connection_face(i)
                res.add_connection_face(tuple(cur_f))
            else:
                for i in xrange(part.face_count):
                    if i != face2:
                        f = part.connection_face(i)
                        cur_f = [id_check[vertex] for vertex in f]
                        res.add_connection_face(tuple(cur_f))
        return res

    def close(self):
        """This will close the mesh for the head and tail gates so we obtain a
        closed STL surface.
        NOTE: this will terminate the mesh, so there is no guarantee that the
        rest of operation will work after closing the mesh."""
        for i in xrange(self.n_faces()):
            face = self.connection_face(i)
            center, normal = self.get_face_info(i)
            v_index = self.add_vertex(center)
            for v1, v2 in zip(face, face[1:]+(face[0],)):
                self.add_triangle((v1, v_index, v2))

    def intersection_of_point(self, point, normal):
        ray = Line3D(point, normal)
        inter_point = None
        min_d = 9999
        for key, triangle in self.triangles.iteritems():
            v0 = self.vertex(triangle[0])
            v1 = self.vertex(triangle[1])
            v2 = self.vertex(triangle[2])
            n = normal_of(v0, v1, v2)
            plane = Plane(v0, n)
            inter = plane.intersection(ray)
            if inter is not None:
                if (not math.isnan(inter[0]) and
                        not math.isnan(inter[1]) and
                        not math.isnan(inter[2])):
                    # check if inside triangle
                    a = np.array([[v0[0], v1[0], v2[0]],
                                  [v0[1], v1[1], v2[1]],
                                  [v0[2], v1[2], v2[2]]])
                    b = np.array([inter[0], inter[1], inter[2]])
                    try:
                        s = np.linalg.solve(a, b)
                    except np.linalg.linalg.LinAlgError:
                        return None
                    if (s[0] >= 0 and s[0] <= 1 and
                            s[1] >= 0 and s[1] <= 1 and
                            s[2] >= 0 and s[2] <= 1):
                        cur_d = distance(inter, point)
                        if cur_d < min_d:
                            inter_point = ((inter, key))
                            min_d = cur_d
        return inter_point
        
    def intersections_of_point(self, point, normal):
        ray = Line3D(point, normal)
        inter_points = []
        inter_point = None
        min_d = 9999
        for key, triangle in self.triangles.iteritems():
            v0 = self.vertex(triangle[0])
            v1 = self.vertex(triangle[1])
            v2 = self.vertex(triangle[2])
            n = normal_of(v0, v1, v2)
            plane = Plane(v0, n)
            inter = plane.intersection(ray)
            if inter is not None:
                if (not math.isnan(inter[0]) and
                        not math.isnan(inter[1]) and
                        not math.isnan(inter[2])):
                    # check if inside triangle
                    a = np.array([[v0[0], v1[0], v2[0]],
                                  [v0[1], v1[1], v2[1]],
                                  [v0[2], v1[2], v2[2]]])
                    b = np.array([inter[0], inter[1], inter[2]])
                    try:
                        s = np.linalg.solve(a, b)
                    except np.linalg.linalg.LinAlgError:
                        return None
                    if (s[0] >= 0 and s[0] <= 1 and
                            s[1] >= 0 and s[1] <= 1 and
                            s[2] >= 0 and s[2] <= 1):
                        inter_points.append((inter, key))
        return inter_points

    def is_inside(self, point, inter_points=None):
        # copy_mesh = copy.deepcopy(self)
        # copy_mesh.close()
        # inter_points = copy_mesh.intersections_of_point(point, (0,1,0))
        if inter_points is None:
            inter_points = self.intersections_of_point(point, (0,1,0))
        left = 0
        right = 0
        for coords, key in inter_points:
            cur_n = (coords[0]-point[0], coords[1]-point[1], coords[2]-point[2])
            if cur_n[1] < 0:
                left += 1
            else:
                right += 1
        # print "point"        
        # print point        
        # print "left - right"
        # print left, right
        if left % 2 != 0 and right % 2 != 0:
            return True
        return False

    def fill_mesh(self, step, filename):
        self.close()
        limits = self.coord_limits()
        # cube = mesh.generate_cubic_mesh(limits['x_min'],limits['x_max'],limits['y_min'],limits['y_max'],limits['z_min'],limits['z_max'], step)
        
        x_min = limits['x_min']
        y_min = limits['y_min']
        z_min = limits['z_min']
        x_max = limits['x_max']
        y_max = limits['y_max']
        z_max = limits['z_max']
        cur_x = x_min
        cur_y = y_min
        cur_z = z_min
        inside = []
        not_inside = []
        while cur_x < x_max:
            # print "X"
            # print cur_x, cur_y, cur_z
            while cur_z < z_max:
                # print "Z"
                # print cur_x, cur_y, cur_z
                p = (cur_x, cur_y, cur_z)
                inter_points = self.intersections_of_point(p, (0,1,0))
                while cur_y < y_max:
                    # print "Y"
                    # print cur_x, cur_y, cur_z
                    cur_p = (cur_x, cur_y, cur_z)
                    if self.is_inside(cur_p, inter_points):
                        inside.append(cur_p)
                    else:
                        not_inside.append(cur_p)
                    cur_y += step
                cur_y = y_min
                cur_z += step
            cur_z = z_min
            cur_x += step
        
        file_out = open(filename, 'w')

        total_v = len(inside)
        file_out.write('{}\n'.format(total_v))
        file_out.write('---------------\n')
        spec = 'O'
        for v in inside:
            file_out.write('{0} {1} {2} {3}\n'.format(spec, v[0], v[1], v[2]))
            
        file_out.close()
        
        return not_inside

    def coord_limits(self):
        x_min = 9999
        x_max = -9999
        y_min = 9999
        y_max = -9999
        z_min = 9999
        z_max = -9999
        for v in self.vertices.itervalues():
            if v[0] < x_min:
                x_min = v[0]
            if v[0] > x_max:
                x_max = v[0]
            if v[1] < y_min:
                y_min = v[1]
            if v[1] > y_max:
                y_max = v[1]
            if v[2] < z_min:
                z_min = v[2]
            if v[2] > z_max:
                z_max = v[2]
        return {'x_min':x_min, 'x_max':x_max, 
                'y_min':y_min, 'y_max':y_max,
                'z_min':z_min, 'z_max':z_max}
        
    # @classmethod
    def generate_cubic_mesh(self, x_min, x_max, y_min, y_max, z_min, z_max, step=1):
        res = GeometricMesh()
        x_len = x_max - x_min
        y_len = y_max - y_min
        z_len = z_max - z_min
        cur_x = x_min
        cur_y = y_min
        cur_z = z_min
        while cur_x < x_max:
            while cur_y < y_max:
                while cur_z < z_max:
                    res.add_vertex((cur_x, cur_y, cur_z))
                    cur_z += step
                cur_z = z_min
                cur_y += step
            cur_y = y_min
            cur_x += step
        return res
        

    def intersection(self, figure):
        """This calculates an returns the intersection of the vertices of
        figure with the triangles of self. Returns a list of tuples with:
        (inter_point, triangle_number).
        """
        if isinstance(figure, Circle3D):
            points_inside = []
            for i in xrange(figure.n_vertices()):
                inter_point = self.intersection_of_point(figure.vertex(i),
                                                         figure.normal_v)
                if inter_point is not None:
                    points_inside.append(inter_point)
            return points_inside

    def insert_point(self, point, triangle=None):
        """Inserts a point in the mesh, recalculating triangles.
        If triangle is specified, we know with which vertices of
        our mesh we have to calculate new triangles, so is more efficient.
        It returns index of the new point and new triangles.
        """
        if triangle is not None:
            index = self.add_vertex(point)
            vertices = self.triangle(triangle)
            self.update_triangle(triangle, (index, vertices[1], vertices[0]))
            i1 = self.add_triangle((index, vertices[2], vertices[1]))
            i2 = self.add_triangle((index, vertices[0], vertices[2]))
            return (index, (triangle, i1, i2))
        else:
            # TODO
            pass

    def connect_points(self, p0, p1, t0=None, t1=None):
        """Connect two points, recalculating triangles between them.
        p0 and p1 are the points, t0 and t1 are their current triangles.
        If specified, the process will be more efficient.
        """
        if t0 is not None and t1 is not None:
            # We search for the triangles that are adjacent (this is,
            # they have 2 vertices in common
            for cur_triangle_index in t0:
                cur_triangle = list(self.triangle(cur_triangle_index))
                for triangle_index in t1:
                    triangle = list(self.triangle(triangle_index))
                    n_vertex = 0
                    for v in cur_triangle:
                        if v in triangle:
                            n_vertex += 1
                    if n_vertex == 2:
                        # We change the triangles
                        index_changed = None
                        for i in xrange(len(cur_triangle)):
                            i0 = cur_triangle[i]
                            if i0 in triangle:
                                index_changed = i0
                                cur_triangle[i] = p1
                        for j in xrange(len(triangle)):
                            i1 = triangle[j]
                            if i1 in cur_triangle and i1 != index_changed:
                                triangle[j] = p0
                        self.update_triangle(cur_triangle_index,
                                             tuple(cur_triangle))
                        self.update_triangle(triangle_index, tuple(triangle))
                        break
        else:
            # TODO
            pass

    def flip_connection_face(self, face):
        face_vertices = self.connection_face(face)
        n_vert = len(face_vertices)
        count = 0
        new_face_vertices = list(face_vertices)
        for i in face_vertices:
            i0 = i
            i1 = face_vertices[(n_vert-1)-count]
            new_face_vertices[count] = face_vertices[(n_vert-1)-count]
            new_face_vertices[(n_vert-1)-count] = face_vertices[count]
            p0 = self.vertex(i0)
            p1 = self.vertex(i1)
            self.update_vertex(i0, p1)
            self.update_vertex(i1, p0)
            count += 1
        face_vertices = list(new_face_vertices)
        self.connection_faces[face] = face_vertices

    def to_structuredcylindricalpart(self):
        res = StructuredCylindricalPart()

        res.vertex_count = self.vertex_count
        res.normals_count = self.normals_count
        res.triangles_count = self.triangles_count
        res.face_count = self.face_count
        res.vertices = dict(self.vertices)
        res.normals = dict(self.normals)
        res.triangles = dict(self.triangles)
        res.connection_faces = dict(self.connection_faces)

        resolution = self.resolution
        cur_set = []
        for v in xrange(res.vertex_count):
            cur_set.append(v)
            if len(cur_set) == resolution:
                res.add_set(tuple(cur_set))
                cur_set = []
        return res

    def copy_from_cylindricalpart(self, cylpart):
        self.copy_from_geometricmesh(cylpart)
        self.connection_faces = dict(cylpart.connection_faces)
        self.face_count = cylpart.face_count

    @property
    def resolution(self):
        if self.n_faces > 0:
            return len(self.connection_faces[0])
        return 0


class StructuredCylindricalPart(CylindricalPart):
    """This class represents any cylindrical part that has to keep track
    of how the vertices are organized along faces, so the algorithms can be
    applied without problems."""
    def __init__(self):
        super(StructuredCylindricalPart, self).__init__()
        self.sets = []

    def add_set(self, set):
        index = len(self.sets)
        bisect.insort(self.sets, (index, set))
        return index

    def get_set(self, key):
        # sets = [s[1] for s in self.sets]
        i = bisect.bisect_left(self.sets, (key, []))
        if i != len(self.sets) and self.sets[i][0] == key:
            return self.sets[i]
        raise ValueError

    def add_connection_face(self, face):
        self.connection_faces[self.face_count] = face
        self.face_count = self.face_count + 1

    def twist(self, angle):
        if angle != 0.0 and math.isnan(angle) is False:
            for set in self.sets:
                # i = set[0]
                vertices = set[1]
                cur_indexes = vertices
                cur_vertices = [self.vertex(index) for index in cur_indexes]
                c_normal = normal_of(cur_vertices[0],
                                     cur_vertices[2],
                                     cur_vertices[1])
                rot_m = rotation_matrix(angle, c_normal)
                center = center_of(cur_vertices)
                t = (-center[0], -center[1], -center[2])
                for k, v in map(None, cur_indexes, cur_vertices):
                    n_v = (v[0]+t[0], v[1]+t[1], v[2]+t[2])
                    n_v = np.dot(n_v+(1,), rot_m)
                    n_v = (n_v[0]-t[0], n_v[1]-t[1], n_v[2]-t[2])
                    self.update_vertex(k, n_v)

    def connect(self, figure, conn_face=0):
        if isinstance(figure, Circle3D):
            # the 1 means it will connect the tail
            return self._connect_to_circle3d(figure, 1)
        elif isinstance(figure, StructuredCylindricalPart):
            return self._connect_to_structuredcylindricalpart(figure)
        elif isinstance(figure, CylindricalPart):
            return self._connect_to_cylindricalpart(figure)

    def _connect_to_point(self, point):
        pass

    def _connect_to_circle3d(self, circle, face=None):
        res = StructuredCylindricalPart()
        n_vertices1 = self.n_vertices()
        n_vertices2 = circle.n_vertices()
        for i in xrange(n_vertices1):
            index = res.add_vertex(self.vertex(i))
            try:
                res.add_normal(index, self.normal(i))
            except:
                pass
        # Copy current triangles in the part
        res.triangles = dict(self.triangles)
        res.sets = list(self.sets)
        res.triangles_count = self.triangles_count
        cur_index = None
        cur_face = None
        # cur_info = None
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
                    # cur_info = info
                    cur_distance = distance
                    cur_index = index
        else:
            cur_face = self.connection_face(face)
            cur_index = face
        new_indexes = {}
        for i in xrange(n_vertices2):
            index = res.add_vertex(circle.vertex(i))
            new_indexes[i] = index
            try:
                res.add_normal(index, circle.normal(i))
            except:
                pass
        # in future, check for optimal vertex connection? (i.e. search
        # for the nearest vertex of each original one
        n_vertices = len(cur_face)
        for i in xrange(n_vertices):
            res.add_triangle((cur_face[i],
                              new_indexes[i],
                              cur_face[(i+1) % n_vertices]))
            res.add_triangle((cur_face[(i+1) % n_vertices],
                              new_indexes[i],
                              new_indexes[(i+1) % n_vertices]))
        # Copy this properly!!
        res.connection_faces = dict(self.connection_faces)
        res.connection_faces[cur_index] = new_indexes.values()
        res.face_count = self.face_count
        res.add_set(tuple(new_indexes.values()))
        return res

    def _connect_to_cylindricalpart(self, part):
        # We assume that the two cylinderparts have
        # a face in common, so we look for which faces to merge them.
        # Later we can think about moving the pieces
        res = StructuredCylindricalPart()
        # n_vertices1 = self.n_vertices()
        n_vertices2 = part.n_vertices()
        face1 = None
        face2 = None
        min_distance = 9999
        for i in xrange(self.n_faces()):
            cur_face1 = self.connection_face(i)
            # we check with the center of the face
            cur_center1 = center_of([self.vertex(v) for v in cur_face1])
            # v = self.vertex(cur_face1[0])
            for j in xrange(part.face_count):
                cur_face2 = part.connection_face(j)
                cur_center2 = center_of([part.vertex(v) for v in cur_face2])
                cur_distance = distance(cur_center1, cur_center2)
                if cur_distance < min_distance:
                    face1 = i
                    face2 = j
                    min_distance = cur_distance
        vertices1 = self.connection_face(face1)
        vertices2 = part.connection_face(face2)
        id_check = {}
        for i in xrange(len(vertices1)):
            id_check[vertices2[i]] = vertices1[i]
        res.vertices = dict(self.vertices)
        res.vertex_count = self.n_vertices()
        res.normals = dict(self.normals)
        res.normals_count = self.n_normals()
        res.sets = list(self.sets)
        # Copy current triangles in the cylinder
        res.triangles = dict(self.triangles)
        res.triangles_count = self.triangles_count
        vertices_to_add = []
        for i in xrange(n_vertices2):
            if i not in id_check.keys():
                index = res.add_vertex(part.vertex(i))
                vertices_to_add.append(index)
                id_check[i] = index
                try:
                    res.add_normal(index, part.normal(i))
                except:
                    pass
        for t in xrange(part.triangles_count):
            current_t = part.triangle(t)
            p1 = id_check[current_t[0]]
            p2 = id_check[current_t[1]]
            p3 = id_check[current_t[2]]
            res.add_triangle((p1, p2, p3))
        # Add the other connection face of this object
        for i in xrange(self.face_count):
            if i != face1:
                cur_f = self.connection_face(i)
                res.add_connection_face(tuple(cur_f))
        # Add the other connection face of the part
        for i in xrange(part.face_count):
            if i != face2:
                f = part.connection_face(i)
                cur_f = [id_check[vertex] for vertex in f]
                res.add_connection_face(tuple(cur_f))
        resolution = part.resolution
        cur_set = []
        for v in vertices_to_add:
            cur_set.append(v)
            if len(cur_set) == resolution:
                res.add_set(tuple(cur_set))
                cur_set = []
        return res

    def _connect_to_structuredcylindricalpart(self, part):
        res = StructuredCylindricalPart()
        # n_vertices1 = self.n_vertices()
        n_vertices2 = part.n_vertices()
        face1 = None
        face2 = None
        min_distance = 9999
        for i in xrange(self.n_faces()):
            cur_face1 = self.connection_face(i)
            # we check with the center of the face
            cur_center1 = center_of([self.vertex(v) for v in cur_face1])
            # v = self.vertex(cur_face1[0])
            for j in xrange(part.face_count):
                cur_face2 = part.connection_face(j)
                cur_center2 = center_of([part.vertex(v) for v in cur_face2])
                cur_distance = distance(cur_center1, cur_center2)
                if cur_distance < min_distance:
                    face1 = i
                    face2 = j
                    min_distance = cur_distance

        vertices1 = self.connection_face(face1)
        vertices2 = part.connection_face(face2)
        id_check = {}
        for i in xrange(len(vertices1)):
            id_check[vertices2[i]] = vertices1[i]
        res.vertices = dict(self.vertices)
        res.vertex_count = self.n_vertices()
        res.normals = dict(self.normals)
        res.normals_count = self.n_normals()
        res.sets = list(self.sets)
        # Copy current triangles in the cylinder
        res.triangles = dict(self.triangles)
        res.triangles_count = self.triangles_count
        vertices_to_add = []
        for i in xrange(n_vertices2):
            if i not in id_check.keys():
                index = res.add_vertex(part.vertex(i))
                vertices_to_add.append(index)
                id_check[i] = index
                try:
                    res.add_normal(index, part.normal(i))
                except:
                    pass
        for t in xrange(part.triangles_count):
            current_t = part.triangle(t)
            p1 = id_check[current_t[0]]
            p2 = id_check[current_t[1]]
            p3 = id_check[current_t[2]]
            res.add_triangle((p1, p2, p3))
        # Add the other connection face of this object
        for i in xrange(self.face_count):
            if i != face1:
                cur_f = self.connection_face(i)
                res.add_connection_face(tuple(cur_f))
        # Add the other connection face of the part
        for i in xrange(part.face_count):
            if i != face2:
                f = part.connection_face(i)
                cur_f = [id_check[vertex] for vertex in f]
                res.add_connection_face(tuple(cur_f))
        # resolution = part.resolution
        current_sets = [s[1] for s in res.sets]
        for s in part.sets:
            transformed_set = tuple([id_check[vertex] for vertex in s[1]])
            if transformed_set not in current_sets:
                res.add_set(transformed_set)
        return res
