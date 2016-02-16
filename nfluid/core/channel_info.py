from nfluid.core.channel_element import ChannelElement
from nfluid.core.channel_element_2g import ChannelElement2G


sep_s = '\n' + '-'*40 + '\n'
sep_m = '\n' + '='*60 + '\n'
sep_l = '\n' + '_'*80 + '\n' + '='*80 + '\n'
sep_xl = '\n' + '_'*100 + '\n' + '='*100 + '\n' + \
                      '_'*100 + '\n'


class GateInfo(object):

    def __init__(self, gate, id):
        self.gate = gate
        self.id = id
        # convert the info we want
        self.extract_info()

    def extract_info(self):
        self.radius = self.gate.get_r()
        self.normal = self.gate.get_normal()
        self.pos = self.gate.get_pos()
        self.next = self.gate.element.get_next_element(self.id)

    def has_next(self):
        return (self.next is not None)

    def get_next(self):
        return self.next

    def get_pos(self):
        return self.pos

    def get_normal(self):
        return self.normal

    def get_radius(self):
        return self.radius

    def __str__(self):
        res = 'Radius: ' + str(self.radius) + '\n' + \
              'Position: ' + str(self.pos) + '\n' + \
              'Normal: ' + str(self.normal) + '\n'
        return res


class PieceInfo(object):

    def __init__(self, elem):
        self.elem = elem
        self.head = None
        self.tails = []
        # convert the info we want
        self.extract_info()

    def extract_common_info(self):
        self.id = self.elem.get_id()
        self.name = self.elem.get_name()
        self.radius = self.elem.get_r()
        self.length = self.elem.get_len()
        self.volume = self.elem.get_volume()
        self.pos = self.elem.get_pos_head()
        self.normal = self.elem.get_normal_head()
        self.head = GateInfo(self.elem.heads[0], 0)
        n = 0
        for gate in self.elem.tails:
            self.tails.append(GateInfo(gate, n))
            n += 1

    def extract_specific_info(self):
        print "id, name"
        print self.id, self.name
        try:
            self.curvature_radius = self.elem.RadiusCurvature
            print "GOOD ", self.curvature_radius
        except:
            self.curvature_radius = None
            print "BAD ", self.curvature_radius
        try:
            self.angle = self.elem.angle
            print "GOOD ", self.angle
        except:
            self.angle = None
            print "BAD ", self.angle
        try:
            self.sphere_radius = self.elem.RadiusSphere
            print "GOOD ", self.sphere_radius
        except:
            self.sphere_radius = None
            print "BAD ", self.sphere_radius
        try:
            self.points_list = self.elem.InputPoints
            print "GOOD ", self.points_list
        except:
            self.points_list = None
            print "BAD ", self.points_list

    def extract_info(self):
        self.extract_common_info()
        self.extract_specific_info()

    def get_pos(self):
        return self.pos

    def get_normal(self):
        return self.normal

    def __str__(self):
        res = 'Id: ' + str(self.id) + '\n' + \
              'Name: ' + str(self.name) + '\n' + \
              'Radius: ' + str(self.radius) + '\n' + \
              'Length: ' + str(self.length) + '\n' + \
              'Volume: ' + str(self.volume) + '\n' + \
              'Position: ' + str(self.pos) + '\n' + \
              'Normal: ' + str(self.normal) + '\n'
        if self.curvature_radius is not None:
            res += 'Curvature Radius: ' + \
                   str(self.curvature_radius) + '\n'
        if self.angle is not None:
            res += 'Angle: ' + str(self.angle) + '\n'
        if self.sphere_radius is not None:
            res += 'Sphere Radius: ' + str(self.sphere_radius) + '\n'
        if self.points_list is not None:
            res += 'Points list:\n'
            for p in self.points_list:
                res += '    ' + str(p) + '\n'
        res += 'Gates: \n' + \
               '    Head: \n        ' + str(self.head) + '\n' + \
               '    Tails: \n'
        for tail in self.tails:
            res += '        ' + str(tail) + sep_s
        return res


class ChannelInfo(object):

    def __init__(self, assembly):
        self.assembly = assembly

    def get_initial_piece(self):
        for elem in self.assembly.elements:
            if elem.get_prev_element() is None:
                return PieceInfo(elem)

    def get_final_pieces(self):
        res = []
        for elem in self.assembly.elements:
            if isinstance(elem, ChannelElement2G):
                if elem.get_next_element() is None:
                    res.append(PieceInfo(elem))
            elif isinstance(elem, ChannelElement):
                i = 0
                total_tails = len(elem.tails)
                while (i < total_tails and
                       elem.get_next_element(i) is not None):
                        i += 1
                if i < total_tails:
                    res.append(PieceInfo(elem))
        return res

    def get_assembly_length(self):
        res = 0.0
        for elem in self.assembly.elements:
            res += elem.get_len()
        return res

    def get_assembly_volume(self):
        res = 0.0
        for elem in self.assembly.elements:
            res += elem.get_volume()
        return res

    def get_number_of_pieces(self):
        return len(self.assembly.elements)

    def get_assembly_structure(self):
        tree = self.assembly.get_tree_structure()
        n_levels = tree.depth()
        for i in range(n_levels):
            cur_level = i + 1
            elems = tree.get_level(cur_level)
            n_elems = len(elems)
            

    def get_assembly_pieces(self):
        # return copy.deepcopy(self.assembly.elements)
        res = []
        for elem in self.assembly.elements:
            res.append(PieceInfo(elem))
        return res


class ChannelInfoParser(object):

    def __init__(self, info):
        self.info = info

    def str_title_intro(self):
        res = ''
        res += '================ Assembly information ================\n'
        res += '======================================================\n'
        return res

    def str_title_init(self):
        res = ''
        res += '\n' + 'Init information' + '\n'
        res += '----------------' + '\n'
        return res

    def str_title_end(self):
        res = ''
        res += '\n' + 'End information' + '\n'
        res += '---------------' + '\n'
        return res

    def str_title_general_info(self):
        res = ''
        res += '\n' + 'General information' + '\n'
        res += '-------------------' + '\n'
        return res

    def str_title_pieces_info(self):
        res = ''
        res += '\n' + 'Pieces information' + '\n'
        res += '------------------' + '\n'
        return res

    def str_init_info(self):
        res = ''
        init_piece = self.info.get_initial_piece()
        res += str(init_piece.head)
        return res

    def str_end_info(self):
        res = ''
        end_pieces = self.info.get_final_pieces()
        for piece in end_pieces:
            for tail in piece.tails:
                res += '\n'
                res += str(tail)
                res += '\n'
            res += sep_m
        return res

    def str_general_info(self):
        res = ''
        length = self.info.get_assembly_length()
        volume = self.info.get_assembly_volume()
        n_pieces = self.info.get_number_of_pieces()
        res += '\nLength: ' + str(length)
        res += '\nVolume: ' + str(volume)
        res += '\nNumber of pieces: ' + str(n_pieces)
        res += '\n'
        return res

    def str_pieces_info(self):
        res = ''
        pieces = self.info.get_assembly_pieces()
        for piece in pieces:
            res += str(piece) + sep_m
        return res

    def output_text(self):
        res = ''
        res += self.str_title_intro()
        sep_s
        res += self.str_title_init() + '\n'
        res += self.str_init_info() + '\n'
        res += sep_l
        res += self.str_title_end() + '\n'
        res += self.str_end_info() + '\n'
        res += sep_l
        res += self.str_title_general_info() + '\n'
        res += self.str_general_info() + '\n'
        res += sep_l
        res += self.str_title_pieces_info() + '\n'
        res += self.str_pieces_info() + '\n'
        return res

    def print_output(self, filename=None):
        if filename is None:
            print self.output_text()
        else:
            text = self.output_text()
            f = open(filename, 'w')
            f.write(text)
            f.close()
