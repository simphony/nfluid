from nfluid.core.channel_assembly import *
#from nfluid.elements.flow_adapter import *
from nfluid.elements.circle_coupling import *
from nfluid.elements.long_elbow import *
from nfluid.tests.TestBase import *
import os

print os.path.basename(__file__), "------------------------\n"

assembly = ChannelAssembly()

NormalH0 = Vector(0, 0, 100)

print "%%%%%%%%%%%%%%", NormalH0 

create_channel( 
    Coupling(10, 15, 
    PosH = Vector(0, 77, 130), 
    Normal = Vector(0, 0, 1) 
    ) 
#  ) 
  ). \
  link(LongElbow(RC = 50, PosT = Vector(0, 127.0, 195.0))).  \
  link (Coupling(L = 125)). \
  link(LongElbow(RC = 50, NormalT = Vector(1, 0, 0))).  \
  link (Coupling(L = 122))

#  link(LongElbow(RC = 50, NormalH = Vector(0, 0, 1), NormalT = Vector(0, 1, 0))).  \
#  link(LongElbow(RC = 50, NormalT = Vector(1, 0, 0))).  \
#  link(LongElbow(RC = 50, PosT = Vector(50, 20, 100))).  \

print "%%%%%%%%%%%%%%", NormalH0
 
"""
create_channel( 
    Coupling(10, 20, 
    PosH = Vector(0, 20, 30), 
    Normal = Vector(0, 0, 1) 
    ) 
#  ) 
  ). \
  link(LongElbow(RC = 50, NormalT = Vector(0, 1, 0))). \
  link(LongElbow(RC = 50, NormalT = Vector(1, 0, 0))). \
  link (Coupling(L = 100))

"""

print "%%%%%%%%%%%%%%", NormalH0 


#  link(LongElbow(RC = 50, NormalH = Vector(0, 0, 1), PosT = Vector(0, 70, 100))). \
#  link(LongElbow(RC = 50, NormalT = Vector(0, 1, 0))). \
#  link(LongElbow(RC = 50, R= 10, NormalH = Vector(0, 0, 1), NormalT = Vector(1, 0, 0))). \
#  link(LongElbow(RC = 50, NormalH = NormalH0, PosT = Vector(0, 70, 100))). \

#  link(LongElbow(RC = 50, PosT = Vector(50, 20, 100))).  \

MakeTest1(assembly)


PosH = Vector(1, 0, 0) 
Normal = Vector(5, 5, 0) 
angle = get_vector_angle_grad(PosH, Normal)
print "angle = ", angle
