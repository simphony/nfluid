import unittest
import os
import shutil

from nfluid.core.channel_assembly import ChannelAssembly
from nfluid.core.channel_element import ChannelElement
from nfluid.core.gate_base import Gate
from nfluid.elements.cap import Cap
from nfluid.elements.circle_coupling import CircleCoupling
from nfluid.elements.circle_path import CirclePath
from nfluid.elements.circle_tee import CircleTee
from nfluid.elements.flow_adapter import FlowAdapter
from nfluid.elements.long_elbow_angle import LongElbowAngle
from nfluid.elements.long_elbow_normals import LongElbowNormals
from nfluid.elements.short_elbow_angle import ShortElbowAngle
from nfluid.elements.short_elbow_normals import ShortElbowNormals
from nfluid.elements.spheric_coupling import SphericCoupling
from nfluid.shapes.shapes import Shape
from nfluid.util.vector import Vector
from nfluid.geometry.geometricmesh import GeometricMesh, CylindricalPart
import nfluid.geometry.cap as geo_cap
import nfluid.geometry.coupling as geo_coupling
import nfluid.geometry.coupling_path as geo_coupling_path
import nfluid.geometry.flow_adapter as geo_flow_adapter
import nfluid.geometry.long_elbow as geo_long_elbow
import nfluid.geometry.short_elbow as geo_short_elbow
import nfluid.geometry.spheric_coupling as geo_spheric_coupling
import nfluid.geometry.tee as geo_tee
from simphony.cuds.mesh import ABCMesh
from visvis import OrientableMesh


def compare_two_vectors(first, second, testcase=None):
    self = testcase
    self.assertTrue(first.x == second.x)
    self.assertTrue(first.y == second.y)
    self.assertTrue(first.z == second.z)


def compare_two_gates(first, second, testcase=None):
    self = testcase
    self.assertTrue(first.x == second.x)
    self.assertTrue(first.y == second.y)
    self.assertTrue(first.z == second.z)
    self.assertEqual(first.Pos, second.Pos)
    self.assertEqual(first.Normal, second.Normal)


def compare_two_elements(first, second, testcase=None):
    self = testcase
    self.assertTrue(first.get_id() == second.get_id())
    self.assertTrue(first.name() == second.name())
    self.assertListEqual(first.heads, second.heads)
    self.assertListEqual(first.tails, second.tails)


def compare_two_meshes(first, second, testcase=None):
    pass


class TestNfluidAddGet(unittest.TestCase):

    def setUp(self):
        self.assembly = ChannelAssembly()
        self.addTypeEqualityFunc(ChannelElement, compare_two_elements)
        self.addTypeEqualityFunc(Gate, compare_two_gates)
        self.addTypeEqualityFunc(Vector, compare_two_vectors)

    def test_add_element(self):
        CircleCoupling(R=10, L=75, PosH=Vector(0, 0, 0),
                       Normal=Vector(0, 0, 1))
        n_elems = len(self.assembly.elements)
        self.assertTrue(n_elems == 1,
                        msg='Element not added, size == {}'.format(n_elems))

    def test_get_element_by_id(self):
        circle_coupling = CircleCoupling(R=10, L=75, PosH=Vector(0, 0, 0),
                                         Normal=Vector(0, 0, 1))
        id = circle_coupling.get_id()
        added_elem = self.assembly.get_element_by_id(id)
        self.assertEqual(circle_coupling, added_elem)


class TestNFluidAssembly(unittest.TestCase):

    def setUp(self):
        self.assembly = ChannelAssembly()
        self.addTypeEqualityFunc(ChannelElement, compare_two_elements)
        self.addTypeEqualityFunc(Gate, compare_two_gates)
        self.addTypeEqualityFunc(Vector, compare_two_vectors)
        self.circle_coupling1 = CircleCoupling(R=10, L=75,
                                               PosH=Vector(0, 0, 0),
                                               Normal=Vector(0, 0, 1))
        self.circle_coupling2 = CircleCoupling(L=15)
        self.circle_coupling1.link(self.circle_coupling2)

    def test_resolve_geometry(self):
        ret = self.assembly.resolve_geometry()
        self.assertTrue(ret == '')
        self.assertTrue(self.assembly.is_resolved_geometry() == '')
        n_elems = len(self.assembly.elements)
        self.assertTrue(n_elems == 2,
                        msg='Element not added, size == {}'.format(n_elems))

    def test_clear_geometry(self):
        self.assembly.resolve_geometry()
        self.assembly.clear_geometry()
        id = self.circle_coupling1.get_id()
        added = self.assembly.get_element_by_id(id)
        self.assertTrue(added.changed)
        self.assertEqual(self.circle_coupling1, added)

    def test_slices(self):
        n_slices = 10
        self.assembly.set_slices(n_slices)
        self.assertTrue(n_slices, self.assembly.slices())

    def test_stacks(self):
        n_stacks = 4
        self.assembly.set_stacks(n_stacks)
        self.assertTrue(n_stacks, self.assembly.stacks())

    def test_create_shapes(self):
        self.assembly.resolve_geometry()
        ret = self.assembly.create_shapes()
        self.assertTrue(ret == '')
        self.assertIsNotNone(Shape.total_mesh)

    def test_release_shapes(self):
        self.assembly.resolve_geometry()
        self.assembly.create_shapes()
        self.assembly.release_shapes()
        self.assertIsNone(Shape.total_mesh)
        id = self.circle_coupling1.get_id()
        elem = self.assembly.get_element_by_id(id)
        self.assertIsNone(elem.shape)

    def test_export_shapes(self):
        self.assembly.resolve_geometry()
        self.assembly.create_shapes()
        stl_name = './test_export_shapes.stl'
        self.assembly.export_shapes(stl_name)
        self.assertTrue(os.path.exists(stl_name))
        os.remove(stl_name)

    def test_create_openfoam_snappy_project(self):
        self.assembly.resolve_geometry()
        self.assembly.create_shapes()
        stl_name = './test_export_shapes.stl'
        snappy_name = './SNAPPY_PROJECT'
        self.assembly.export_shapes(stl_name)
        self.assembly.create_openfoam_snappy_project(stl_name)
        self.assertTrue(os.path.exists(snappy_name))
        shutil.rmtree(snappy_name)

    def test_create_openfoam_cfmesh_project(self):
        self.assembly.resolve_geometry()
        self.assembly.create_shapes()
        stl_name = './test_export_shapes.stl'
        cfmesh_name = './CFMESH_PROJECT'
        self.assembly.export_shapes(stl_name)
        self.assembly.create_openfoam_cfmesh_project(stl_name)
        self.assertTrue(os.path.exists(cfmesh_name))
        shutil.rmtree(cfmesh_name)

    def test_extract_simphony_mesh(self):
        self.assembly.resolve_geometry()
        self.assembly.create_shapes()
        mesh = self.assembly.extract_simphony_mesh()
        self.assertIsInstance(mesh, ABCMesh)

    def test_delete_element(self):
        id = self.circle_coupling1.get_id()
        self.assembly.delete_element(self.circle_coupling1)
        elem = self.assembly.get_element_by_id(id)
        self.assertIsNone(elem)

    def test_insert_element_before(self):
        circle_coupling3 = CircleCoupling(L=5)
        self.assembly.insert_element_before(circle_coupling3,
                                            self.circle_coupling2)
        ids = [self.circle_coupling1.get_id(),
               circle_coupling3.get_id(),
               self.circle_coupling2.get_id()]
        current_ids = []
        for elem in self.assembly.elements:
            current_ids.append(elem.get_id())
        self.assertListEqual(ids, current_ids)

    def test_print_info_file(self):
        self.assembly.resolve_geometry()
        self.assembly.create_shapes()
        filename = 'test_output_info.txt'
        self.assembly.print_info_file(filename)
        self.assertTrue(os.path.exists(filename))
        os.remove(filename)

    def test_get_tree_structure(self):
        self.assembly.resolve_geometry()
        self.assembly.create_shapes()
        tree = self.assembly.get_tree_structure()
        self.assertIsNotNone(tree)
        n_nodes = tree.n_nodes()
        self.assertTrue(len(self.assembly.elements) == n_nodes)


class TestNfluidElement(unittest.TestCase):

    def setUp(self):
        self.assembly = ChannelAssembly()
        self.addTypeEqualityFunc(ChannelElement, compare_two_elements)
        self.addTypeEqualityFunc(Gate, compare_two_gates)
        self.addTypeEqualityFunc(Vector, compare_two_vectors)
        self.elem = None

    def test_get_id(self):
        if self.elem is not None:
            id = self.elem.get_id()
            self.assertIsNotNone(id)

    def test_get_name(self):
        if self.elem is not None:
            name = self.elem.get_name()
            self.assertIsNotNone(name)

    def test_create_shape_child(self):
        if self.elem is not None:
            shape = self.elem.create_shape_child()
            self.assertIsNotNone(shape)

    def test_volume(self):
        if self.elem is not None:
            self.elem.calculate_volume()
            volume = self.elem.get_volume()
            self.assertIsNotNone(volume)


class TestNfluidElementFlowAdapter(TestNfluidElement):

    def setUp(self):
        super(TestNfluidElementFlowAdapter, self).setUp()
        self.elem = FlowAdapter(RH=5, RT=10, L=15, PosH=Vector(0, 0, 0),
                                Normal=Vector(0, 0, 1))
        self.assembly.resolve_geometry()


class TestNfluidElementCircleTee(TestNfluidElement):

    def setUp(self):
        super(TestNfluidElementCircleTee, self).setUp()
        self.elem = CircleTee(R=5, PosH=Vector(0, 0, 0),
                              NormalH=Vector(0, 0, 1),
                              NormalT0=Vector(1, 0, 0))
        self.assembly.resolve_geometry()


class TestNfluidElementCirclePath(TestNfluidElement):

    def setUp(self):
        super(TestNfluidElementCirclePath, self).setUp()
        points = [Vector(0, 0, 0), Vector(0, 0, 50),
                  Vector(50, 0, 50), Vector(50, 0, 100),
                  Vector(100, 0, 100)]
        self.elem = CirclePath(R=5, Points=points, PosH=Vector(0, 0, 0),
                               NormalH=Vector(0, 0, 1),
                               NormalT=Vector(1, 0, 0))
        self.assembly.resolve_geometry()


class TestNfluidElementCircleCoupling(TestNfluidElement):

    def setUp(self):
        super(TestNfluidElementCircleCoupling, self).setUp()
        self.elem = CircleCoupling(R=5, L=15, PosH=Vector(0, 0, 0),
                                   Normal=Vector(0, 0, 1))
        self.assembly.resolve_geometry()


class TestNfluidElementCap(TestNfluidElement):

    def setUp(self):
        super(TestNfluidElementCap, self).setUp()
        self.elem = Cap(R=20, L=15, PosH=Vector(0, 0, 0),
                        NormalH=Vector(0, 0, 1))
        self.assembly.resolve_geometry()


class TestNfluidElementSphericCoupling(TestNfluidElement):

    def setUp(self):
        super(TestNfluidElementSphericCoupling, self).setUp()
        self.elem = SphericCoupling(RS=15, R=5, PosH=Vector(0, 0, 0),
                                    Normal=Vector(0, 0, 1))
        self.assembly.resolve_geometry()


class TestNfluidElementShortElbowNormals(TestNfluidElement):

    def setUp(self):
        super(TestNfluidElementShortElbowNormals, self).setUp()
        self.elem = ShortElbowNormals(R=5, PosH=Vector(0, 0, 0),
                                      NormalH=Vector(0, 0, 1),
                                      NormalT=Vector(1, 0, 0))
        self.assembly.resolve_geometry()


class TestNfluidElementShortElbowAngle(TestNfluidElement):

    def setUp(self):
        super(TestNfluidElementShortElbowAngle, self).setUp()
        self.elem = ShortElbowAngle(R=5, PosH=Vector(0, 0, 0),
                                    NormalH=Vector(0, 0, 1),
                                    NormalT=Vector(1, 0, 0))
        self.assembly.resolve_geometry()


class TestNfluidElementLongElbowNormals(TestNfluidElement):

    def setUp(self):
        super(TestNfluidElementLongElbowNormals, self).setUp()
        self.elem = LongElbowNormals(RC=3, R=5, PosH=Vector(0, 0, 0),
                                     NormalH=Vector(0, 0, 1),
                                     NormalT=Vector(1, 0, 0))
        self.assembly.resolve_geometry()


class TestNfluidElementLongElbowAngle(TestNfluidElement):

    def setUp(self):
        super(TestNfluidElementLongElbowAngle, self).setUp()
        self.elem = LongElbowAngle(RC=3, R=5, PosH=Vector(0, 0, 0),
                                   NormalH=Vector(0, 0, 1),
                                   NormalT=Vector(1, 0, 0))
        self.assembly.resolve_geometry()


class TestNfluidGeometricMeshCommon(unittest.TestCase):

    def setUp(self):
        self.addTypeEqualityFunc(GeometricMesh, compare_two_meshes)
        self.mesh = GeometricMesh()

    def test_vertex(self):
        v0 = (1, 3, 9)
        v1 = (4, 2, 10)
        index0 = self.mesh.add_vertex(v0)
        index1 = self.mesh.add_vertex(v1)
        added0 = self.mesh.vertex(index0)
        added1 = self.mesh.vertex(index1)
        n_vertices = self.mesh.n_vertices()
        self.assertTrue(n_vertices == 2)
        self.assertEqual(added0, v0)
        self.assertEqual(added1, v1)
        v1 = (10, 2, 4)
        self.mesh.update_vertex(index1, v1)
        updated1 = self.mesh.vertex(index1)
        self.assertEqual(updated1, v1)
        self.mesh.remove_vertex(index0)
        with self.assertRaises(Exception):
            self.mesh.vertex(index0)

    def test_normal(self):
        v0 = (1, 3, 9)
        v1 = (4, 2, 10)
        n0 = (1, 1, 1)
        n1 = (0.5, 0.3, 0.1)
        index0 = self.mesh.add_vertex(v0)
        index1 = self.mesh.add_vertex(v1)
        self.mesh.add_normal(index0, n0)
        self.mesh.add_normal(index1, n1)
        added0 = self.mesh.normal(index0)
        added1 = self.mesh.normal(index1)
        n_normals = self.mesh.n_normals()
        self.assertTrue(n_normals == 2)
        self.assertEqual(added0, n0)
        self.assertEqual(added1, n1)
        n1 = (0.1, 0.3, 0.5)
        self.mesh.update_normal(index1, n1)
        updated1 = self.mesh.normal(index1)
        self.assertEqual(updated1, n1)
        self.mesh.remove_normal(index0)
        with self.assertRaises(Exception):
            self.mesh.normal(index0)

    def test_triangle(self):
        v0 = (1, 3, 9)
        v1 = (4, 2, 10)
        v2 = (7, 8, 11)
        index0 = self.mesh.add_vertex(v0)
        index1 = self.mesh.add_vertex(v1)
        index2 = self.mesh.add_vertex(v2)
        t0 = (index0, index1, index2)
        t1 = (index1, index2, index0)
        index_t0 = self.mesh.add_triangle(t0)
        index_t1 = self.mesh.add_triangle(t1)
        added0 = self.mesh.triangle(index0)
        added1 = self.mesh.triangle(index1)
        n_triangles = self.mesh.n_triangles()
        self.assertTrue(n_triangles == 2)
        self.assertEqual(added0, t0)
        self.assertEqual(added1, t1)
        t1 = (index2, index0, index1)
        self.mesh.update_triangle(index_t1, t1)
        updated1 = self.mesh.triangle(index1)
        self.assertEqual(updated1, t1)
        self.mesh.remove_triangle(index0)
        with self.assertRaises(Exception):
            self.mesh.triangle(index_t0)


class TestNfluidGeometry(unittest.TestCase):

    def setUp(self):
        self.addTypeEqualityFunc(GeometricMesh, compare_two_meshes)
        self.slices = 3
        self.stacks = 10
        self.r = 1
        self.mesh = None
        # self.example = geo_coupling.Coupling(self.r, self.r,
        #                                      self.slices, self.stacks)
        self.example = CylindricalPart()
        i0 = self.example.add_vertex((0, 0, self.r))
        i1 = self.example.add_vertex((self.r, 0, self.r))
        i2 = self.example.add_vertex((0, self.r, self.r))
        n = (0, 0, 1)
        self.example.add_triangle((i0, i1, i2))
        self.example.add_normal(i0, n)
        self.example.add_normal(i1, n)
        self.example.add_normal(i2, n)
        self.example.add_connection_face((i0, i1, i2))
        self.example.add_connection_face((i0, i1, i2))

    def test_vis_vis_mesh(self):
        if self.mesh is not None:
            res = self.mesh.to_visvis_mesh()
            self.assertIsInstance(res, OrientableMesh)

    def test_simphony_mesh(self):
        if self.mesh is not None:
            res = self.mesh.to_simphony_mesh()
            self.assertIsInstance(res, ABCMesh)

    def test_export(self):
        if self.mesh is not None:
            filename = './test_export.stl'
            self.mesh.export(filename)
            self.assertTrue(os.path.exists(filename))
            os.remove(filename)

    def test_move(self):
        if self.mesh is not None:
            p = (0, 0, 0)
            n = (1, 0, 0)
            self.mesh.move(p, n)

    def test_attach(self):
        if self.mesh is not None:
            res = self.example.attach(self.mesh)
            self.assertIsNotNone(res)

    def test_adapt(self):
        if self.mesh is not None:
            res = self.example.attach(self.mesh)
            res = self.example.adapt(res)
            self.assertIsNotNone(res)

    def test_connect(self):
        if self.mesh is not None:
            res = self.example.attach(self.mesh)
            res = self.example.adapt(res)
            res = self.example.connect(res)
            self.assertIsNotNone(res)

    def test_link(self):
        if self.mesh is not None:
            res = self.example.link(self.mesh)
            self.assertIsNotNone(res)

    def test_twist(self):
        if self.mesh is not None:
            self.mesh.twist(90)

    def test_compute_normals(self):
        if self.mesh is not None:
            n_normals_before = self.mesh.n_normals()
            self.mesh.compute_normals()
            n_normals_after = self.mesh.n_normals()
            self.assertTrue(n_normals_before == n_normals_after)


class TestNfluidGeometricMeshCap(TestNfluidGeometry):

    def setUp(self):
        super(TestNfluidGeometricMeshCap, self).setUp()
        self.mesh = geo_cap.Cap(self.r, 5, self.slices, self.stacks)


class TestNfluidGeometricMeshCoupling(TestNfluidGeometry):

    def setUp(self):
        super(TestNfluidGeometricMeshCoupling, self).setUp()
        self.mesh = geo_coupling.Coupling(self.r, 5, self.slices, self.stacks)


class TestNfluidGeometricMeshCouplingPath(TestNfluidGeometry):

    def setUp(self):
        super(TestNfluidGeometricMeshCouplingPath, self).setUp()
        points = [(0, 0, 0), (0, 0, self.r), (0, self.r, self.r*2)]
        self.mesh = geo_coupling_path.CouplingPath(self.r, points,
                                                   self.slices, self.stacks)


class TestNfluidGeometricMeshFlowAdapter(TestNfluidGeometry):

    def setUp(self):
        super(TestNfluidGeometricMeshFlowAdapter, self).setUp()
        self.mesh = geo_flow_adapter.FlowAdapter(self.r, self.r*2, self.r,
                                                 self.slices, self.stacks)


class TestNfluidGeometricMeshLongElbow(TestNfluidGeometry):

    def setUp(self):
        super(TestNfluidGeometricMeshLongElbow, self).setUp()
        self.mesh = geo_long_elbow.LongElbow(self.r, self.r/2.0,
                                             self.slices, self.stacks)


class TestNfluidGeometricMeshShortElbow(TestNfluidGeometry):

    def setUp(self):
        super(TestNfluidGeometricMeshShortElbow, self).setUp()
        self.mesh = geo_short_elbow.ShortElbow(self.r, self.slices,
                                               self.stacks)


class TestNfluidGeometricMeshSphericCoupling(TestNfluidGeometry):

    def setUp(self):
        super(TestNfluidGeometricMeshSphericCoupling, self).setUp()
        self.mesh = geo_spheric_coupling.SphericCoupling(self.r, self.r*2,
                                                         self.slices,
                                                         self.stacks)


class TestNfluidGeometricMeshTee(TestNfluidGeometry):

    def setUp(self):
        super(TestNfluidGeometricMeshTee, self).setUp()
        self.mesh = geo_tee.Tee(self.r, self.slices, self.stacks)
