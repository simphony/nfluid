from NF_ChannelAssembly import *
from NF_Cone import *
from NF_Cylinder import *
from NF_CylinderCurve import *
from TestBase import *
from NF_Bar import *
import os

print os.path.basename(__file__), "------------------------\n"

assembly = NF_ChannelAssembly()


CreateChannel( 
    NF_Bar(111, 27, 78, 
    PosH = NF_Vector(11, 22, 33), 
    Normal = NF_Vector(0, 0, 1) 
    ) 
  ). \
  link(NF_Bar(L = 20)). \
  link(NF_Bar(L = 125))

MakeTest1(assembly)

