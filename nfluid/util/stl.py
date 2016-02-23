# STL utility functions
from nfluid.geometry.functions import normal_of, center_of


class STL_Info():
    def __init__(self, file_name):
        self.file = open(file_name, "r")
        self.minx = 0.0
        self.maxx = 0.0
        self.miny = 0.0
        self.maxy = 0.0
        self.minz = 0.0
        self.maxz = 0.0
        self.inside_point = (0,0,0)
        self.outside_point = (0,0,0)
        self.onface_point = (0,0,0)
        self.output = open('{}_box.txt'.format(file_name), "w")
        self.surrounding_box()
        self._write_output()
        self.file.close()
        self.output.close()

    def _coordinates_of_vertex(self, line):
        words = line.split(' ')
        x = words[1]
        y = words[2]
        z = words[3]
        return (float(x), float(y), float(z))

    def _check_limits(self, coordinates):
        if coordinates[0] < self.minx:
            self.minx = coordinates[0]
        if coordinates[0] > self.maxx:
            self.maxx = coordinates[0]
        if coordinates[1] < self.miny:
            self.miny = coordinates[1]
        if coordinates[1] > self.maxy:
            self.maxy = coordinates[1]
        if coordinates[2] < self.minz:
            self.minz = coordinates[2]
        if coordinates[2] > self.maxz:
            self.maxz = coordinates[2]

    def _write_output(self):
        self.output.write('MinX {}\n'.format(self.minx))
        self.output.write('MaxX {}\n'.format(self.maxx))
        self.output.write('MinY {}\n'.format(self.miny))
        self.output.write('MaxY {}\n'.format(self.maxy))
        self.output.write('MinZ {}\n'.format(self.minz))
        self.output.write('MaxZ {}\n'.format(self.maxz))

    def surrounding_box(self):
        """This will calculate the surrounding box of any given .stl file
        and write the results in a "file_name_box.txt" file.
        Format:
            MinX XXX
            MaxX XXX
            MinY XXX
            MaxY XXX
            MinZ XXX
            MaxZ XXX
        """
        txt = self.file.read()
        lines = txt.split('\n')
        n_lines = len(lines)
        i = 3
        # We process this separate to calculate some information points

        v0 = self._coordinates_of_vertex(lines[i])
        self._check_limits(v0)
        v1 = self._coordinates_of_vertex(lines[i+1])
        self._check_limits(v1)
        v2 = self._coordinates_of_vertex(lines[i+2])
        self._check_limits(v2)

        normal = normal_of(v0, v1, v2)
        center = center_of([v0,v1,v2])
        t = 1.00
        self.inside_point = (center[0] - (normal[0]*t),
                             center[1] - (normal[1]*t),
                             center[2] - (normal[2]*t))
        self.outside_point = (center[0] + (normal[0]*t),
                              center[1] + (normal[1]*t),
                              center[2] + (normal[2]*t))
        self.onface_point = center

        i = i + 7

        while i < n_lines:
            v0 = self._coordinates_of_vertex(lines[i])
            self._check_limits(v0)
            v1 = self._coordinates_of_vertex(lines[i+1])
            self._check_limits(v1)
            v2 = self._coordinates_of_vertex(lines[i+2])
            self._check_limits(v2)
            i = i + 7
