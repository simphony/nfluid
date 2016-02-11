#!/usr/bin/python
# -*- coding: utf-8 -*-
from nfluid.core.channel_info import ChannelInfoParser
from nfluid.core.channel_info import ChannelInfo
from nfluid.core.channel_element import ChannelElement
from nfluid.core.channel_element_2g import ChannelElement2G
from nfluid.shapes.shapes import Shape
from nfluid.util import snappy_generator


class ChannelAssembly(object):

    def __init__(self):
        self.elements = []
        ChannelElement.assembly = self
        self.info_extractor = ChannelInfoParser(ChannelInfo(self))

    def add_element(self, element):
        self.elements.append(element)

    def get_element_by_id(self, id):
        for element in self.elements:
            if element.get_id() == id:
                return element
        return None

    def for_each_element(self, fcn):
        for element in self.elements:
            fcn(element)

    def resolve_geometry(self):

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
        for element in self.elements:
            res = element.is_resolved_geometry()
            if res != '':
                return 'Geometry not resolved in' \
                    + element.get_chain_str() + ':' + res
        return ''

    def clear_geometry(self):
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
        Shape.init()

        for element in self.elements:
            res = element.create_shape()
            if res != '':
                return res
            Shape.add_shape(element.shape)

        return Shape.finalize()

    def release_shapes(self):
        for element in self.elements:
            element.release_shape()
        Shape.release()

    def export_shapes(self, file_name):
        # file = open(file_name, 'w')
        Shape.export(file_name)
        # file.close()
        return ''

    def create_openfoam_project(self, stl=None, template=None):
        self.export_shapes('foam.stl')
        snappy_generator.generate_snappy_project('foam.stl',
                                                 template)

    def extract_simphony_mesh(self):
        return Shape.simphony_mesh()

    def show_shapes(self):
        Shape.show()

    def delete_element(self, element):

        if not isinstance(element, ChannelElement2G):
            raise TypeError('unsupported operand type(s)')

        element.delete()

        try:
            index = self.elements.index(element)
            del self.elements[index]
        except:
            print 'delete_element error'

    def insert_element_before(self, element, element_before):

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
        self.info_extractor.print_output(filename)

def create_channel(elt):
    return elt
