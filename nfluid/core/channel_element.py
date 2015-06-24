from nfluid.core.gate_base import * 
from nfluid.shapes.shapes import * 


#==============================================================================
#Base class of Channel Elements
class ChannelElement(object):
#--------------------------------------------------------------------
  assembly = None;

  def __init__(self):
    ChannelElement.assembly.add_element(self)
    self.heads = []
    self.tails = []
    self.changed = True
    self.shape = None

#--------------------------------------------------------------------
  def get_name(self):
    return "ChannelElement"

#--------------------------------------------------------------------
  def get_head_gate(self, n = 0):
    return self.heads[n]

#--------------------------------------------------------------------
  def get_tail_gate(self, n = 0):
    return self.tails[n]

#--------------------------------------------------------------------
  def get_next_element(self, n = 0):
    gt = self.get_tail_gate(n)
    if gt is None:
      return None
    gtb = gt.buddy
    if gtb is None:
      return None
    return gtb.element

#--------------------------------------------------------------------
  def get_prev_element(self, n = 0):
    gh = self.get_head_gate(n)
    if gh is None:
      return None
    ghb = gh.buddy
    if ghb is None:
      return None
    return ghb.element

#--------------------------------------------------------------------
  def link(self, next, gateTail = 0, gateHead = 0):
    gt1 = self.get_tail_gate(gateTail)
    gh2 = next.get_head_gate(gateHead)
    gt1.buddy = gh2
    gh2.buddy = gt1
    return next

#--------------------------------------------------------------------
  def print_info(self):
    self.for_each_gate(fcn_print_info_xxx)
#    print "ChannelElement"

#--------------------------------------------------------------------  
  def print_info_channel(self):
    self.print_info()
    next = self.get_next_element()
    if next is not None:
      next.print_info_channel()

#--------------------------------------------------------------------
# "" nothing changed
# "ok" something changed
# "other text" - fatal error
  def resolve_geometry(self):
#--------------------------------------------------------------------
    ret = ""
    res = self.resolve_geometry_base()
    print "Tail gate res = ", res
    if res == "":
      pass
    elif res == "ok":
      ret = "ok"
    else:
      return res

    res = self.resolve_geometry_child()
    print "Tail gate res = ", res
    if res == "":
      pass
    elif res == "ok":
      ret = "ok"
    else:
      return res

    return ret

#--------------------------------------------------------------------
  def resolve_geometry_child(self):
    return ""

#--------------------------------------------------------------------
# "" nothing changed
# "ok" something changed
# "other text" - fatal error
  def resolve_geometry_base(self):
#--------------------------------------------------------------------
    ret = ""
    for gate in self.heads:
      res = gate.resolve_geometry()
      print "Head gate res = ", res
      if res == "":
        pass
      elif res == "ok":
        ret = "ok"
      else:
        return res 

    for gate in self.tails:
      res = gate.resolve_geometry()
      print "Tail gate res = ", res
      if res == "":
        pass
      elif res == "ok":
        ret = "ok"
      else:
        return res

      return ret

#--------------------------------------------------------------------
  def is_resolved_geometry(self):
    msg = "xxx"
    for gate in self.heads:
      res = gate.is_resolved_geometry()
      if res != "":
        return msg + res
    for gate in self.tails:
      res = gate.is_resolved_geometry()
      if res != "":
        return msg + res
    return ""

#--------------------------------------------------------------------
#  @staticmethod
  def fcn_clear_geometry(gate):
    gate.clear_geometry()

#--------------------------------------------------------------------
  def clear_geometry(self):
    self.for_each_gate(fcn_clear_geometry_xxx)
#    self.for_each_gate(ChannelElement.fcn_clear_geometry)

#--------------------------------------------------------------------
  def for_each_gate(self, fcn):
    for gate in self.heads:
      fcn(gate)
    for gate in self.tails:
      fcn(gate)

#--------------------------------------------------------------------
  def create_shape(self):
#    self.shape = ShapeSTL() #Real shapes in derived classes
#    print "create_shape"
    return ""

#--------------------------------------------------------------------
  def release_shape(self):
    print "release_shape"
    self.shape = None

#--------------------------------------------------------------------
  def export(self, file):
#    print "export"
    if self.shape is not None:
      self.shape.export(file) 

#--------------------------------------------------------------------
  def show_shape(self):
#    print "show_shape"
    if self.shape is not None:
      self.shape.show()


#--------------------------------------------------------------------
def fcn_clear_geometry_xxx(gate):
    gate.clear_geometry()

#--------------------------------------------------------------------
def fcn_print_info_xxx(gate):
    gate.print_info()

