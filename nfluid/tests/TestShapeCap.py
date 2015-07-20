from nfluid.core.channel_assembly import *
from nfluid.elements.circle_coupling import *
from nfluid.elements.cap import *
from nfluid.tests.TestBase import *
import os
import sys

print os.path.basename(__file__), "------------------------\n"

if len(sys.argv) == 1:
  print "0: "
  exit(0)

assembly = ChannelAssembly()

if sys.argv[1] == "0":
  print "Test Cap 0"

  create_channel( 
      Coupling(10, 20, 
      PosH = Vector(0, 27, 35), 
      Normal = Vector(0, 0, 1) 
      ) 
    ). \
    link(Cap(L = 5))
  
else:
  print "Incorrect argument value"
  exit(0)

MakeTest1(assembly)
 
