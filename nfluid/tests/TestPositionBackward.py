from channel_assembly import *
from flow_adapter import *
from circle_coupling import *
from elbow import *
from TestBase import *
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

