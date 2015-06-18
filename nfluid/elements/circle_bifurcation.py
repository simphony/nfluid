from nfluid.core.channel_element import *
from nfluid.core.gates import *
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


