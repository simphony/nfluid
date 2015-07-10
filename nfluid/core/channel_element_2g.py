from nfluid.core.channel_element import *

#====================================================================
class ChannelElement2G(ChannelElement):
#--------------------------------------------------------------------
  def __init__(self):
    ChannelElement.__init__(self)
    self.length = None

  def get_gate_size_h(self, n = 0):
    return self.get_head_gate().Size[n]

  def set_gate_size_h(self, s0, s1 = None, s2 = None, s3 = None):
    return self.get_head_gate().set_size_arg(s0, s1, s2, s3)

  def get_gate_size_t(self, n = 0):
    return self.get_tail_gate().Size[n]

  def set_gate_size_t(self, s0, s1 = None, s2 = None, s3 = None):
    return self.get_tail_gate().set_size_arg(s0, s1, s2, s3)

#--------------------------------------------------------------------
  def get_pos_tail(self):
    return self.get_tail_gate().Pos

#--------------------------------------------------------------------
  def get_normal_head(self):
    return self.get_head_gate().Normal

#--------------------------------------------------------------------
  def get_normal_tail(self):
    return self.get_tail_gate().Normal

#--------------------------------------------------------------------
  def get_gates_diff_real(self):
#--------------------------------------------------------------------
    diff = copy.copy(self.get_pos_tail())
    diff.sub(self.get_pos_head())
    return diff

#--------------------------------------------------------------------
  def set_normal_def(self, NormalDef):
    self.get_head_gate().set_normal_def(NormalDef)
    self.get_tail_gate().set_normal_def(NormalDef)

#--------------------------------------------------------------------
  def get_normal_tail_from_head(self, NormalH):
    return NormalH

#--------------------------------------------------------------------
  def get_normal_head_from_tail(self, NormalT):
    return NormalT

#--------------------------------------------------------------------
  def get_len(self):
#--------------------------------------------------------------------
    if self.length is not None:
      return self.length
    else:
      DifPos = self.get_head_gate().Pos - self.get_tail_gate().Pos
      return DifPos.get_len()

#--------------------------------------------------------------------
  def print_info(self): #  replace with __str__ ?
    ChannelElement.print_info(self)
    print "Len = ", self.get_len()
