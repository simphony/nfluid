import visvis as vv
from visvis import solidLine
backend = 'pyside'


def import_visvis():
    import visvis as vv
    from visvis import solidLine
    backend = 'pyside'

def show(items, normals=None):
    """Function that shows a mesh object.
    """
    import_visvis()
    for item in items:
        vv.clf()
        # convert to visvis.Mesh class
        new_normals = []
        new_vertices = []
        for k, v in item.vertices.iteritems():
            new_normals.append(item.normal(k))
            new_vertices.append(v)
        mesh = item.to_visvis_mesh()

        mesh.SetVertices(new_vertices)
        mesh.SetNormals(new_normals)
        mesh.faceColor = 'y'
        mesh.edgeShading = 'plain'
        mesh.edgeColor = (0, 0, 1)

    axes = vv.gca()
    if axes.daspectAuto is None:
        axes.daspectAuto = False
    axes.SetLimits()

    if normals is not None:
        for normal in normals:
            sl = solidLine(normal, 0.15)
            sl.faceColor = 'r'

    # Show title and enter main loop
    vv.title('Show')
    app = vv.use()
    app.Run()
