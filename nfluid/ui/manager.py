from nfluid.core.channel_assembly import ChannelAssembly
from nfluid.core.channel_element import ChannelElement
from nfluid.elements.circle_coupling import CircleCoupling
from nfluid.elements.circle_tee import CircleTee
from nfluid.elements.flow_adapter import FlowAdapter
from nfluid.elements.long_elbow_angle import LongElbowAngle
from nfluid.elements.short_elbow_angle import ShortElbowAngle
from nfluid.elements.long_elbow_normals import LongElbowNormals
from nfluid.elements.short_elbow_normals import ShortElbowNormals
from nfluid.elements.spheric_coupling import SphericCoupling
from nfluid.elements.circle_path import CirclePath
from nfluid.elements.cap import Cap
from nfluid.shapes.shapes import Shape
from nfluid.ui.elements.auxiliar import strings
from nfluid.util.vector import Vector
from nfluid.util.tree import TreeFunctions
import copy
import visvis as vv


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

    def __str__(self):
        return self.name()

    def _extract_param(self, elem, param):
        try:
            res = None
            if param == strings.head_position:
                res = elem.get_pos_head()
            elif param == strings.tail_position:
                res = elem.get_pos_tail()
            elif param == strings.tail_position0:
                res = elem.get_pos_tail(0)
            elif param == strings.tail_position1:
                res = elem.get_pos_head(1)
            elif param == strings.head_normal:
                res = elem.get_normal_head()
            elif param == strings.tail_normal:
                res = elem.get_normal_tail()
            elif param == strings.tail_normal0:
                res = elem.get_normal_tail(0)
            elif param == strings.tail_normal1:
                res = elem.get_normal_tail(1)
            elif param == strings.head_radius:
                res = elem.get_r()
            elif param == strings.tail_radius:
                res = elem.get_rt()
            elif param == strings.length:
                res = elem.get_len()
            elif param == strings.curvature_radius:
                res = elem.get_r_curv()
            elif param == strings.sphere_radius:
                res = elem.get_sphere_r()
            elif param == strings.points_list:
                res = elem.get_points()
            elif param == strings.angle:
                res = elem.get_angle()
            return res
        except:
            return None

    def from_element(self, elem):
        self.type = NfluidDataManager.get_string(elem)
        self.id = elem.get_id()
        parameters = {}

        parameters[strings.head_position] = \
            self._extract_param(elem, strings.head_position)
        parameters[strings.tail_position] = \
            self._extract_param(elem, strings.tail_position)
        parameters[strings.tail_position0] = \
            self._extract_param(elem, strings.tail_position0)
        parameters[strings.tail_position1] = \
            self._extract_param(elem, strings.tail_position1)
        parameters[strings.head_normal] = \
            self._extract_param(elem, strings.head_normal)
        parameters[strings.tail_normal] = \
            self._extract_param(elem, strings.tail_normal)
        parameters[strings.tail_normal0] = \
            self._extract_param(elem, strings.tail_normal0)
        parameters[strings.tail_normal1] = \
            self._extract_param(elem, strings.tail_normal1)
        parameters[strings.head_radius] = \
            self._extract_param(elem, strings.head_radius)
        parameters[strings.tail_radius] = \
            self._extract_param(elem, strings.tail_radius)
        parameters[strings.length] = self._extract_param(elem, strings.length)
        parameters[strings.curvature_radius] = \
            self._extract_param(elem, strings.curvature_radius)
        parameters[strings.angle] = self._extract_param(strings.angle)
        parameters[strings.sphere_radius] = \
            self._extract_param(elem, strings.sphere_radius)
        parameters[strings.points_list] = \
            self._extract_param(elem, strings.points_list)

        self.parameters = parameters


class TreeFunctionsManager(TreeFunctions):
    @classmethod
    def reset(cls):
        TreeFunctions.reset()

    @classmethod
    def convert_data(cls, elem, params=None):
        name = elem.data.get_name()
        if name == 'CircleCoupling':
            name = strings.coupling
        elif name == 'SphericCoupling':
            name = strings.spheric_coupling
        elif name == 'FlowAdapter':
            name = strings.flow_adapter
        elif name == 'CircleTee':
            name = strings.tee
        elif name == 'ShortElbowAngle':
            name = strings.short_elbow_angle
        elif name == 'LongElbowAngle':
            name = strings.long_elbow_angle
        elif name == 'ShortElbowNormals':
            name = strings.short_elbow_normals
        elif name == 'LongElbowNormals':
            name = strings.long_elbow_normals
        elif name == 'Cap':
            name = strings.cap
        elif name == 'CirclePath':
            name = strings.circle_path
        elem.data = Piece(name, elem.data.get_id())


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
        return (NfluidDataManager.model is not None)

    @classmethod
    def add_piece(cls, piece):
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
                   its initial head normal."
            normal = NfluidDataManager.gui.ask_for(Vector,
                                                   strings.head_normal,
                                                   msg)
            piece.params[strings.head_normal] = normal
            msg = "As is the first piece of the assembly, you must define\
                   its initial head radius."
            radius = NfluidDataManager.gui.ask_for(float,
                                                   strings.head_radius,
                                                   msg)
            piece.params[strings.head_radius] = radius
            if piece.params[strings.tail_normal] is None:
                if piece.params[strings.tail_normal0] is None:
                    # We copy the same normal, since if its not defined
                    # means that we have a symmetric element
                    piece.params[strings.tail_normal] =\
                                piece.params[strings.head_normal]
            new_piece = NfluidDataManager.create_piece(piece)
            NfluidDataManager.model.clear_geometry()
            NfluidDataManager.model.resolve_geometry()
            return 0
        else:
            current_piece = NfluidDataManager.gui.\
                            dw_pieces_list.widget().\
                            current_piece()
            if current_piece.id == -1:
                msg = "No piece selected to link to!"
                NfluidDataManager.gui.message(msg)
                return -1
            else:
                selected_piece = NfluidDataManager.get_piece(current_piece)
                selected_piece.print_info()
                new_piece = NfluidDataManager.create_piece(piece)
                if current_piece.type == strings.tee:
                    gate = 0
                    msg = "As you are linking to a tee, you need to\
                           specify the gate (0 or 1)."
                    gate = NfluidDataManager.gui.ask_for(int,
                                                         strings.gate,
                                                         msg)
                    selected_piece.link(new_piece, gate)
                else:
                    selected_piece.link(new_piece)
                NfluidDataManager.model.clear_geometry()
                NfluidDataManager.model.resolve_geometry()
                return 0

    @classmethod
    def remove_piece(cls, piece):
        selected = NfluidDataManager.get_piece(piece)
        NfluidDataManager.model.delete_element(selected)

    @classmethod
    def get_piece(cls, piece):
        return NfluidDataManager.model.get_element_by_id(
                                    piece.id)

    @classmethod
    def remove_all(cls):
        # for elem in NfluidDataManager.model.elements:
            # NfluidDataManager.model.delete_element(elem)
        NfluidDataManager.model.elements = []

    @classmethod
    def get_string(self, element):
        if isinstance(element, CircleCoupling):
            return strings.coupling
        if isinstance(element, FlowAdapter):
            return strings.flow_adapter
        if isinstance(element, ShortElbowAngle):
            return strings.short_elbow_angle
        if isinstance(element, LongElbowAngle):
            return strings.long_elbow_angle
        if isinstance(element, ShortElbowNormals):
            return strings.short_elbow_normals
        if isinstance(element, LongElbowNormals):
            return strings.long_elbow_normals
        if isinstance(element, SphericCoupling):
            return strings.spheric_coupling
        if isinstance(element, CircleTee):
            return strings.tee
        if isinstance(element, CirclePath):
            return strings.circle_path
        if isinstance(element, Cap):
            return strings.cap

    @classmethod
    def list_of_pieces(cls):
        res = []
        if not NfluidDataManager.exists():
            return res
        for element in NfluidDataManager.model.elements:
            type = NfluidDataManager.get_string(element)
            id = element.get_id()
            res.append(Piece(type, id))
        return res

    @classmethod
    def get_total_mesh(self):
        if not NfluidDataManager.exists():
            return None
        NfluidDataManager.model.create_shapes()
        return Shape.total_mesh

    @classmethod
    def get_assembly_tree(self):
        if not NfluidDataManager.exists():
            return None
        tree = NfluidDataManager.model.get_tree_structure()
        if tree is not None:
            tree.walk_amplitude(func=TreeFunctionsManager.convert_data)
        return tree

    @classmethod
    def export_mesh_stl(self):
        file_name = NfluidDataManager.gui.get_path_save_file(ext='.stl')
        title = 'Close .stl?'
        msg = 'Do you want to close the exported .stl surface?'
        close = NfluidDataManager.gui.ask_for(bool,
                                              title,
                                              msg)
        NfluidDataManager.model.export_shapes(file_name[0], close)
        vv.closeAll()

    @classmethod
    def export_mesh_info_txt(self):
        file_name = NfluidDataManager.gui.get_path_save_file(ext='.txt')
        NfluidDataManager.model.print_info_file(file_name[0])

    @classmethod
    def export_mesh_foam_snappy(self):
        NfluidDataManager.model.create_openfoam_snappy_project()
        msg = "Exported as snappy project."
        NfluidDataManager.gui.message(msg)

    @classmethod
    def export_mesh_foam_cfmesh(self):
        NfluidDataManager.model.create_openfoam_cfmesh_project()
        msg = "Exported as cfmesh (tetmesh) project."
        NfluidDataManager.gui.message(msg)

    @classmethod
    def number_of_pieces(self):
        return len(NfluidDataManager.model.elements)

    @classmethod
    def create_piece(self, piece):
        """Factory function for piece creation.
        """
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
        if piece.type == strings.short_elbow_angle:
            return ShortElbowAngle(R=piece.params[strings.head_radius],
                                   Angle=piece.params[strings.angle],
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
        if piece.type == strings.short_elbow_normals:
            return ShortElbowNormals(R=piece.params[strings.head_radius],
                                     PosH=piece.params[strings.head_position],
                                     PosT=piece.params[strings.tail_position],
                                     NormalH=piece.params[strings.head_normal],
                                     NormalT=piece.params[strings.tail_normal])
        if piece.type == strings.long_elbow_normals:
            return LongElbowNormals(R=piece.params[strings.head_radius],
                                    RC=piece.params[strings.curvature_radius],
                                    PosH=piece.params[strings.head_position],
                                    PosT=piece.params[strings.tail_position],
                                    NormalH=piece.params[strings.head_normal],
                                    NormalT=piece.params[strings.tail_normal])
        if piece.type == strings.spheric_coupling:
            return SphericCoupling(R=piece.params[strings.head_radius],
                                   RS=piece.params[strings.sphere_radius],
                                   PosH=piece.params[strings.head_position],
                                   PosT=piece.params[strings.tail_position],
                                   Normal=piece.params[strings.tail_normal])
        if piece.type == strings.tee:
            return CircleTee(R=piece.params[strings.head_radius],
                             PosH=piece.params[strings.head_position],
                             PosT0=piece.params[strings.tail_position0],
                             PosT1=piece.params[strings.tail_position1],
                             NormalH=piece.params[strings.head_normal],
                             NormalT0=piece.params[strings.tail_normal0],
                             NormalT1=piece.params[strings.tail_normal1])
        if piece.type == strings.cap:
            return Cap(L=piece.params[strings.length],
                       R=piece.params[strings.head_radius],
                       PosH=piece.params[strings.head_position],
                       NormalH=piece.params[strings.head_normal])
        if piece.type == strings.circle_path:
            return CirclePath(Points=piece.params[strings.points_list],
                              R=piece.params[strings.head_radius],
                              PosH=piece.params[strings.head_position],
                              PosT=piece.params[strings.tail_position],
                              NormalH=piece.params[strings.head_normal],
                              NormalT=piece.params[strings.tail_normal],
                              Twist=piece.params[strings.angle])
