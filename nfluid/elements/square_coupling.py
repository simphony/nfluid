from channel_element_2g import *
from gates import *
#====================================================================
# Class of CouplingSquare
class CouplingSquare(ChannelElement2G):
#--------------------------------------------------------------------
  def __init__(self, A = None, B = None, L = None, \
      PosH = None, PosT = None,    \
      Normal = None):
    ChannelElement2G.__init__(self)
    self.length = L
    self.heads.append(GateRect(self))
    self.tails.append(GateRect(self))

    self.set_normal_def(Normal)
    self.get_head_gate().set_pos_def(PosH)
    self.get_tail_gate().set_pos_def(PosT)
    self.get_head_gate().set_size_def(A, B)
    self.get_tail_gate().set_size_def(A, B)

#--------------------------------------------------------------------
  def get_name(self):
    return "CouplingSquare"

#--------------------------------------------------------------------
  def resolve_geometry_child(self):
    return self.set_equal_gate_size()

#--------------------------------------------------------------------
  def print_info(self):
    ChannelElement2G.print_info(self)
    print "CouplingSquare AHdef =", self.get_head_gate().get_a_def(), \
      " BHdef =", self.get_head_gate().get_b_def(),           \
      "length =", self.length, \
      " AH =", self.get_gate_size_h(), "AT =", self.get_gate_size_t() 


