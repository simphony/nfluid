from nfluid.core.channel_assembly import *
from nfluid.elements.flow_adapter import *
from nfluid.elements.circle_coupling import *
from nfluid.tests.TestBase import *
import os
import sys

print os.path.basename(__file__), "------------------------\n"

if len(sys.argv) == 1:
  print "0: Normal - forward, Pos - backward"
  print "1: Normal - forward, Pos - backward"
  exit(0)

n_tests = 3

assembly = ChannelAssembly()


#print "sys.argv ", sys.argv
#print "len(sys.argv) ", len(sys.argv)

if sys.argv[1] == "0":
#  Test_0
  print "Test Normal - forward, Pos - backward"
  create_channel(
      Coupling(R = 10, L = 45,
      PosH = Vector(0, 20, 30),
      Normal = Vector(1, 0, 0)
      )
    
    ). \
    link (Coupling(PosT = Vector(400, 20, 0)))

elif sys.argv[1] == "1":
#  Test_1
  print "Test_1"
  print "Test Two positions, Pos - backward"
  create_channel(
      Coupling(R = 10,
      PosH = Vector(0, 20, 30),
      PosT = Vector(0, 20, 150)
      )

    ). \
    link (Coupling(PosT = Vector(0, 20, 400)))

elif sys.argv[1] == "2":
#  Test_2
  print "Test_2"


elif sys.argv[1] == "*":
  for i in range(0, n_tests):
    os.system("TestShapeCircleCoupling.py " + str(i))
  exit(0)

else:
  print "Incorrect argument value"
  exit(0)




"""
create_channel( 
    Coupling(R = 10, 
    PosH = Vector(0, 20, 30),
    PosT = Vector(0, 20, 150)  
    ) 
 
  ). \
  link (Coupling(PosT = Vector(0, 20, 400)))
"""
#    Normal = Vector(1, 0, 0) 
#  link (Coupling(L = 125) )
#  link (Coupling(PosH = Vector(0, 20, 50), PosT = Vector(0, 20, 400)) )


MakeTest1(assembly)


