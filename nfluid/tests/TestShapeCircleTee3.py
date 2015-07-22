from nfluid.core.channel_assembly import *
from nfluid.elements.flow_adapter import *
from nfluid.elements.circle_coupling import *
from nfluid.elements.circle_tee3 import *
from nfluid.tests.TestBase import *
import os

print os.path.basename(__file__), "------------------------\n"

assembly = ChannelAssembly()


tee = create_channel( 
    Coupling(111, 78, 
    PosH = Vector(11, 22, 33), 
    Normal = Vector(0, 0, 1) 
    ) 
  ). \
  link(FlowAdapter(RT = 220, L = 15)). \
  link(Coupling(L = 125)).  \
  link(TeeCircle3(220,NormalH = Vector(0, 0, 1), NormalT0 = Vector(1, 0, 0))) 

#
tee. \
  link(FlowAdapter(RT =123, L = 20)). \
  link(Coupling(L = 200))


tee. \
  link(FlowAdapter(RT =155, L = 27), 1). \
  link(Coupling(L = 120))
"""
tee. \
  link(FlowAdapter(RT =15, L = 7), 2). \
  link(Coupling(L = 20))
"""

MakeTest1(assembly)
