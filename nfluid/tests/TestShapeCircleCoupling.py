from nfluid.core.channel_assembly import *
from nfluid.elements.flow_adapter import *
from nfluid.elements.circle_coupling import *
from nfluid.tests.TestBase import *
import os

print os.path.basename(__file__), "------------------------\n"

assembly = ChannelAssembly()

create_channel( 
    Coupling(R = 10, L = 45,
    PosH = Vector(0, 20, 30),
    Normal = Vector(1, 0, 0) 
    ) 
 
  ). \
  link (Coupling(PosT = Vector(400, 20, 0)))


"""
create_channel( 
    Coupling(R = 10, 
    PosH = Vector(0, 20, 30),
    PosT = Vector(0, 20, 150)  
    ) 
 
  ). \
  link (Coupling(PosT = Vector(0, 20, 400)))
"""
#    Normal = Vector(1, 0, 0) 
#  link (Coupling(L = 125) )
#  link (Coupling(PosH = Vector(0, 20, 50), PosT = Vector(0, 20, 400)) )


MakeTest1(assembly)
