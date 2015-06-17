from ChannelAssembly import *
from FlowAdapter import *
from Coupling import *
from Elbow import *
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
  link(FlowAdapter(RT = 222, L = 15)). \
  link(Coupling(L = 125)).  \
  link(FlowAdapter(RT =123, L = 20)). \
  link(Coupling(L = 200))

#  link(FlowAdapter(RT =123, L = 30)). \
#  link(Coupling(L = 20)). \

MakeTest1(assembly)

