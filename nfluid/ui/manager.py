from nfluid.core.channel_assembly import ChannelAssembly
from nfluid.core.channel_element import ChannelElement
from nfluid.elements.cap import Cap
from nfluid.elements.circle_coupling import CircleCoupling
from nfluid.elements.circle_tee import CircleTee
from nfluid.elements.flow_adapter import FlowAdapter
from nfluid.elements.long_elbow import LongElbow
from nfluid.elements.long_elbow_angle import LongElbowAngle
from nfluid.elements.short_elbow import ShortElbow
from nfluid.elements.spheric_coupling import SphericCoupling
from nfluid.shapes.shapes import Shape
from nfluid.ui.elements.auxiliar import strings
from nfluid.util.vector import Vector
import copy

class Piece(object):
    sep = '-'
    
    def __init__(self, type='', id=-1, params=None):
        self.type = type
        self.id = id
        self.params = copy.deepcopy(params)
    
    def name(self):
        return self.type + Piece.sep + str(self.id)
    
    def set_name(self, name):
        elems = name.split(Piece.sep)
        self.type = elems[0]
        self.id = int(elems[1])

class NfluidDataManager(object):
    
    model = None
    gui = None
    
    def __init__(self, gui):
        if ChannelElement.assembly is None:
            NfluidDataManager.model = ChannelAssembly()
        else:
            NfluidDataManager.model = ChannelElement.assembly
        NfluidDataManager.gui = gui
    
    @classmethod
    def exists(cls):
        return (NfluidDataManager.model != None)
        
    @classmethod
    def add_piece(cls, piece):
        # print "piece..."
        # print piece.type
        # print piece.id
        # print piece.params
        # print piece.params["L  - length"]
        n_pieces = NfluidDataManager.number_of_pieces()
        new_piece = None
        current_piece = None
        if n_pieces == 0:
            msg = "As is the first piece of the assembly, you must define\
                   its initial position."
            pos = NfluidDataManager.gui.ask_for(Vector,
                                                strings.head_position,
                                                msg)
            piece.params[strings.head_position] = pos
            msg = "As is the first piece of the assembly, you must define\
                   its initial normal head."
            normal = NfluidDataManager.gui.ask_for(Vector,
                                                strings.head_normal,
                                                msg)
            piece.params[strings.head_normal] = normal
            if piece.params[strings.tail_normal] is None:
                if piece.params[strings.tail_normal0] is None:
                    # tail_n = NfluidDataManager.gui.ask_for(Vector,
                                                           # strings.tail_normal,
                                                           # msg="")
                    # piece.params[strings.tail_normal] = tail_n
                    # We copy the same normal, since if its not defined
                    # means that we have a symmetric element
                    piece.params[strings.tail_normal]=piece.params[strings.head_normal]
            new_piece = NfluidDataManager.create_piece(piece)
        else:
            current_piece = NfluidDataManager.gui.\
                            dw_pieces_list.widget().\
                            current_piece()
            if current_piece == None:
                msg = "No piece selected to link to!"
                NfluidDataManager.gui.message(msg)
            else:
                selected_piece = NfluidDataManager.model.get_element_by_id(
                                    current_piece.id)
                new_piece = NfluidDataManager.create_piece(piece)
                gate = 0
                if current_piece.type == strings.tee:
                    msg = "As you are linking to a tee, you need to\
                           specify the gate (0 or 1)."
                    gate = NfluidDataManager.gui.ask_for(int,
                                                        strings.gate,
                                                        msg)
                selected_piece.link(new_piece, gate)
        NfluidDataManager.gui.refresh_all()
    
    @classmethod
    def remove_piece(cls, piece):
        pass
    
    @classmethod
    def remove_all(self):
        for elem in NfluidDataManager.model.elements:
            NfluidDataManager.model.delete_element(elem)
        NfluidDataManager.gui.refresh_all()

    @classmethod
    def _get_string(self, element):
        if isinstance(element, CircleCoupling):
            return strings.coupling
        if isinstance(element, FlowAdapter):
            return strings.flow_adapter
        if isinstance(element, ShortElbow):
            return strings.short_elbow
        if isinstance(element, LongElbow):
            return strings.long_elbow
        if isinstance(element, LongElbowAngle):
            return strings.long_elbow_angle
        if isinstance(element, SphericCoupling):
            return strings.spheric_coupling
        if isinstance(element, CircleTee):
            return strings.tee

    @classmethod
    def list_of_pieces(cls):
        # DUMMY !!!!
        res = []
        if not NfluidDataManager.exists():
            return res
        for element in NfluidDataManager.model.elements:
            type = NfluidDataManager._get_string(element)
            id = element.get_id()
            res.append(Piece(type, id))
        # res.append(Piece(strings.coupling, 0))
        # res.append(Piece(strings.coupling, 1))
        # res.append(Piece(strings.flow_adapter, 2))
        # res.append(Piece(strings.short_elbow, 3))
        # res.append(Piece(strings.short_elbow, 4))
        # res.append(Piece(strings.spheric_coupling, 5))
        # res.append(Piece(strings.tee, 6))
        return res
        
    @classmethod
    def get_total_mesh(self):
        if not NfluidDataManager.exists():
            return None
        NfluidDataManager.model.release_shapes()
        NfluidDataManager.model.resolve_geometry()
        NfluidDataManager.model.create_shapes()
        return Shape.total_mesh
    
    @classmethod
    def number_of_pieces(self):
        return len(NfluidDataManager.model.elements)

    @classmethod
    def create_piece(self, piece):
        """Factory function for piece creation.
        """
        print "piece..."
        print piece.type
        print piece.id
        print piece.params
        if piece.type == strings.coupling:
            return CircleCoupling(R=piece.params[strings.head_radius],
                                  L=piece.params[strings.length],
                                  PosH=piece.params[strings.head_position],
                                  PosT=piece.params[strings.tail_position],
                                  Normal=piece.params[strings.tail_normal])
        if piece.type == strings.flow_adapter:
            return FlowAdapter(RH=piece.params[strings.head_radius],
                               RT=piece.params[strings.tail_radius],
                               L=piece.params[strings.length],
                               PosH=piece.params[strings.head_position],
                               PosT=piece.params[strings.tail_position],
                               Normal=piece.params[strings.tail_normal])
        if piece.type == strings.short_elbow:
            return ShortElbow(R=piece.params[strings.head_radius],
                              PosH=piece.params[strings.head_position],
                              PosT=piece.params[strings.tail_position],
                              NormalH=piece.params[strings.head_normal],
                              NormalT=piece.params[strings.tail_normal])
        if piece.type == strings.long_elbow:
            return LongElbow(R=piece.params[strings.head_radius],
                             RC=piece.params[strings.curvature_radius],
                             PosH=piece.params[strings.head_position],
                             PosT=piece.params[strings.tail_position],
                             NormalH=piece.params[strings.head_normal],
                             NormalT=piece.params[strings.tail_normal])
        if piece.type == strings.long_elbow_angle:
            return LongElbowAngle(R=piece.params[strings.head_radius],
                                  RC=piece.params[strings.curvature_radius],
                                  Angle=piece.params[strings.angle],
                                  PosH=piece.params[strings.head_position],
                                  PosT=piece.params[strings.tail_position],
                                  NormalH=piece.params[strings.head_normal],
                                  NormalT=piece.params[strings.tail_normal])
        if piece.type == strings.spheric_coupling:
            return SphericCoupling(R=piece.params[strings.head_radius],
                                   RS=piece.params[strings.sphere_radius],
                                   PosH=piece.params[strings.head_position],
                                   PosT=piece.params[strings.tail_position],
                                   NormalH=piece.params[strings.head_normal],
                                   NormalT=piece.params[strings.tail_normal])
        if piece.type == strings.tee:
            return CircleTee(R=piece.params[strings.head_radius],
                             PosH=piece.params[strings.head_position],
                             PosT0=piece.params[strings.tail_position0],
                             PosT1=piece.params[strings.tail_position1],
                             NormalH=piece.params[strings.head_normal],
                             NormalT0=piece.params[strings.tail_normal0],
                             NormalT1=piece.params[strings.tail_normal1])
    
    