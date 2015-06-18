from nfluid.core.channel_element_2g import *
from nfluid.core.gates import *
#====================================================================
# Class of FlowAdapter
class FlowAdapter(ChannelElement2G):
#--------------------------------------------------------------------
  def __init__(self, \
    RH = None, RT = None, L = None, \
    PosH = None, PosT = None,    \
    Normal = None):

    ChannelElement2G.__init__(self)
    self.heads.append(GateCircle(self))
    self.tails.append(GateCircle(self))

    self.length = L
    self.set_normal_def(Normal)
    self.get_head_gate().set_pos_def(PosH)
    self.get_tail_gate().set_pos_def(PosT)
    self.get_head_gate().set_size_def(RH)
    self.get_tail_gate().set_size_def(RT)

#--------------------------------------------------------------------
  def get_name(self):
    return "FlowAdapter"

#--------------------------------------------------------------------
  def print_info(self):
    ChannelElement2G.print_info(self)
    print "FlowAdapter RHdef =", self.get_head_gate().get_r_def(), \
      "radiusTail RTdef=", self.get_tail_gate().get_r_def(), "length =", self.length, \
      "RH =", self.get_gate_size_h(), "RT =", self.get_gate_size_t() 
                                                        
