from nfluid.core.channel_element import *
from nfluid.core.gates import *
#====================================================================
class TeeCircle4(ChannelElement):
#--------------------------------------------------------------------
  def __init__(self, R = None,     \
      PosH = None, PosT0 = None, PosT1 = None, PosT2 = None, PosT3 = None, \
      NormalH = None, NormalT0 = None, NormalT1 = None, NormalT2 = None, NormalT3 = None):

# NormalH, NormalT0 must be orthogonal
# NormalT should be corrected to respect that

    ChannelElement.__init__(self)
    
    self.IsEqualGateSize = True

    self.length = R

    self.heads.append(GateCircle(self))
    self.tails.append(GateCircle(self))
    self.tails.append(GateCircle(self))
    self.tails.append(GateCircle(self))
    self.tails.append(GateCircle(self))

    self.get_head_gate().set_size_def(R)
    self.get_tail_gate(0).set_size_def(R)
    self.get_tail_gate(1).set_size_def(R)
    self.get_tail_gate(2).set_size_def(R)
    self.get_tail_gate(3).set_size_def(R)

    self.get_head_gate().set_pos_def(PosH)
    self.get_tail_gate(0).set_pos_def(PosT0)
    self.get_tail_gate(1).set_pos_def(PosT1)
    self.get_tail_gate(2).set_pos_def(PosT2)
    self.get_tail_gate(3).set_pos_def(PosT3)
    
    self.get_head_gate().set_normal_def(NormalH)
    self.get_tail_gate(0).set_normal_def(NormalT0)
    self.get_tail_gate(1).set_normal_def(NormalT1)
    self.get_tail_gate(2).set_normal_def(NormalT2)
    self.get_tail_gate(3).set_normal_def(NormalT3)

# Initial position along Z and X
    self.get_head_gate().NormalElement = Vector(0, 0, 1)
    self.get_tail_gate(0).NormalElement = Vector(1, 0, 0)
    self.get_tail_gate(1).NormalElement = Vector(-1, 0, 0)
    self.get_tail_gate(2).NormalElement = Vector(0, 1, 0)
    self.get_tail_gate(3).NormalElement = Vector(0, -1, 0)
    
#--------------------------------------------------------------------
  def get_name(self):
    return "TeeCircle4"

#--------------------------------------------------------------------
  def get_gate_size_h(self, n = 0):
    return self.get_head_gate().Size[n]

#--------------------------------------------------------------------
  def set_gate_size_h(self, s0, s1 = None, s2 = None, s3 = None):
    return self.get_head_gate().set_size_arg(s0, s1, s2, s3)

#--------------------------------------------------------------------
  def get_r(self):
    return self.get_head_gate().get_r()

#--------------------------------------------------------------------
  def resolve_geometry_child(self):
#--------------------------------------------------------------------
    R = self.get_r()
    if R is not None:
      self.get_head_gate().PosElement = Vector(0, 0, - R)
      self.get_tail_gate(0).PosElement = Vector(R, 0, 0)
      self.get_tail_gate(1).PosElement = Vector(-R, 0, 0)
      self.get_tail_gate(2).PosElement = Vector(0, R, 0)
      self.get_tail_gate(3).PosElement = Vector(0, -R, 0)

    return ""


    

