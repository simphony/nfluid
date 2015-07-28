import os
import sys
from nfluid.core.channel_assembly import *
from nfluid.elements.circle_coupling import *
from nfluid.elements.flow_adapter import *
from nfluid.elements.short_elbow import *
from nfluid.elements.cap import *
from nfluid.tests.TestBase import *

print os.path.basename(__file__), "------------------------\n"

if len(sys.argv) == 1:
    print "0: Coupling, Normal z, Cap"
    print "1: Coupling, Normal x, Cap"
    print "2: Coupling, Cap"
    print "3: Coupling, Cap"
    exit(0)

n_tests = 4

assembly = ChannelAssembly()

if sys.argv[1] == "0":
    print "Test Cap 0"

    last = create_channel(Coupling(R=10, L=20, PosH=Vector(0, 27, 35),
                          Normal=Vector(0, 0, 1))
    ). \
        link(Cap(L=5))

elif sys.argv[1] == "1":
    print "Test Cap 1"

    last = create_channel(Coupling(R=10, L=20, PosH=Vector(0, 27, 35),
                          Normal=Vector(1, 0, 0))
    ). \
        link(Cap(L=5))

elif sys.argv[1] == "2":
    print "Test Cap 2"

elif sys.argv[1] == "3":
    print "Test Cap 3"

else:
    print "Incorrect argument value"
    exit(0)

elif sys.argv[1] == "*":
    for i in range(0, n_tests):
        os.system("TestShapeCap.py " + str(i))
    exit(0)

MakeTest1(assembly)

"""
print "-----------------------------"
el1 = assembly.get_element_by_id(1)

if el1 is not None:
  print "get_element_by_id ", el1.print_info()


gates_t, gates_h = el1.detach()
if el1 is not None:
  print "gates_t, gates_h ", gates_t, gates_h


#if el1 is not None:
#  assembly.delete_element(el1)

new_elt = Coupling(L = 125)
#el1.insert_before(new_elt)

assembly.insert_element_before(new_elt, el1)

MakeTest1(assembly)

#print last.get_chain_str()
#print el1.get_chain_str()

"""
