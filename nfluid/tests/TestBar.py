from channel_assembly import *
from flow_adapter import *
from circle_coupling import *
from elbow import *
from TestBase import *
from square_coupling import *
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

