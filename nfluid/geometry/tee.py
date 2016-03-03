from nfluid.geometry.geometricmesh import Circle3D, CylindricalPart
from nfluid.visualisation.show import show
from nfluid.geometry.functions import normal_of, center_of
from visvis import solidLine, Pointset, Point


class Tee(CylindricalPart):
    def __init__(self, r, slices, stacks):
        super(Tee, self).__init__()
        normals = []
        long = 5
        self.r = r
        eps = 0.1
        face1 = Circle3D(r, slices, pos=(0, 0, 0), normal=(0, -1, 0))
        face2 = Circle3D(r, slices, pos=(0, r*2+eps, 0), normal=(0, -1, 0))
        circle = Circle3D(r, slices, pos=(0, r+eps/2.0, 0), normal=(0, 0, 1))
        circle_test = Circle3D(r, slices, pos=(0, r+eps/2.0, -r-eps),
                               normal=(0, 0, 1))
        if slices % 2 != 0:
            factor = 1
        else:
            factor = 0
        # These are the indexes for the Z component of the vertices
        n_vert = circle.n_vertices()
        face_indexes = []
        face_indexes.extend([i for i in xrange((n_vert / 2)+factor)])
        if slices % 2 != 0:
            face_indexes.append(n_vert/2)
        else:
            face_indexes.append(0)
        face_indexes.extend([i for i in xrange((n_vert / 2))][:0:-1])
        for i in xrange(n_vert):
            cur_v = circle.vertex(i)
            face_v = face1.vertex(face_indexes[i])
            # We change the Z coordinate
            cur_v = (cur_v[0], cur_v[1], face_v[2])
            circle.update_vertex(i, cur_v)
        cyl = face1.connect(face2)
        involved_vertices = [i+1 for i in xrange(((n_vert/2)+factor)-1)]
        involved_vertices.extend(
            [i+1+n_vert for i in xrange(((n_vert/2)+factor)-1)])
        for vertex in involved_vertices:
            for k, t in cyl.triangles.iteritems():
                if vertex in t:
                    cyl.triangles[k] = ()

        new_triangles = {}
        new_triangles_count = 0
        for k, t in cyl.triangles.iteritems():
            if t != ():
                new_triangles[new_triangles_count] = t
                new_triangles_count += 1

                v0 = cyl.vertex(t[0])
                v1 = cyl.vertex(t[1])
                v2 = cyl.vertex(t[2])
                c_n = normal_of(v0,v1,v2)
                c_c = center_of([v0,v1,v2])
                c_c2 = [c_c[0] + c_n[0] * long, c_c[1] + c_n[1] * long, c_c[2] + c_n[2] * long]
                ps = Pointset(3)
                ps.append(Point(c_c))
                ps.append(Point(c_c2))
                normals.append(ps)

        cyl.triangles = new_triangles
        cyl.triangles_count = new_triangles_count
        # We copy current information
        top = circle.connect(circle_test)
        count = 0
        new_connection_face = []
        index_match = {}
        for i in xrange(slices*2):
            index = cyl.add_vertex(top.vertex(i))
            # cyl.add_normal(index, top.normal(i))
            cyl.add_normal(index, (0, 0, 1))
            index_match[i] = index
            count = count + 1
            if count > n_vert:
                new_connection_face.append(index)
        cyl.add_connection_face(new_connection_face)
        # we swap connection faces, so 0 is the entrance, 1 and 2 the exits:
        aux = tuple(cyl.connection_face(0))
        cyl.connection_faces[0] = tuple(cyl.connection_faces[2])
        cyl.connection_faces[2] = aux
        for k, t in top.triangles.iteritems():
            cyl.add_triangle((index_match[t[0]], index_match[t[1]],
                              index_match[t[2]]))

            v0 = cyl.vertex(index_match[t[0]])
            v1 = cyl.vertex(index_match[t[1]])
            v2 = cyl.vertex(index_match[t[2]])
            c_n = normal_of(v0,v1,v2)
            c_c = center_of([v0,v1,v2])
            c_c2 = [c_c[0] + c_n[0] * long, c_c[1] + c_n[1] * long, c_c[2] + c_n[2] * long]
            ps = Pointset(3)
            ps.append(Point(c_c))
            ps.append(Point(c_c2))
            normals.append(ps)

        # We generate new triangles!
        prev_z = 999
        if n_vert % 2 != 0:
            for index in xrange(n_vert):
                cur_v = cyl.vertex(index_match[index])
                if index >= (n_vert/2)+factor:
                    internal_index = n_vert*2 - index
                    new_triangle1 = (index_match[index],
                                     index_match[(index+1) % n_vert],
                                     (internal_index))

                    v0 = cyl.vertex(index_match[index])
                    v1 = cyl.vertex(index_match[(index+1) % n_vert])
                    v2 = cyl.vertex(internal_index)
                    c_n = normal_of(v0,v1,v2)
                    c_c = center_of([v0,v1,v2])
                    c_c2 = [c_c[0] + c_n[0] * long, c_c[1] + c_n[1] * long, c_c[2] + c_n[2] * long]
                    ps = Pointset(3)
                    ps.append(Point(c_c))
                    ps.append(Point(c_c2))
                    normals.append(ps)

                    new_triangle2 = (index_match[(index+1) % n_vert],
                                     (internal_index-1),
                                     internal_index)

                    v0 = cyl.vertex(index_match[(index+1) % n_vert])
                    v1 = cyl.vertex((internal_index-1))
                    v2 = cyl.vertex(internal_index)
                    c_n = normal_of(v0,v1,v2)
                    c_c = center_of([v0,v1,v2])
                    c_c2 = [c_c[0] + c_n[0] * long, c_c[1] + c_n[1] * long, c_c[2] + c_n[2] * long]
                    ps = Pointset(3)
                    ps.append(Point(c_c))
                    ps.append(Point(c_c2))
                    normals.append(ps)

                else:
                    internal_index = index
                    new_triangle1 = (index_match[index],
                                     index_match[(index+1) % n_vert],
                                     (internal_index+1))

                    v0 = cyl.vertex(index_match[index])
                    v1 = cyl.vertex(index_match[(index+1) % n_vert])
                    v2 = cyl.vertex((internal_index+1))
                    c_n = normal_of(v0,v1,v2)
                    c_c = center_of([v0,v1,v2])
                    c_c2 = [c_c[0] + c_n[0] * long, c_c[1] + c_n[1] * long, c_c[2] + c_n[2] * long]
                    ps = Pointset(3)
                    ps.append(Point(c_c))
                    ps.append(Point(c_c2))
                    normals.append(ps)

                    new_triangle2 = (index_match[index], (internal_index+1),
                                     internal_index)

                    v0 = cyl.vertex(index_match[index])
                    v1 = cyl.vertex((internal_index+1))
                    v2 = cyl.vertex(internal_index)
                    c_n = normal_of(v0,v1,v2)
                    c_c = center_of([v0,v1,v2])
                    c_c2 = [c_c[0] + c_n[0] * long, c_c[1] + c_n[1] * long, c_c[2] + c_n[2] * long]
                    ps = Pointset(3)
                    ps.append(Point(c_c))
                    ps.append(Point(c_c2))
                    normals.append(ps)

                # we check if we have the two vertex of the polygon that
                # share a parallel of the original
                # cylinder. In this case, we'll have to generate
                # special triangles
                if abs(prev_z - cur_v[2]) <= 0.0001:
                    new_triangle3 = (index_match[index], internal_index+1,
                                     n_vert/2+1)


                    v0 = cyl.vertex(index_match[index])
                    v1 = cyl.vertex(internal_index+1)
                    v2 = cyl.vertex(n_vert/2+1)
                    c_n = normal_of(v0,v1,v2)
                    c_c = center_of([v0,v1,v2])
                    c_c2 = [c_c[0] + c_n[0] * long, c_c[1] + c_n[1] * long, c_c[2] + c_n[2] * long]
                    ps = Pointset(3)
                    ps.append(Point(c_c))
                    ps.append(Point(c_c2))
                    normals.append(ps)

                    new_triangle4 = (index_match[index], internal_index,
                                     internal_index+1)

                    v0 = cyl.vertex(index_match[index])
                    v1 = cyl.vertex(internal_index)
                    v2 = cyl.vertex(internal_index+1)
                    c_n = normal_of(v0,v1,v2)
                    c_c = center_of([v0,v1,v2])
                    c_c2 = [c_c[0] + c_n[0] * long, c_c[1] + c_n[1] * long, c_c[2] + c_n[2] * long]
                    ps = Pointset(3)
                    ps.append(Point(c_c))
                    ps.append(Point(c_c2))
                    normals.append(ps)

                    cyl.add_triangle(new_triangle3)
                    cyl.add_triangle(new_triangle4)
                cyl.add_triangle(new_triangle1)
                cyl.add_triangle(new_triangle2)
                prev_z = cur_v[2]
        else:

            for index in xrange(n_vert):
                cur_v = cyl.vertex(index_match[index])
                if index >= (n_vert/2)+factor:
                    internal_index = n_vert*2 - index
                    new_triangle1 = (index_match[index],
                                     index_match[(index+1) % n_vert],
                                     (internal_index))
                    v0 = cyl.vertex(index_match[index])
                    v1 = cyl.vertex(index_match[(index+1) % n_vert])
                    v2 = cyl.vertex((internal_index))
                    c_n = normal_of(v0,v1,v2)
                    c_c = center_of([v0,v1,v2])
                    c_c2 = [c_c[0] + c_n[0] * long, c_c[1] + c_n[1] * long, c_c[2] + c_n[2] * long]
                    ps = Pointset(3)
                    ps.append(Point(c_c))
                    ps.append(Point(c_c2))
                    normals.append(ps)
                    # print "N O R M A L t 1", c_n
                    # new_triangle2 = (index_match[(index+1) % n_vert],
                                     # (internal_index-1),
                                     # internal_index)
                    # new_triangle1 = ((internal_index),
                                     # index_match[(index+1) % n_vert],
                                     # index_match[index]
                                     # )
                    new_triangle2 = (internal_index,
                                     index_match[(index+1) % n_vert],
                                     (internal_index-1)
                                     )
                    v0 = cyl.vertex(internal_index)
                    v1 = cyl.vertex(index_match[(index+1) % n_vert])
                    v2 = cyl.vertex((internal_index-1))
                    c_n = normal_of(v0,v1,v2)
                    c_c = center_of([v0,v1,v2])
                    c_c2 = [c_c[0] + c_n[0] * long, c_c[1] + c_n[1] * long, c_c[2] + c_n[2] * long]
                    ps = Pointset(3)
                    ps.append(Point(c_c))
                    ps.append(Point(c_c2))
                    normals.append(ps)
                    # print "N O R M A L t 2", c_n
                else:
                    internal_index = index
                    new_triangle1 = (index_match[index],
                                     index_match[(index+1) % n_vert],
                                     (internal_index+1))

                    v0 = cyl.vertex(index_match[index])
                    v1 = cyl.vertex(index_match[(index+1) % n_vert])
                    v2 = cyl.vertex((internal_index+1))
                    c_n = normal_of(v0,v1,v2)
                    c_c = center_of([v0,v1,v2])

                    c_c2 = [c_c[0] + c_n[0] * long, c_c[1] + c_n[1] * long, c_c[2] + c_n[2] * long]
                    ps = Pointset(3)
                    ps.append(Point(c_c))
                    ps.append(Point(c_c2))
                    normals.append(ps)
                    # new_triangle2 = (index_match[index], (internal_index+1),
                                     # internal_index)
                    # new_triangle1 = ((internal_index+1),
                                     # index_match[(index+1) % n_vert],
                                     # index_match[index]
                                     # )
                    new_triangle2 = ((internal_index+1),
                                      internal_index,
                                    index_match[index]
                                     )
                    v0 = cyl.vertex(internal_index+1)
                    v1 = cyl.vertex((internal_index))
                    v2 = cyl.vertex(index_match[index])
                    c_n = normal_of(v0,v1,v2)
                    c_c = center_of([v0,v1,v2])
                    c_c2 = [c_c[0] + c_n[0] * long, c_c[1] + c_n[1] * long, c_c[2] + c_n[2] * long]
                    ps = Pointset(3)
                    ps.append(Point(c_c))
                    ps.append(Point(c_c2))
                    normals.append(ps)
                cyl.add_triangle(new_triangle1)
                cyl.add_triangle(new_triangle2)
                prev_z = cur_v[2]
        cyl.flip_connection_face(2)
        self.copy_from_cylindricalpart(cyl)
        print "self.vertices"
        print self.vertices
        print "self.triangles"
        print self.triangles

        # show([self], normals)
