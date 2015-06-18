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
#    Normal = Vector(0, 0, 1) 
    ) 
  ). \
  link(FlowAdapter(RH = 22, L = 15)). \
  link(Coupling(L = 125)).  \
  link(FlowAdapter(RH =12, L = 20)). \
  link(Coupling(88, 20, PosT = Vector(11, 22, 800)))


MakeTest1(assembly)

