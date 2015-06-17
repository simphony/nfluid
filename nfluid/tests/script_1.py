import visvis as vv
# from visvis import OrientableMesh, Point, Pointset
from nfluid.geometry.geometricmesh import GeometricMesh
from nfluid.visualisation.show import show
from nfluid.geometry.generator import GeometryGenerator
from nfluid.external.transformations import vector_product
from nfluid.geometry.functions import normal_of, center_of

# m = GeometricMesh()
# i1 = m.add_vertex((1,0,0))
# i2 = m.add_vertex((0,1,0))
# i3 = m.add_vertex((0,0,1))
# p = Pointset(3)
# point = m.vertex(i1)
# p.append(point)
# point = m.vertex(i2)
# p.append(point)
# point = m.vertex(i3)
# p.append(point)

# vm = OrientableMesh(parent=vv.gca(), vertices=p)
# vm.SetValues([(1,0,0),(0,1,0),(0,0,1)])
# vm.SetFaces([(i1,i2,i3)])
# vm.SetNormals([(1,0,0),(0,1,0),(0,0,1)])


# sphere = vv.solidSphere((3,0,0))
# vv.plot(vm)

gg = GeometryGenerator(slices=8, stacks=3)
# m = gg.create_random_mesh(10)
# vm = m.to_visvis_mesh()

# show(m)

# c = gg.generate_circle_3d(1,5, filled=True)

# show(c)




# # figure = gg.create_random_mesh(100)
# # figure = gg.create_coupling(1, 12)
# # figure = gg.create_zigzag(3, 120, zigzags=8)
# # figure = gg.create_cap(3,0)
# # figure = gg.create_flow_adapter(10,5,15)
# # figure = gg.create_curve_zigzag(5,120, 2)
# # figure = gg.create_lamp(5,20)
# figure = gg.create_spheric_coupling(110,300)
# # figure = gg.create_short_elbow(5,angle=48)
# # figure = gg.create_long_elbow(1,3,angle=60)

# show([figure])

# # print figure.triangles
# # print figure.vertices

# # p1 = (0,0,0)
# # p2 = (1,0,-1)
# # p3 = (0,1,0)

# # print normal_of(p1,p2,p3)
# # print center_of([p1,p2,p3])

# -------------------------------------------------------------

# f1 = gg.create_coupling(1, 15)
# # f2 = gg.create_flow_adapter(1,5,15)
# # f1.attach(f2)

# show([f1])
# # show([f2])
# # show([f1,f2])

# -------------------------------------------------------------

f1 = gg.create_coupling(1, 12)
f2 = gg.create_flow_adapter(1,5,15)
f3 = gg.create_flow_adapter(5,10,15)
# f3 = gg.create_spheric_coupling(1,300)
f4 = gg.create_short_elbow(10,angle=45)
# f5 = gg.create_coupling(10, 12)
f5 = gg.create_flow_adapter(10,3, 12)
f6 = gg.create_short_elbow(3,angle=45)
f7 = gg.create_long_elbow(10,3,angle=60)
f8 = gg.create_flow_adapter(3,1,15)
f9 = gg.create_long_elbow(30,1,angle=30)
f10 = gg.create_spheric_coupling(1, 7.5)
f11 = gg.create_coupling(1, 7)
# f11 = gg.create_spheric_coupling(1, 7.5)
# f11 = gg.create_coupling(10, 70)
# f7 = gg.create_short_elbow(1,angle=45)
# print type(f4)
# print f4.connection_faces
# f5 = gg.create_long_elbow(10,10,angle=60)

# f1.attach(f6)
# f6.attach(f7)
figures = [f1]
c_f = f1.attach(f2)
figures.append(c_f)
c_f = f2.attach(f3)
figures.append(c_f)
c_f = f3.attach(f4)
figures.append(c_f)
c_f = f4.attach(f5)
figures.append(c_f)
c_f = f5.attach(f6)
figures.append(c_f)
c_f = f6.attach(f7)
figures.append(c_f)
c_f = f7.attach(f8)
figures.append(c_f)
c_f = f8.attach(f9)
figures.append(c_f)
c_f = f9.attach(f10)
figures.append(c_f)
c_f = f10.attach(f11)
figures.append(c_f)
# print f4.connection_faces
total = None
for f in figures:
    if total == None:
         total = f
    else:
        total = total.connect(f)
# bbb
# total = figures[0].connect(figures[1]).connect(figures[2])
# show([f1,f6,f7])
# show([f6,f7])
show([total])
total.export("Assembly_test_0.stl")

# show([f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11])
# show([f1,f2,f3,f4,f5,f6,f7,f8,f9,f10])
# show([f1,f2,f3])

# ---------------------------------------------------------------

# f1 = gg.create_short_elbow(1,angle=90)
# f2 = gg.create_short_elbow(1,angle=45)

# f1.attach(f2)

# # show([f1.connect(f2)])
# show([f1,f2])

# ---------------------------------------------------------------

# # test = gg.create_coupling_path(0.5, [(0,0,0), (0,5,0), (2,8,8)])
# # test = gg.create_coupling_path(1, [(1,3,7), (1,6,1), (1,8,6)])
# # test = gg.create_coupling_path(1, [(0,-5,0), (0,0,0), (0,0,5)])
# # test = gg.create_coupling_path(1, [(0,0,0), (0,4,0), (0,6,3)])
# # test = gg.create_coupling_path(1, [(0,0,0), (0,4,0), (0,4.5,3)])
# # test = gg.create_coupling_path(1, [(0,0,0), (0,4,0), (0,3,3)])
# # test = gg.create_coupling_path(1, [(0,0,0), (0,4,0), (0,3,3), (0,3,7), (0,8,9), (0,8,0)])
# # yz plane
# # heart = [(0,0,0),(0,-3,3),(0,-6,6),(0,-9,9),(0,-9,12),(0,-6,15),(0,-3,15),(0,-3,12),
         # # (0,0,9),
         # # (0,3,12),(0,3,15),(0,6,15),(0,9,12),(0,9,9),(0,6,6),(0,3,3),(0,0,0)]#,(0,3,3)]
# # xy plane
# heart = [(0,0,0),(3,-3,0),(6,-6,0),(9,-9,0),(12,-9,0),(15,-6,0),(15,-3,0),(12,-3,0),
         # (9,0,0),
         # (12,3,0),(15,3,0),(15,6,0),(12,9,0),(9,9,0),(6,6,0),(3,3,0),(0,0,0)]#,(0,3,3)]
# # inclined
# # heart = [(0,0,0),(1.5,-3,3),(3,-6,6),(4.5,-9,9),(6,-9,12),(7.5,-6,15),(7.5,-3,15),(6,-3,12),
         # # (4.5,0,9),
         # # (6,3,12),(7.5,3,15),(7.5,6,15),(6,9,12),(4.5,9,9),(3,6,6),(1.5,3,3),(0,0,0)]#,(0,3,3)]
         
# # heart = [(12,-9,0),(15,-6,0),(15,-3,0)
         # # ]#,(0,3,3)]
         
# test = gg.create_coupling_path(1, heart)

# show([test])


# # wheel1_points = [(0,0,0),(0,6,0),(6,6,0),(6,0,0),(0,0,0)]
# # wheel2_points = [(21,0,0),(21,6,0),(27,6,0),(27,0,0),(21,0,0)]
# # body1_points = [(0,3,0),(-3,3,0),(-6,3,0),(-9,3,0),(-12,3,0),(-12,6,0),(-9,6,0),(-6,9,0),(-3,12,0),
               # # (0,12,0),(24,12,0),(24,9,0),(27,9,0),(27,6,0),(30,6,0),(30,3,0),(27,3,0)]
# # body2_points = [(6,3,0),(21,3,0)]
# # wheel1 = gg.create_coupling_path(0.1, wheel1_points)
# # wheel2 = gg.create_coupling_path(0.1, wheel2_points)
# # body1 = gg.create_coupling_path(0.1, body1_points)
# # body2 = gg.create_coupling_path(0.1, body2_points)

# # show([wheel1,wheel2,body1,body2])



# test.export("Assembly_test_1.stl")

# ---------------------------------------------------------------

# test = gg.create_coupling(1,5)
# show([test])
# test.export("Assembly_test_1.stl")