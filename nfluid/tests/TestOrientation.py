from nfluid.core.channel_assembly import *
from nfluid.elements.flow_adapter import *
from nfluid.elements.circle_coupling import *
from nfluid.elements.elbow import *
from nfluid.tests.TestBase import *
import os

print os.path.basename(__file__), "------------------------\n"

assembly = ChannelAssembly()


create_channel( 
    Coupling(111, 78, 
    PosH = Vector(11, 22, 33), 
    Normal = Vector(1, 0, 0) 
    ) 
  ). \
  link(FlowAdapter(L = 20)). \
  link(Coupling(25, L = 125)).  \
  link(FlowAdapter(L = 20)). \
  link(Coupling(30, L = 200))


MakeTest1(assembly)



