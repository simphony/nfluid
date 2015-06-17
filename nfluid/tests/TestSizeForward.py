from NF_ChannelAssembly import *
from NF_Cone import *
from NF_Cylinder import *
from NF_CylinderCurve import *
from TestBase import *
import os

print os.path.basename(__file__), "------------------------\n"

assembly = NF_ChannelAssembly()


CreateChannel( 
    NF_Cylinder(111, 78, 
    PosH = NF_Vector(11, 22, 33), 
    Normal = NF_Vector(0, 0, 1) 
    ) 
  ). \
  link(NF_Cone(RT = 222, L = 15)). \
  link(NF_Cylinder(L = 125)).  \
  link(NF_Cone(RT =123, L = 20)). \
  link(NF_Cylinder(L = 200))

#  link(NF_Cone(RT =123, L = 30)). \
#  link(NF_Cylinder(L = 20)). \

MakeTest1(assembly)

