from nfluid.core.channel_element import ChannelElement
from nfluid.core.channel_element_2g import ChannelElement2G


class ChannelInfo(object):

    def __init__(self, assembly):
        self.assembly = assembly

    def get_initial_piece(self):
        res = {}
        for elem in self.assembly.elements:
            if elem.get_prev_element() is None:
                return elem

    def get_final_pieces(self):
        res = []
        for elem in self.assembly.elements:
            if isinstance(elem, ChannelElement2G):
                if elem.get_next_element() is None:
                    res.append(elem)
            elif isinstance(elem, ChannelElement):
                i = 0
                total_tails = len(elem.tails)
                while (i < total_tails and
                    elem.get_next_element(i) is not None):
                        i += 1
                if i < total_tails:
                    res.append(elem)
        return res

    def get_assembly_length(self):
        res = 0.0
        for elem in self.assembly.elements:
            res += elem.get_len()
        return res

    def get_assembly_volume(self):
        return 0.0

    def get_number_of_pieces(self):
        return len(self.assembly.elements)

    def get_assembly_structure(self):
        pass

class ChannelInfoParser(object):

    def __init__(self, info):
        self.info = info
        self.sep_s = '\n' + '-'*40 + '\n'
        self.sep_m = '\n' + '='*60 + '\n'
        self.sep_l = '\n' + '_'*80 + '\n' + '='*80 + '\n'
        self.sep_xl = '\n' + '_'*100 + '\n' + '='*100 + '\n' + \
                      '_'*100 + '\n'  

    def _str_gate_info(self, gate):
        res = ''
        print self.sep_s
        print self.sep_s
        print gate
        print gate.print_info()
        print 'element ', gate.element
        if gate.buddy is None:
            res += 'Position: ' + str(gate.get_pos()) + '\n' + \
                   'Normal: ' + str(gate.get_normal()) + '\n'
        return res

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

    def str_init_info(self):
        res = ''
        init_piece = self.info.get_initial_piece()
        init_pos = init_piece.get_pos_head()
        init_normal = init_piece.get_normal_head()
        res += 'Position: ' + str(init_pos) + '\n' + \
               'Normal: ' + str(init_normal) + '\n'
        return res

    def str_end_info(self):
        res = ''
        end_pieces = self.info.get_final_pieces()
        for piece in end_pieces:
            for tail in piece.tails:
                res += '\n'
                res += self._str_gate_info(tail)
                res += '\n'
            res += self.sep_m
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

    def output_text(self):
        res = ''
        res += self.str_title_intro()
        self.sep_s
        res += self.str_title_init() + '\n'
        res += self.str_init_info() + '\n'
        res += self.sep_l
        res += self.str_title_end() + '\n'
        res += self.str_end_info() + '\n'
        res += self.sep_l
        res += self.str_title_general_info() + '\n'
        res += self.str_general_info() + '\n'
        return res

    def print_output(self, filename=None):
        if filename is None:
            print self.output_text()
        else:
            raise NotImplemented()











                    