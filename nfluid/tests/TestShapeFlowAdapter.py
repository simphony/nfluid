from nfluid.core.channel_assembly import *
from nfluid.elements.circle_coupling import *
from nfluid.elements.flow_adapter import *
from nfluid.tests.TestBase import *
import os

print os.path.basename(__file__), "------------------------\n"

assembly = ChannelAssembly()


last = create_channel( 
    Coupling(10, 20, 
    PosH = Vector(0, 20, 30), 
    Normal = Vector(0, 0, 1) 
    ) 
#  ) 
  ). \
  link(FlowAdapter(L = 15)). \
  link (Coupling(45, L = 125))

#  link(FlowAdapter(L = 50, PosT = Vector(0, 70, 100))). \


#MakeTest1(assembly)

print "-----------------------------"
el1 = assembly.get_element_by_id(1)
"""
if el1 is not None:
  print "get_element_by_id ", el1.print_info()

gates_t, gates_h = el1.detach()
if el1 is not None:
  print "gates_t, gates_h ", gates_t, gates_h
"""

#if el1 is not None:
#  assembly.delete_element(el1)

new_elt = Coupling(L = 125)
#el1.insert_before(new_elt)

assembly.insert_element_before(new_elt, el1)

MakeTest1(assembly)

print last.get_chain_str()
print el1.get_chain_str()
 