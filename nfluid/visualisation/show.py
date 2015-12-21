import visvis as vv
from visvis.processing.calculateNormals import calculateNormals
# from PySide import QtGui, QtCore
backend = 'pyside'

from nfluid.geometry.geometricmesh import GeometricMesh


def show(items):
    """Function that shows a mesh object.
    """
    meshes = []
    for item in items:
        # convert to visvis.Mesh class
        item.compute_normals()
        mesh = item.to_visvis_mesh()
        mesh.SetNormals(item.normals.values())
        meshes.append(mesh)
        

    axes = vv.gca()
    if axes.daspectAuto is None:
        axes.daspectAuto = False
    axes.SetLimits()
        
    # Show title and enter main loop
    vv.title('Show')
    app = vv.use()
    app.Run()