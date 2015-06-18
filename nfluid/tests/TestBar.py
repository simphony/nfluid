from nfluid.core.channel_assembly import *
from nfluid.elements.flow_adapter import *
from nfluid.elements.circle_coupling import *
from nfluid.elements.elbow import *
from nfluid.elements.square_coupling import *
from nfluid.tests.TestBase import *
import os

print os.path.basename(__file__), "------------------------\n"

assembly = ChannelAssembly()


create_channel( 
    CouplingSquare(111, 27, 78, 
    PosH = Vector(11, 22, 33), 
    Normal = Vector(0, 0, 1) 
    ) 
  ). \
  link(CouplingSquare(L = 20)). \
  link(CouplingSquare(L = 125))

MakeTest1(assembly)

