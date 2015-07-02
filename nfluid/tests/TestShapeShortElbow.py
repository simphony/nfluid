from nfluid.core.channel_assembly import *
from nfluid.elements.circle_coupling import *
from nfluid.elements.flow_adapter import *
from nfluid.elements.short_elbow import *
from nfluid.tests.TestBase import *
import os

print os.path.basename(__file__), "------------------------\n"

assembly = ChannelAssembly()


create_channel( 
    Coupling(10, 20, 
    PosH = Vector(0, 20, 30), 
    Normal = Vector(0, 0, 1) 
    ) 
#  ) 
  ). \
  link(ShortElbow(NormalT = Vector(1, 0, 0))). \
  link (Coupling(L = 125)). \
  link(ShortElbow(NormalT = Vector(0, 1, 0))). \
  link (Coupling(L = 140))


#  link(ShortElbow(NormalH = Vector(0, 0, 1), PosT = Vector(0, 70, 100))). \
#  link(ShortElbow(NormalT = Vector(0, 1, 0))). \
#  link(ShortElbow(R= 10, NormalH = Vector(0, 0, 1), NormalT = Vector(1, 0, 0))). \

#  link(ShortElbow(PosT = Vector(60, 70, 80)). 

#  link(FlowAdapter()). \

MakeTest1(assembly)
