from nfluid.core.channel_element_2g import *
from nfluid.core.gates import *

#====================================================================
# Class of Cap
class Cap(ChannelElement):
#--------------------------------------------------------------------
  def __init__(self, L, R = None,  \
      PosH = None, NormalH = None):
    ChannelElement.__init__(self)

    self.length = L 

    self.heads.append(GateCircle(self))

    self.alpha = 90 # Could vary in future


    self.get_head_gate().set_normal_def(NormalH) 

    self.get_head_gate().set_pos_def(PosH)

    self.get_head_gate().set_size_def(R)

#--------------------------------------------------------------------
  def get_name(self):
    return "Cap"

#--------------------------------------------------------------------
  def get_r(self):
    return self.get_head_gate().get_r()

#--------------------------------------------------------------------
  def resolve_geometry_child(self):
    if self.get_r() is None:
      return "" 
    if self.get_r() < self.length:
      return "Incorrect Cup length"
    else:
      return ""

#--------------------------------------------------------------------
  def print_info(self):
    ChannelElement.print_info(self)
    print "Cap radius Rdef =", self.get_head_gate().get_r_def(), \
      "R =", self.get_head_gate().get_r() 

#--------------------------------------------------------------------
  def create_shape(self):
    # check geometry data
    self.shape = ShapeCap(self.get_head_gate().get_r(), self.length, 0) 
#    self.shape = ShapeCap(self.get_head_gate().get_r(), self.length, self.get_pos_head()) 
    print "create_shape Cap"
    return ""

 
