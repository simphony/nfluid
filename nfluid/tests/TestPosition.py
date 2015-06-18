from channel_assembly import *
from flow_adapter import *
from circle_coupling import *
from elbow import *
from TestBase import *
import os

print os.path.basename(__file__), "------------------------\n"

assembly = ChannelAssembly()


create_channel( 
    Coupling(111, 78, 
    PosH = Vector(11, 22, 33), 
    Normal = Vector(0, 0, 1) 
    ) 
  ). \
  link(FlowAdapter(L = 20)). \
  link(Coupling(25, L = 125)).  \
  link(FlowAdapter(L = 20)). \
  link(Coupling(30, L = 200))

#  link(FlowAdapter(RT =123, L = 30)). \
#  link(Coupling(L = 20)). \

MakeTest1(assembly)

