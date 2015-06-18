from nfluid.core.channel_assembly import *
from nfluid.elements.circle_bifurcation import *
from nfluid.elements.flow_adapter import *
from nfluid.elements.circle_coupling import *
from nfluid.tests.TestBase import *
import os

print os.path.basename(__file__), "------------------------\n"

assembly = ChannelAssembly()


bif = create_channel( 
    Coupling(111, 78, 
    PosH = Vector(11, 22, 33), 
    Normal = Vector(0, 0, 1) 
    ) 
  ). \
  link(FlowAdapter(RT = 220, L = 15)). \
  link(Coupling(L = 125)).  \
  link(BifurcationCircle(220)) 

#
bif. \
  link(FlowAdapter(RT =123, L = 20)). \
  link(Coupling(L = 200))


bif. \
  link(FlowAdapter(RT =150, L = 20), 1). \
  link(Coupling(L = 200))

MakeTest1(assembly)

