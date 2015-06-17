from ChannelElement import *
from Gates import *
#====================================================================
class BifurcationCircle(ChannelElement):
#--------------------------------------------------------------------
  def __init__(self, R = None):
    ChannelElement.__init__(self)
    
    self.length = R

    self.heads.append(GateCircle(self))
    self.tails.append(GateCircle(self))
    self.tails.append(GateCircle(self))

    self.get_head_gate().set_size_def(R)
    self.get_tail_gate(0).set_size_def(R)
    self.get_tail_gate(1).set_size_def(R)
    
    """
    self.set_normal_def(Normal)
    self.get_head_gate().set_pos_def(PosH)
    self.get_tail_gate().set_pos_def(PosT)
    """
    
  def get_gate_size_h(self, n = 0):
    return self.get_head_gate().Size[n]

  def set_gate_size_h(self, s0, s1 = None, s2 = None, s3 = None):
    return self.get_head_gate().set_size_arg(s0, s1, s2, s3)

  """
  def get_gate_size_t(self, n = 0):
    return self.get_tail_gate().Size[n]

  def get_gate_size_tBif(self, n = 0):
    return self.get_tail_gate_bif().Size[n]

  def set_gate_size_t(self, s0, s1 = None, s2 = None, s3 = None):
    return self.get_tail_gate().set_size_arg(s0, s1, s2, s3)

  def set_gate_size_tBif(self, s0, s1 = None, s2 = None, s3 = None):
    return self.get_tail_gate_bif().set_size_argBif(s0, s1, s2, s3)
  """

#--------------------------------------------------------------------
  def resolve_geometry_base(self):
#--------------------------------------------------------------------
    ret = ""
    res = ChannelElement.resolve_geometry_base(self)
    if res == "":
      pass
    elif res == "ok":
      ret = "ok"
    else: 
      return res

#STUB!!!
    res = self.get_head_gate(0).set_normal(Vector(0, 0, 1))
    if res == "":
      pass
    elif res == "ok":
      ret = "ok"
    else: 
      return res

    res = self.get_tail_gate(0).set_normal(Vector(-1, 0, 0))
    if res == "":
      pass
    elif res == "ok":
      ret = "ok"
    else: 
      return res

    res = self.get_tail_gate(1).set_normal(Vector(1, 0, 0))
    if res == "":
      pass
    elif res == "ok":
      ret = "ok"
    else: 
      return res

    """
    NormalH = copy.copy(self.get_head_gate().Normal)
    res = self.get_tail_gate().set_normal(self.get_normal_tail_from_head(NormalH))
    if res == "":
      pass
    elif res == "ok":
      ret = "ok"
    else: 
      return res

    NormalT = copy.copy(self.get_tail_gate().Normal)
    res = self.get_head_gate().set_normal(self.get_normal_head_from_tail(NormalT))
    if res == "":
      pass
    elif res == "ok":
      ret = "ok"
    else:
      return res
    """

    PosT0 = copy.copy(self.get_head_gate().Pos)
    res = PosT0.add(Vector(-self.length, 0, -self.length))
    if res == "ok":
      res = self.get_tail_gate(0).set_pos(PosT0)
      if res == "":
        pass
      elif res == "ok":
        ret = "ok"
      else: 
        return res
    
    
    PosT1 = copy.copy(self.get_head_gate().Pos)
    res = PosT1.add(Vector(self.length, 0, -self.length))
    if res == "ok":
      res = self.get_tail_gate(1).set_pos(PosT1)
      if res == "":
        pass
      elif res == "ok":
        ret = "ok"
      else: 
        return res
    
    """
    PosH = copy.copy(self.get_head_gate().Pos)
#    print "XXX---------------"
#    PosH.print_info()
#    print "111---------------"
#    self.get_gates_diff().print_info()
#    print "222---------------"
    res = PosH.add(self.get_gates_diff())
#    PosH.print_info()
#    print "333--------------- res = ", res
    if res == "ok":
      res = self.get_tail_gate().set_pos(PosH)
      if res == "":
        pass
      elif res == "ok":
        ret = "ok"
      else: 
        return res

    PosT = copy.copy(self.get_tail_gate().Pos)
#    print "XXX---------------"
#    PosT.print_info()
#    self.get_gates_diff().print_info()
    res = PosT.sub(self.get_gates_diff())
#    PosT.print_info()
#    print "--------------- res = ", res
    if res == "ok":
      res = self.get_head_gate().set_pos(PosT)
      if res == "":
        pass
      elif res == "ok":
        ret = "ok"
      else: 
        return res
#    print "AAA---------------"
    self.get_head_gate().Pos.print_info()
    """
    
    return ret

"""
#--------------------------------------------------------------------
  def get_gates_diff(self):
#--------------------------------------------------------------------
    Normal = copy.copy(self.get_head_gate().Normal)
    print "get_gates_diff Normal"
    Normal.print_info()
    Len = Normal.get_len()
    print "get_gates_diff Len", Len, "self.length", self.length
    if Len is None or  Len == 0:
      print "get_gates_diff bad"
      return Vector()
    else:
      if self.length is None:
        x = None
        if is_equal_eps(Normal.x, 0):
          x = 0
        y = None
        if is_equal_eps(Normal.y, 0):
          y = 0
        z = None
        if is_equal_eps(Normal.z, 0):
          z = 0
        return Vector(x, y, z)
      else:
        Normal.scale(self.length / Len)
        print "get_gates_diff Normal Scaled"
        Normal.print_info()
        return Normal
#    return Vector(10, 20, self.length)

#--------------------------------------------------------------------
  def set_equal_gate_size(self):
#--------------------------------------------------------------------
    ret = ""
    SizeH = self.get_head_gate().Size
    res = self.get_tail_gate().set_size(SizeH)
    if res == "":
      pass
    elif res == "ok":
      ret = "ok"
    else:
      return res

    SizeT = self.get_tail_gate().Size
    res = self.get_head_gate().set_size(SizeT)
    if res == "":
      pass
    elif res == "ok":
      ret = "ok"
    else:
      return res

    return ret

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
    if self.length is not None:
      return self.length
    else:
      DifPos = copy.copy(self.get_head_gate().Pos)
      DifPos.sub(self.get_tail_gate().Pos)
      return DifPos.get_len()

#--------------------------------------------------------------------
  def print_info(self):
    ChannelElement.print_info(self)
    print "Len = ", self.get_len()
"""


