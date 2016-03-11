Nfluid
======

Nfluid simphony module for mesh generation of microchannel circuits.

.. image:: https://travis-ci.org/simphony/nfluid.svg?branch=master
   :target: https://travis-ci.org/simphony/nfluid
   :alt: Build status

Repository
----------
Nfluid is hosted on github https://github.com/simphony/nfluid

Requirements
------------
    - simphony >= 0.2.0
    - numpy >= 1.4.1

Visualization requirements
--------------------------
    - visvis
    - PySide

For mesh integrated visualization it needs visvis visualization library https://pypi.python.org/pypi/visvis/1.8
and PySide as the backend: https://pypi.python.org/pypi/PySide/1.2.4

Documentation requirements
--------------------------
    - sphinx

Also the documentation is available online at:
http://simphony-nfluid.readthedocs.org/en/latest/

Installation
------------
To install nfluid:

    python setup.py install
    
    or
    
    MakeWin nfluid

    (using the MakeWin .bat file in the SimPhoNy framework package)

    or

    make simphony-nfluid

    (using the Makefile linux file in the SimPhoNy framework package)
    
    
Structure
---------
    - doc: documentation generation package (with sphinx)
    - nfluid: main package with all the code
        - core: main subpackage containing the base clases of nfluid
        - elements: subpackage that contains all the microchannel pieces the user can build with nfluid
        - external: subpackage with some matrix and arithmetic auxiliar files and functions
        - geometry: internal subpackage responsible of generating the final triangle meshes of the assemblies built with nfluid
        - shapes: intermediate subpackage between the core and the geometry package
        - tests: subpackage containing some usage examples of nfluid using all the posible pieces
        - util: subpackage with auxiliar utilies, also containing the OpenFOAM project generator utility, called snappy_generator.py
        - visualisation: internal subpackage with the files containing the visualization utilities
        - ui: GUI package with all the PySide infraestructure

Building an assembly with nfluid
--------------------------------
Nfluid is an easy and user-friendly package for building microchannel assemblies of pieces.
First, user should import the ChannelAssembly class, as its the main class for nfluid:

    from nfluid.core.channel_assembly import ChannelAssembly, create_channel

We also import the create_channel function since it will be the starting point for generating channels of the assembly. After this we create the channel assembly object:

    my_assembly = ChannelAssembly()

After creating this, all the channels and elements will be added automatically to the assembly object. We can start building pieces:

    create_channel(CircleCoupling(R=10, L=20, PosH=Vector(0, 20, 30), Normal=Vector(0, 0, 1))).link(FlowAdapter(L=15)).link(CircleCoupling(R=45, L=125))

Using the link method of the elements we specify how the elements are connected. As we can see in the example above there is no
need to specify every parameter of each element since there are some of them that are inherited depending of which channel are they in
and their previous elements.

Once we have added all the elements we want, we tell nfluid to resolve the geometry of the channel(s) using the assembly object we created before:

    my_assembly.resolve_geometry()

If there are no error messages means the everything went well and the geometry of the channel is correct (we can also check this programatically with the my_assembly.is_resolved_geometry() method).
After this we can show info of the assembly:

    my_assembly.print_info()

and create a more detailed text file of the assembly:

    my_assembly.print_info_file('Assembly_0.txt')

and create the meshes:

    my_assembly.create_shapes()

If everything went well, we can export and show the shapes:

    my_assembly.export_shapes('my_assembly.stl')
    my_assembly.create_openfoam_snappy_project()
    my_assembly.create_openfoam_cfmesh_project()
    my_assembly.show_shapes()

When we are done with the shapes, we can release them:

    my_assembly.release_shapes()

We can also get the mesh in simphony format (as a Mesh object):

    mesh = my_assembly.extract_simphony_mesh()
    
Also we can modify the assembly creating new pieces and liking them, deleting existing pieces...
After modifying the assembly, we just have to clear the geometry and resolve it again:

    my_assembly.clear_geometry()
    my_assembly.resolve_geometry()
    
And then we can use the create_shapes method and any other one.

Notes
-----
The valid pieces that are now available and working are:

    - circle_coupling (CircleCoupling - simple pipe)
    - circle_tee (CircleTee - bifurcation 1 to 2)
    - flow_adapter (FlowAdapter - pipe with different head and tail radius)
    - long_elbow (LongElbowAngle and LongElbowNormals - elbow withinternal radius, specifying the angle of the normal that the tail will point to)
    - short_elbow (ShortElbowAngle and ShortElbowNormals - elbow without internal radius, specifying the angle of the normal that the tail will point to)
    - spheric_coupling (SphericCoupling - truncated sphere in both hemispheres)
    - circle_path (CirclePath - group of ordered points defining a piece from the first point to the last)

OpenFOAM project generation
---------------------------

Using templates, nfluid can generate project templates for the SnappyHexMesh and tetMesh (from cfMesh package) utilities:
http://cfd.direct/openfoam/user-guide/snappyHexMesh/
http://cfmesh.com/cfmesh/

At this moment, the generators are in nfluid.util subpackage, and the python script are called snappy_generator.py and cfmesh_generator.py
The usage is simple:

    python snappy_generator.py stl_file.stl snappy_template.txt
    python cfmesh_generator.py stl_file.stl cfmesh_template.txt

when:
    snappy_generator.py cfmesh_generator.py are the scripts
    stl_file.stl is the stl file generated by exporting using nfluid
    snappy_template.txt is the snappy hex mesh template that the script will use to generate the project structure and snappyHexMeshDict file.
    cfmesh_template.txt is the cfmesh template that the script will use to generate the project structure and meshDict file.

The templates contain some keywords that, using information of the stl, will be replaced by the correct values. As a first approach,
there are different templates in the nfluid package, but the user can potentially use their own templates, using the keywords that are used by the scripts.

Also, we can use the method in the ChannelAssembly class directly to do this:

    my_asembly.create_openfoam_snappy_project()
    my_asembly.create_openfoam_cfmesh_project()
    
to which we can indicate the stl to use (if not specified it will create a "foam.stl" for this task),
the template to use (if not specified it will use the default template of the package),
and also the cells in the three axis to generate the template (20, 20, 20 by default) - in case of snappyHexMesh.

Using the GUI
-------------

nFluid library can also be used with the GUI developed using PySide. To do this:

    from nfluid.ui.main_module import start_gui

    start_gui()

and the GUI will show up. It has all the features that the libray has, using special widgets
to make things simpler and giving the user additional tools to work with the library. Also the GUI can be opened and closed anytime, working in both python shell
and GUI with the same assembly.

