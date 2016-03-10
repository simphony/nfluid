#!/usr/bin/python
# -*- coding: utf-8 -*-
from nfluid.core.channel_info import ChannelInfoParser
from nfluid.core.channel_info import ChannelInfo
from nfluid.core.channel_element import ChannelElement
from nfluid.core.channel_element_2g import ChannelElement2G
from nfluid.shapes.shapes import Shape
from nfluid.util import snappy_generator
from nfluid.util import cfmesh_generator
from nfluid.util.tree import TreeBase, TreeNode


class ChannelAssembly(object):
    """Main class representing a group of linked pieces, forming
    a full triangular mesh.

    Attributes
    ----------
    gates_sides : int
        number of vertical slices of all the pieces in the assembly
    elements_divisions : int
        number of horizontal stacks of the pieces
    elements : list of ChannelElement
        All the elements of the assembly
    info_extractor : ChannelInfoParser
        Object that does all the txt output processing

    """

    def __init__(self, gates_sides=14, elements_divisions=7):
        """Constructor of the Assembly.

        Parameters
        ----------
        gates_sides : int
        number of vertical slices of all the pieces in the assembly
        elements_divisions : int
        number of horizontal stacks of the pieces

        """
        self.elements = []
        ChannelElement.assembly = self
        ChannelElement.slices = gates_sides
        ChannelElement.stacks = elements_divisions
        self.gates_sides = gates_sides
        self.elements_divisions = elements_divisions
        self.info_extractor = ChannelInfoParser(ChannelInfo(self))

    def add_element(self, element):
        """Adds a new element to the Assembly.

        Parameters
        ----------
        element : ChannelElement
            the element to be added to the assembly

        """
        self.elements.append(element)

    def get_element_by_id(self, id):
        """Returns the element of the assembly with the given id.

        Parameters
        ----------
        id : int
            id of the piece

        Returns
        -------
        The requested piece or None

        """
        for element in self.elements:
            if element.get_id() == id:
                return element
        return None

    def for_each_element(self, fcn):
        for element in self.elements:
            fcn(element)

    def resolve_geometry(self):
        """Main method that loops over all the elements, analyzing if their
        geometric parameters are compatible and if the assembly is correct or
        not.

        Returns
        -------
        If the geometry is ok it will return ''. An error message otherwise.

        See also
        --------
        is_resolved_geometry

        """
        while True:
            print 'resolve_geometry loop ---------------------------'
            Changed = False
            for element in self.elements:
                if element.changed:
                    print 'resolve_geometry before --------'
                    element.print_info()
                    res = element.resolve_geometry()
                    print 'assembly.resolve_geometry res = ', res
                    if res != '':
                        if res == 'ok':
                            Changed = True
                        else:
                            return 'ERROR in' + element.get_chain_str() \
                                + ':' + res
                    print 'resolve_geometry after --------'
                    element.print_info()
                    element.changed = False
            print 'Changed', Changed
            if not Changed:
                break
        return self.is_resolved_geometry()

    def is_resolved_geometry(self):
        """Method that checks if the geometry was well resolved or not.

        Returns
        -------
        If the geometry is ok it will return ''. An error message otherwise.

        See also
        --------
        is_resolved_geometry

        """

        for element in self.elements:
            res = element.is_resolved_geometry()
            if res != '':
                return 'Geometry not resolved in' \
                    + element.get_chain_str() + ':' + res
        return ''

    def clear_geometry(self):
        """Iterates over all the elements, removing all the geometric linkage
        parameters between them, so the geometry of the assembly must be
        resolved again.

        """
        for element in self.elements:
            element.clear_geometry()
            print 'clear_geometry Assembly loop ---------------------------'

    def print_info(self):
        for element in self.elements:
            print 'New Assembly Element --------------------------- ' \
                + element.get_name()
            element.print_info()
            res = element.is_resolved_geometry()
            if res != '':
                print '-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-'
                print 'GEOMETRY NOT RESOLVED: ', res
                print '-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-'

    def create_shapes(self):
        """Builds all the triangular meshes of the elements in the assembly,
        making the linkage between them, creating the full mesh of it.

        """
        Shape.init(self.gates_sides, self.elements_divisions)

        for element in self.elements:
            res = element.create_shape()
            if res != '':
                return res
            Shape.add_shape(element.shape)

        return Shape.finalize()

    def release_shapes(self):
        """Reset the current triangular mesh of the assembly and elements.

        """
        for element in self.elements:
            element.release_shape()
        Shape.release()

    def export_shapes(self, file_name, close=False):
        """Creates the correspondent .stl file of the triangular mesh
        of the current assembly.

        Parameters
        ----------
        file_name : string
            name of the stl file to be exported to.

        close : bool
            Indicates if the mesh should be closed in all its gates
            before exporting to .stl or if should be exported as it is.

        Returns
        -------
        Returns '' indicating everything was ok.

        """
        # close == True --> we close the stl surface
        Shape.export(file_name, close)
        return ''

    def create_openfoam_snappy_project(self, stl=None, template=None):
        """Creates a folder with the snappyHexMesh structure using the current
        assembly.

        Parameters
        ----------
        stl : string
            Name of the stl to be used. This method could potencially works
            with any stl (not the one generated by the current assembly), but
            as the file containing the algorithm can be used a standalone
            script this is not implemented right now. This is also true
            for the create_openfoam_cfmesh_project method.

        template : string
            The template that will be used for the parameters dictionary of
            the project. If None is specified it will be use the nFluid
            default template.

        See Also
        --------
        create_openfoam_cfmesh_project
        """
        self.export_shapes('foam.stl', close=True)
        snappy_generator.generate_snappy_project('foam.stl',
                                                 template)

    def create_openfoam_cfmesh_project(self, stl=None, template=None):
        """Creates a folder with the cfmesh (tetMesh) structure using the
        current assembly.

        Parameters
        ----------
        stl : string
            Name of the stl to be used. This method could potencially works
            with any stl (not the one generated by the current assembly), but
            as the file containing the algorithm can be used a standalone
            script this is not implemented right now. This is also true
            for the create_openfoam_snappy_project method.

        template : string
            The template that will be used for the parameters dictionary of
            the project. If None is specified it will be use the nFluid
            default template.

        See Also
        --------
        create_openfoam_snappy_project
        """
        self.export_shapes('foam.stl', close=True)
        cfmesh_generator.generate_cfmesh_project('foam.stl',
                                                 template)

    def extract_simphony_mesh(self):
        """Exports the mesh of the current assembly to a SimPhony mesh
        object.

        Returns
        -------
        A Mesh object from SimPhoNy.

        """
        return Shape.simphony_mesh()

    def show_shapes(self):
        """Opens a modal standalone visualizer containing the full structure
        of the assembly.

        """
        Shape.show()

    def delete_element(self, element):
        """Removes an element from the assembly.

        Since deleting a tee its problematic because two channels
        can't be linked to one, deleting a tee is not allowed.

        Parameters
        ----------
            element : ChannelElement
                The element to be deleted.

        """

        if not isinstance(element, ChannelElement2G):
            if len(element.tails) != 0:
                raise TypeError('unsupported operand type(s)')
        else:
            element.delete()

        try:
            index = self.elements.index(element)
            del self.elements[index]
        except:
            print 'delete_element error'

    def insert_element_before(self, element, element_before):
        """Links a new element int the assembly to another existing element
        in the assembly.

        Parameters
        ----------
            element : ChannelElement
                the new element to be added

            element_before : ChannelElement
                the element we want to insert before to

"""

        if not isinstance(element, ChannelElement2G):
            raise TypeError('unsupported operand type(s)')

        element_before.insert_before(element)

        #    return

        try:
            index = self.elements.index(element)
            del self.elements[index]
        except:
            print 'insert_element_before error'

        try:
            index = self.elements.index(element_before)
            self.elements.insert(index, element)
        except:
            print 'insert_element_before error'

    def print_info_file(self, filename=None):
        """Creates a detailed file containing all the important
        information of the assembly.

        Parameters
        ----------
            filename : string
                the name of the output file

        """
        self.info_extractor.print_output(filename)

    def get_tree_structure(self):
        if len(self.elements) == 0:
            return None
        tree = self._get_tree_structure()
        return tree

    def _get_tree_structure(self):
        tree = TreeBase(TreeNode(self.elements[0]))
        cur_node = tree.get_root()
        queue = [(cur_node, self.elements[0])]
        while len(queue) != 0:
            cur_node, cur_elem = queue.pop()
            if cur_elem is not None:
                for i in xrange(len(cur_elem.tails)):
                    next_elem = cur_elem.get_next_element(i)
                    if next_elem is not None:
                        new_node = tree.add_node(cur_node, TreeNode(next_elem))
                        queue.append((new_node, next_elem))
        return tree


def create_channel(elt):
    return elt
