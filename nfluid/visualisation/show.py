import visvis as vv
# from PySide import QtGui, QtCore
backend = 'pyside'

from nfluid.geometry.geometricmesh import GeometricMesh

def show(items):
    """Function that shows a mesh object.
    """
    meshes = []
    for item in items:
        # convert to visvis.Mesh class
        meshes.append(item.to_visvis_mesh())

    axes = vv.gca()
    if axes.daspectAuto is None:
        axes.daspectAuto = False
    axes.SetLimits()
        
    # Show title and enter main loop
    vv.title('Show test')
    app = vv.use()
    app.Run()