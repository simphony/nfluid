from nfluid.core.channel_assembly import *
from nfluid.elements.flow_adapter import *
from nfluid.elements.circle_coupling import *
from nfluid.elements.elbow import *
from nfluid.tests.TestBase import *
import os

print os.path.basename(__file__), "------------------------\n"

assembly = ChannelAssembly()


create_channel( 
    Coupling(L = 78, 
#    PosH = Vector(11, 22, 33), 
#    Normal = Vector(0, 0, 1) 
    ) 
  ). \
  link(FlowAdapter(RH = 222, L = 15)). \
  link(Coupling(L = 125)).  \
  link(FlowAdapter(RH =123, L = 20)). \
  link(Coupling(88, 20, PosT = Vector(11, 22, 1000), Normal = Vector(0, 0, 1)))

MakeTest1(assembly)

