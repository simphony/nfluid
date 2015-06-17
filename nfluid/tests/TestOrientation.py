from NF_ChannelAssembly import *
from NF_Cone import *
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
    Normal = NF_Vector(1, 0, 0) 
    ) 
  ). \
  link(NF_Cone(L = 20)). \
  link(NF_Cylinder(25, L = 125)).  \
  link(NF_Cone(L = 20)). \
  link(NF_Cylinder(30, L = 200))


MakeTest1(assembly)



