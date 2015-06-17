from NF_ChannelAssembly import *
from NF_Cone import *
from NF_Cylinder import *
from NF_CylinderCurve import *
from TestBase import *
import os

print os.path.basename(__file__), "------------------------\n"

assembly = NF_ChannelAssembly()

CreateChannel( 
    NF_Cylinder(L = 78,  
#    Normal = NF_Vector(0, 0, 1) 
    ) 
  ). \
  link(NF_Cone(RH = 22, L = 15)). \
  link(NF_Cylinder(L = 125)).  \
  link(NF_Cone(RH =12, L = 20)). \
  link(NF_Cylinder(88, 20, PosT = NF_Vector(11, 22, 800)))


MakeTest1(assembly)

