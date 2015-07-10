from nfluid.core.channel_element_2g import *
from nfluid.core.gates import *

#====================================================================
# Class of Coupling                                       
class Coupling(ChannelElement2G):
#--------------------------------------------------------------------
  def __init__(self, R = None, L = None, \
      PosH = None, PosT = None,
      Normal = None):
    ChannelElement2G.__init__(self)

    self.IsEqualGateSize = True

    self.length = L
    self.IsAxialSym = True
    self.heads.append(GateCircle(self))
    self.tails.append(GateCircle(self))

    self.set_normal_def(Normal)
    self.get_head_gate().set_pos_def(PosH)
    self.get_tail_gate().set_pos_def(PosT)
    self.get_head_gate().set_size_def(R)
    self.get_tail_gate().set_size_def(R)

# Initial position along Z
    self.get_head_gate().NormalElement = Vector(0, 0, 1)
    self.get_tail_gate().NormalElement = Vector(0, 0, 1)

#--------------------------------------------------------------------
  def get_name(self):
    return "Coupling"

#--------------------------------------------------------------------
  def get_r(self):
    return self.get_head_gate().get_r()

#--------------------------------------------------------------------
  def resolve_geometry_child(self):
    if self.get_len() is not None: 
      self.get_head_gate().PosElement = Vector(0, 0, - self.get_len() / 2.0)
      self.get_tail_gate().PosElement = Vector(0, 0, self.get_len() / 2.0)

    return ""

#--------------------------------------------------------------------
  def print_info(self):
    ChannelElement2G.print_info(self)
    print "Coupling radius Rdef =", self.get_head_gate().get_r_def(), "length =", self.length, \
      "RH =", self.get_gate_size_h(), "RT =", self.get_gate_size_t(),  \
      "PosH =", self.get_head_gate().Pos, "PosT =", self.get_pos_tail() 

#--------------------------------------------------------------------
  def create_shape(self):
    # check geometry data
    self.shape = ShapeCircleCoupling(self.get_r(), self.get_len(), self.get_pos_head(), \
    self.get_pos_tail()) 
    print "create_shape Coupling"
    return ""

