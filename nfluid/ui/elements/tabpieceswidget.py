from PySide import QtCore, QtGui
from nfluid.core.channel_assembly import ChannelAssembly
from nfluid.core.channel_element import ChannelElement
from nfluid.ui.elements.auxiliar import WidgetParameterNumber
from nfluid.ui.elements.auxiliar import WidgetParameterVector
from nfluid.ui.elements.auxiliar import WidgetNewPiece
from nfluid.ui.elements.auxiliar import strings


_pieces = [('Coupling',
                [(strings.head_radius, 0),
                 (strings.length, 0)
                ]
            ),
           ('Flow Adapter',
                [(strings.head_radius, 0),
                 (strings.tail_radius, 0),
                 (strings.length, 0)
                ])]
            # ),
           # ('Short Elbow',
                # [
                
                # ]
            # ),
           # ('Long Elbow',
                # [
                
                # ]
            # ),
           # ('Spheric Coupling',
                # [
                
                # ]
            # ),
           # ('Tee',
                # [
                
                # ]
            # )
           # ]

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
        params = {}

        params[strings.head_position] = cur_page.get_param(strings.head_position)
        params[strings.tail_position] = cur_page.get_param(strings.tail_position)
        params[strings.tail_position0] = cur_page.get_param(strings.tail_position0)
        params[strings.tail_position1] = cur_page.get_param(strings.tail_position1)
        params[strings.head_normal] = cur_page.get_param(strings.head_normal)
        params[strings.tail_normal] = cur_page.get_param(strings.tail_normal)
        params[strings.tail_normal0] = cur_page.get_param(strings.tail_normal0)
        params[strings.tail_normal1] = cur_page.get_param(strings.tail_normal1)
        params[strings.head_radius] = cur_page.get_param(strings.head_radius)
        params[strings.tail_radius] = cur_page.get_param(strings.tail_radius)
        params[strings.length] = cur_page.get_param(strings.length)
        params[strings.curvature_radius] = cur_page.get_param(strings.curvature_radius)
        params[strings.angle] = cur_page.get_param(strings.angle)
        params[strings.sphere_radius] = cur_page.get_param(strings.sphere_radius)
        params[strings.points_list] = cur_page.get_param(strings.points_list)
        
        return (name, params)
        