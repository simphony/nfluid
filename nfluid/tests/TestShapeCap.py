from nfluid.core.channel_assembly import *
from nfluid.elements.circle_coupling import *
from nfluid.elements.cap import *
from nfluid.tests.TestBase import *
import os

print os.path.basename(__file__), "------------------------\n"

assembly = ChannelAssembly()


create_channel( 
    Coupling(10, 20, 
    PosH = Vector(0, 27, 35), 
    Normal = Vector(0, 0, 1) 
    ) 
  ). \
  link(Cap(L = 5))


MakeTest1(assembly)
