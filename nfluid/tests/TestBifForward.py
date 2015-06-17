from NF_ChannelAssembly import *
from NF_Cone import *
from NF_Cylinder import *
from NF_BifurcationCircle import *
from TestBase import *

import os

print os.path.basename(__file__), "------------------------\n"

assembly = NF_ChannelAssembly()


bif = CreateChannel( 
    NF_Cylinder(111, 78, 
    PosH = NF_Vector(11, 22, 33), 
    Normal = NF_Vector(0, 0, 1) 
    ) 
  ). \
  link(NF_Cone(RT = 220, L = 15)). \
  link(NF_Cylinder(L = 125)).  \
  link(NF_BifurcationCircle(220)) 

#
bif. \
  link(NF_Cone(RT =123, L = 20)). \
  link(NF_Cylinder(L = 200))


bif. \
  link(NF_Cone(RT =150, L = 20), 1). \
  link(NF_Cylinder(L = 200))

MakeTest1(assembly)

