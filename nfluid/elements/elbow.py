from nfluid.core.channel_element_2g import *
from nfluid.core.gates import *

#====================================================================
# Class of Elbow
class Elbow(ChannelElement2G):
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
    return "Elbow"

#--------------------------------------------------------------------
  def get_r(self):
    return self.get_head_gate().get_r()

#--------------------------------------------------------------------
  def resolve_geometry_child(self):
    return self.set_equal_gate_size()

#--------------------------------------------------------------------
  def get_gates_diff(self):
    return Vector(0, 3000, 4000)

#--------------------------------------------------------------------
  def get_normal_tail_from_head(self, NormalH):
    return Vector(1, 0, 0)

#--------------------------------------------------------------------
  def get_normal_head_from_tail(self, NormalT):
    return Vector(0, 0, 1)

#--------------------------------------------------------------------
  def print_info(self):
    ChannelElement2G.print_info(self)
    print "Coupling radius Rdef =", self.get_head_gate().get_r_def(), "length =", self.length, \
      "RH =", self.get_gate_size_h(), "RT =", self.get_gate_size_t() 

#--------------------------------------------------------------------
  """
  def create_shape(self):
    # check geometry data
    self.shape = STLCircleCoupling(self.get_rh(), self.get_len()) 
    print "create_shape FlowAdapter"
    return ""
  """
 
