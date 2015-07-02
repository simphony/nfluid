from nfluid.core.channel_element_2g import *
from nfluid.core.gates import *

#====================================================================
# Class of SphericCoupling
class SphericCoupling(ChannelElement2G):
#--------------------------------------------------------------------
  def __init__(self, RS, R = None,  \
      PosH = None, PosT = None, \
      NormalH = None, NormalT = None):
    ChannelElement2G.__init__(self)

    self.heads.append(GateCircle(self))
    self.tails.append(GateCircle(self))

    self.RadiusSphere = RS

    self.get_head_gate().set_normal_def(NormalH) 
    self.get_tail_gate().set_normal_def(NormalT)

    self.get_head_gate().set_pos_def(PosH)
    self.get_tail_gate().set_pos_def(PosT)

    self.get_head_gate().set_size_def(R)
    self.get_tail_gate().set_size_def(R)

#--------------------------------------------------------------------
  def get_name(self):
    return "SphericCoupling"

#--------------------------------------------------------------------
  def get_r(self):
    return self.get_head_gate().get_r()

#--------------------------------------------------------------------
  def resolve_geometry_child(self):
    return self.set_equal_gate_size()

#--------------------------------------------------------------------
  def print_info(self):
    ChannelElement2G.print_info(self)
    print "SphericCoupling radius Rdef =", self.get_head_gate().get_r_def(), \
      "RH =", self.get_gate_size_h(), "RT =", self.get_gate_size_t(), \
      "RadiusSphere =", self.RadiusSphere, \
      "PosH = ", self.get_pos_head(), "PosT =", self.get_pos_tail()  

#--------------------------------------------------------------------
  def create_shape(self):
    # check geometry data
    self.shape = ShapeSphericCoupling(self.RadiusSphere, self.get_r(),  \
    self.get_pos_head(), self.get_pos_tail()) 
    print "create_shape SphericCoupling"
    return ""

 
