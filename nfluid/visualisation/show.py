import visvis as vv
backend = 'pyside'


def show(items):
    """Function that shows a mesh object.
    """
    # meshes = []
    for item in items:
        # convert to visvis.Mesh class
        # item.compute_normals()
        new_normals = []
        new_vertices = []
        for k, v in item.vertices.iteritems():
            new_normals.append(item.normal(k))
            new_vertices.append(v)
        mesh = item.to_visvis_mesh()

        mesh.SetVertices(new_vertices)
        mesh.SetNormals(new_normals)
        # im = vv.imread("C:\Users\GregorioGarcia\Pictures\Icons\DeleteIcon.png")
        # mesh.SetTexture(im)
        mesh.faceColor = 'y'
        # mesh.faceShading = 'flat'
        mesh.edgeShading = 'plain'
        mesh.edgeColor = (0,0,1)
        # mesh.SetNormals(item.normals.values())
        # meshes.append(mesh)

    axes = vv.gca()
    if axes.daspectAuto is None:
        axes.daspectAuto = False
    axes.SetLimits()

    # Show title and enter main loop
    vv.title('Show')
    app = vv.use()
    app.Run()
