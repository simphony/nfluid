from nfluid.core.channel_element_2g import *
from nfluid.core.gates import *

#====================================================================
# Class of Elbow
class ShortElbow(ChannelElement2G):
#--------------------------------------------------------------------
  def __init__(self, R = None,  \
      PosH = None, PosT = None, \
      NormalH = None, NormalT = None):
    ChannelElement2G.__init__(self)
    self.heads.append(GateCircle(self))
    self.tails.append(GateCircle(self))

    self.angle = 90 # Could vary in future

# TODO Correct NormalT if both NormalH and NormalT are defined
    self.get_head_gate().set_normal_def(NormalH) 
    self.get_tail_gate().set_normal_def(NormalT)

    self.get_head_gate().set_pos_def(PosH)
    self.get_tail_gate().set_pos_def(PosT)

    self.get_head_gate().set_size_def(R)
    self.get_tail_gate().set_size_def(R)

#--------------------------------------------------------------------
  def get_name(self):
    return "ShortElbow"

#--------------------------------------------------------------------
  def get_r(self):
    return self.get_head_gate().get_r()

#--------------------------------------------------------------------
  def get_r_curv(self):
    return self.get_head_gate().get_r()

#--------------------------------------------------------------------
  def resolve_geometry_child(self):
#--------------------------------------------------------------------
    print "zzzzzzzzzzzzzzzzzz++++++++ 1"
    if self.get_normal_head().is_not_none() and self.get_normal_tail().is_not_none():
      angle = get_vector_angle(self.get_normal_head(), self.get_normal_tail())
      print "resolve_geometry_child angle = ", angle
      if not is_equal_eps(angle, self.angle):
        print "Incorrect angle = "
        return "Incorrect angle in ShortElbow"

    return self.set_equal_gate_size()

#--------------------------------------------------------------------
  def get_gates_diff(self):
#--------------------------------------------------------------------
    if self.get_normal_head() is not None \
      and self.get_normal_tail() is not None \
      and self.get_r_curv() is not None:
#    NormalH = copy.copy(self.get_head_gate().Normal)
      # Only for 90 degree
      print "======= get_gates_diff A", self.get_r_curv(), self.get_normal_head(), self.get_normal_tail()
      print "======= get_gates_diff Curv", self.get_r_curv()
      DiffH = self.get_normal_head() * self.get_r_curv()
      DiffT = self.get_normal_tail() * self.get_r_curv()
      print "======= get_gates_diff B", DiffH, DiffT, DiffH + DiffT
      return DiffH + DiffT
    else:
      print "======= get_gates_diff None"
#      return Vector()  
      return None  

#--------------------------------------------------------------------
  def get_normal_tail_from_head(self, NormalH):
#--------------------------------------------------------------------
    # Head Normal and tail pos
    print "++++++++ 1", NormalH, self.get_normal_tail()
    if self.get_normal_tail().is_none():
      print "++++++++ 2"
      if NormalH.is_not_none():
        print "++++++++ 3"
        diff = self.get_gates_diff_real()
        if diff.is_not_none():
          print "++++++++ 4 diff = ", diff
          Normal = diff - self.get_normal_head() * self.get_r_curv()
          Normal.normalize()
          print "+++++++++++++++ Normal", Normal
          return Normal
    return None

#--------------------------------------------------------------------
  def get_normal_head_from_tail(self, NormalT):
#--------------------------------------------------------------------
    # Tail Normal and head pos
    print "-------- 1", NormalT, self.get_normal_head()
    if self.get_normal_head().is_none():
      print "-------- 2"
      if NormalT.is_not_none:
        diff = self.get_gates_diff_real()
        print "-------- diff = ", diff
        if diff.is_not_none():
          print "-------- 4"
          Normal = diff - self.get_normal_tail() * self.get_r_curv()
          Normal.normalize()
          print "--------------- Normal", Normal
          return Normal

    return None

#--------------------------------------------------------------------
  def print_info(self):
    ChannelElement2G.print_info(self)
    print "ShortElbow radius Rdef =", self.get_head_gate().get_r_def(), \
      "RH =", self.get_gate_size_h(), "RT =", self.get_gate_size_t(), \
      "PosH =", self.get_pos_head(), "PosT =", self.get_pos_tail()  

#--------------------------------------------------------------------
  def create_shape(self):
    # check geometry data
    self.shape = ShapeShortElbow(self.get_r(), self.get_pos_head(), self.get_pos_tail()) 
    print "create_shape ShortElbow"
    return ""

 
