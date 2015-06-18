from channel_element_2g import *
from gates import *

#====================================================================
# Class of Coupling
class Coupling(ChannelElement2G):
#--------------------------------------------------------------------
  def __init__(self, R = None, L = None, \
      PosH = None, PosT = None,    \
      Normal = None):
    ChannelElement2G.__init__(self)
    self.length = L
    self.heads.append(GateCircle(self))
    self.tails.append(GateCircle(self))

    self.set_normal_def(Normal)
    self.get_head_gate().set_pos_def(PosH)
    self.get_tail_gate().set_pos_def(PosT)
    self.get_head_gate().set_size_def(R)
    self.get_tail_gate().set_size_def(R)

#--------------------------------------------------------------------
  def get_name(self):
    return "Coupling"

#--------------------------------------------------------------------
  def resolve_geometry_child(self):
    return self.set_equal_gate_size()

#--------------------------------------------------------------------
  def print_info(self):
    ChannelElement2G.print_info(self)
    print "Coupling radius Rdef =", self.get_head_gate().get_r_def(), "length =", self.length, \
      "RH =", self.get_gate_size_h(), "RT =", self.get_gate_size_t()


