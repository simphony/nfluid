from PySide import QtCore, QtGui
from nfluid.core.channel_assembly import ChannelAssembly
from nfluid.core.channel_element import ChannelElement
from nfluid.ui.elements.auxiliar import WidgetParameterNumber
from nfluid.ui.elements.auxiliar import WidgetParameterVector
from nfluid.ui.elements.auxiliar import WidgetNewPiece
from nfluid.ui.elements.auxiliar import strings
from nfluid.ui.manager import NfluidDataManager, Piece


_pieces = [(strings.coupling,
                [(strings.head_radius, 0),
                 (strings.length, 0)
                ]
            ),
           (strings.flow_adapter,
                [(strings.head_radius, 0),
                 (strings.tail_radius, 0),
                 (strings.length, 0)
                ]
            ),
           (strings.short_elbow,
                [(strings.head_radius, 0),
                 (strings.tail_normal, (0,0,0))
                ]
            ),
           (strings.long_elbow,
                [(strings.curvature_radius, 0),
                 (strings.head_radius, 0),
                 (strings.tail_normal, (0,0,0))
                ]
            ),
           (strings.long_elbow_angle,
                [(strings.curvature_radius, 0),
                 (strings.head_radius, 0),
                 (strings.tail_normal, (0,0,0)),
                 (strings.angle, 0),
                ]
            ),
           (strings.spheric_coupling,
                [(strings.head_radius, 0),
                 (strings.sphere_radius, 0),
                 (strings.tail_normal, (0,0,0))
                ]
            ),
           (strings.tee,
                [(strings.head_radius, 0),
                 (strings.tail_normal0, (0,0,0))
                ]
            )
           ]

class TabPiecesWidget(QtGui.QTabWidget):
    
    def __init__(self):
        super(TabPiecesWidget, self).__init__()
        self.create_gui()
        self._name = "  Pieces Creation"

    def name(self):
        return self._name

    def create_gui(self):
        for piece in _pieces:
            new_piece_widget = WidgetNewPiece(piece[0], piece[1])
            self.addTab(new_piece_widget, new_piece_widget.name())
            
    def get_piece(self):
        cur_page = self.currentWidget()
        name = cur_page.name()
        parameters = {}

        parameters[strings.head_position] = cur_page.get_param(strings.head_position)
        parameters[strings.tail_position] = cur_page.get_param(strings.tail_position)
        parameters[strings.tail_position0] = cur_page.get_param(strings.tail_position0)
        parameters[strings.tail_position1] = cur_page.get_param(strings.tail_position1)
        parameters[strings.head_normal] = cur_page.get_param(strings.head_normal)
        parameters[strings.tail_normal] = cur_page.get_param(strings.tail_normal)
        parameters[strings.tail_normal0] = cur_page.get_param(strings.tail_normal0)
        parameters[strings.tail_normal1] = cur_page.get_param(strings.tail_normal1)
        parameters[strings.head_radius] = cur_page.get_param(strings.head_radius)
        parameters[strings.tail_radius] = cur_page.get_param(strings.tail_radius)
        parameters[strings.length] = cur_page.get_param(strings.length)
        parameters[strings.curvature_radius] = cur_page.get_param(strings.curvature_radius)
        parameters[strings.angle] = cur_page.get_param(strings.angle)
        parameters[strings.sphere_radius] = cur_page.get_param(strings.sphere_radius)
        parameters[strings.points_list] = cur_page.get_param(strings.points_list)
        
        return Piece(type=name, params=parameters)
        