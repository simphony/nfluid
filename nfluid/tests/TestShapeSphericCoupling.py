from nfluid.core.channel_assembly import *
from nfluid.elements.circle_coupling import *
from nfluid.elements.spheric_coupling import *
from nfluid.tests.TestBase import *
import os

print os.path.basename(__file__), "------------------------\n"

assembly = ChannelAssembly()


create_channel( 
    Coupling(10, 20, 
    PosH = Vector(0, 20, 30), 
    Normal = Vector(0, 0, 1) 
    ) 
  ). \
  link(SphericCoupling(R = 10, RS = 50))
 
#  link (Coupling(L = 125))


#  link(SphericCoupling(RS = 50, NormalT = Vector(1, 0, 0))). \

MakeTest1(assembly)
