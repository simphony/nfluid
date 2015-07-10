from nfluid.core.gate_base import * 
from nfluid.shapes.shapes import * 
#from nfluid.util.operator import *
from nfluid.util.rotations import *


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

    self.IsAxialSym = False
    self.IsEqualGateSize = False

    self.RotationOperator = None
    self.CenterPos = None

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
  def get_pos_head(self):
    return self.get_head_gate().Pos

#--------------------------------------------------------------------
  def get_next_element(self, n = 0):
#--------------------------------------------------------------------
    gt = self.get_tail_gate(n)
    if gt is None:
      return None
    gtb = gt.buddy
    if gtb is None:
      return None
    return gtb.element

#--------------------------------------------------------------------
  def get_prev_element(self, n = 0):
#--------------------------------------------------------------------
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

#--------------------------------------------------------------------
  def resolve_geometry(self):
#--------------------------------------------------------------------
    print "+++++++++++++++ resolve_geometry beg", self.get_name(), "+++++++++++++"
    ret = ""
    res = self.resolve_geometry_base()
    print "resolve_geometry_base = ", res
    if res == "":
      pass
    elif res == "ok":
      ret = "ok"
    else:
      return res

    print "self.IsEqualGateSize", self.IsEqualGateSize
    if self.IsEqualGateSize:
      res = self.set_equal_gate_size()
      print "set_equal_gate_size res = ", res
      if res == "":
        pass
      elif res == "ok":
        ret = "ok"
      else:
        return res


    res = self.resolve_geometry_child()
    print "resolve_geometry_child res = ", res
    if res == "":
      pass
    elif res == "ok":
      ret = "ok"
    else:
      return res


    res = self.resolve_geometry_pos_norm_generic()
    print "resolve_geometry_pos_norm_generic res = ", res
    if res == "":
      pass
    elif res == "ok":
      ret = "ok"
    else:
      return res

    res = self.resolve_geometry_pos_norm()
    print "resolve_geometry_pos_norm res = ", res
    if res == "":
      pass
    elif res == "ok":
      ret = "ok"
    else:
      return res

    res = self.resolve_geometry_set_gates_norm_pos()
    print "resolve_geometry_set_gates_norm_pos res = ", res
    if res == "":
      pass
    elif res == "ok":
      ret = "ok"
    else:
      return res

    

    print "resolve_geometry ret = ", ret
    return ret

#--------------------------------------------------------------------
  def resolve_geometry_child(self):
    return ""

#--------------------------------------------------------------------
  def resolve_geometry_pos_norm(self):
    return ""

#--------------------------------------------------------------------
  def resolve_geometry_pos_norm_generic(self):
#--------------------------------------------------------------------
    pairs_normal = self.collect_gate_pairs_normal()

    print "$$$$$$$$$$$$$$$$$$$$$$ pairs_normal"

    # Non collinear vectors
    pairs_normal_nc = []

    for pair in pairs_normal:
      print pair[0], pair[1]
      nc_flag = True
      for nc_pair in pairs_normal_nc:
        if is_colinear(pair[0], nc_pair[0]):
          nc_flag = False

      if nc_flag:
        pairs_normal_nc.append(pair)

    print "$$$$$$$$$$$$$$$$$$$$$$ pairs_normal_nc"
    for pair in pairs_normal_nc:
      print pair[0], pair[1]
       

    pairs_pos = self.collect_gate_pairs_pos()

    print "$$$$$$$$$$$$$$$$$$$$$$ pairs_pos"

    for pair in pairs_pos:
      print pair[0], pair[1]


# Resolving of orientation

    print "Resolving of orientation"
    print "IsAxialSym = ", self.IsAxialSym
    if self.IsAxialSym:
      print "IsAxialSym"
      if len(pairs_normal_nc) >= 1:
        print "Normal exists"
        self.RotationOperator = GetRotationMatrixVectorToVector(
          pairs_normal_nc[0][0], pairs_normal_nc[0][1])
      else:
        print "Check positions"
        if len(pairs_pos) >= 2:
          print "More than 1 positions"
          DiffElement = pairs_pos[1][0] - pairs_pos[0][0]
          RealElement = pairs_pos[1][1] - pairs_pos[0][1]
          self.RotationOperator = GetRotationMatrixVectorToVector(
            DiffElement, RealElement)
          
    else:
      print "no IsAxialSym"
      if len(pairs_normal_nc) >= 2:
        print "Two Normal exists"
        axis = pairs_normal_nc[0][1]
        rot1 = GetRotationMatrixVectorToVector(
          pairs_normal_nc[0][0], axis)
        rot1.trace()

        rot2, res2 = GetRotationMatrixVectorFaceToVector(
          rot1 * pairs_normal_nc[1][0], pairs_normal_nc[1][1], axis)
        if res2 != "":
          return res2
        rot2.trace()

        self.RotationOperator = rot1 * rot2

      elif len(pairs_pos) >= 3:
        print "3  positions"
        DiffElement1 = pairs_pos[1][0] - pairs_pos[0][0]
        RealElement1 = pairs_pos[1][1] - pairs_pos[0][1] #axis
        DiffElement2 = pairs_pos[2][0] - pairs_pos[0][0]
        RealElement2 = pairs_pos[2][1] - pairs_pos[0][1]

        rot1 = GetRotationMatrixVectorToVector(
          DiffElement1, RealElement1)
        rot1.trace()

        rot2, res2 = GetRotationMatrixVectorFaceToVector(
          rot1 * DiffElement2, RealElement2, RealElement1)
        if res2 != "":
          return res2
        rot2.trace()

        self.RotationOperator = rot1 * rot2

      elif len(pairs_normal_nc) == 1 and len(pairs_pos) >= 2:
        print "Normal and pos"

        pos_nc = None
        for i in range[0, len(pairs_pos) - 1]: # -2?
          DiffElement0 = pairs_pos[i + 1][0] - pairs_pos[i][0]
          if not is_colinear(DiffElement0, pairs_normal_nc[0]):
            pos_nc = i
            break

        if pos_nc is not None:
          DiffElement = pairs_pos[pos_nc + 1][0] - pairs_pos[pos_nc][0]
          RealElement = pairs_pos[pos_nc + 1][1] - pairs_pos[pos_nc][1] 

          axis = pairs_normal_nc[0][1]
          rot1 = GetRotationMatrixVectorToVector(
            pairs_normal_nc[0][0], axis)
          rot1.trace()
      
          rot2, res2 = GetRotationMatrixVectorFaceToVector(
            rot1 * DiffElement, RealElement, axis)
          if res2 != "":
            return res2
          rot2.trace()
      
          self.RotationOperator = rot1 * rot2


    if self.RotationOperator is not None:
      print "Orientation Resolved"
      self.RotationOperator.trace()
    else:
      print "Orientation not Resolved"


# Resolving of positions

    print "Resolving of positions"
    if len(pairs_pos) > 0:
      print "pairs_pos > 0"
      if self.RotationOperator is not None: 
        print "RotationOperator is not None"
        RealShift = self.RotationOperator * pairs_pos[0][0] 
        print "RealShift, pairs_pos[0][1]", RealShift, pairs_pos[0][1]
        self.CenterPos = pairs_pos[0][1] - RealShift
        self.CenterPos.round()
 
    if self.CenterPos is not None:
      print "CenterPos Resolved CenterPos", self.CenterPos
    else:
      print "CenterPos not Resolved"

    return ""

#--------------------------------------------------------------------
  def resolve_geometry_set_gates_norm_pos(self):
#--------------------------------------------------------------------
    if self.RotationOperator is None:
      return ""

    ret = ""

    for gate in self.heads:
      if gate.NormalElement is not None:
        RealNormal = self.RotationOperator * gate.NormalElement
        RealNormal.round()
        res = gate.set_normal(RealNormal)
        print "set_gates_norm_pos 1 res = ", res
        if res == "":
          pass
        elif res == "ok":
          ret = "ok"
        else:
          return res 

      if self.CenterPos is not None and gate.PosElement is not None:
        RealShift = self.RotationOperator * gate.PosElement
        RealShift.round()
        res = gate.set_pos(self.CenterPos + RealShift)
        print "set_gates_norm_pos 2 res = ", res
        if res == "":
          pass
        elif res == "ok":
          ret = "ok"
        else:
          return res

    for gate in self.tails:
      if gate.NormalElement is not None:
        RealNormal = self.RotationOperator * gate.NormalElement
        RealNormal.round()
        res = gate.set_normal(RealNormal)
        print "set_gates_norm_pos 1 res = ", res
        if res == "":
          pass
        elif res == "ok":
          ret = "ok"
        else:
          return res 

      if self.CenterPos is not None and gate.PosElement is not None:
        RealShift = self.RotationOperator * gate.PosElement
        RealShift.round()
        res = gate.set_pos(self.CenterPos + RealShift)
        print "set_gates_norm_pos 2 res = ", res
        if res == "":
          pass
        elif res == "ok":
          ret = "ok"
        else:
          return res


    return ret


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
#--------------------------------------------------------------------
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
  def set_equal_gate_size(self):
#--------------------------------------------------------------------
    ret = ""

    for gate in self.heads:
      res = self.set_gate_size_all(gate.Size) 
      if res == "":
        pass
      elif res == "ok":
        ret = "ok"
      else:
        return res

    for gate in self.tails:
      res = self.set_gate_size_all(gate.Size)
      if res == "":
        pass
      elif res == "ok":
        ret = "ok"
      else:
        return res

    return ret

#--------------------------------------------------------------------
  def set_gate_size_all(self, Size):
#--------------------------------------------------------------------
    ret = ""

    for gate in self.heads:
      res = gate.set_size(Size)
      if res == "":
        pass
      elif res == "ok":
        ret = "ok"
      else:
        return res

    for gate in self.tails:
      res = gate.set_size(Size)
      if res == "":
        pass
      elif res == "ok":
        ret = "ok"
      else:
        return res

    return ret

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
  def collect_gate_pairs_normal(self):
#--------------------------------------------------------------------
    pairs = []
    for gate in self.heads:
      if gate.NormalElement is not None and gate.Normal.is_not_none():
        pairs.append((gate.NormalElement, gate.Normal))
    for gate in self.tails:
      if gate.NormalElement is not None and gate.Normal.is_not_none():
        pairs.append((gate.NormalElement, gate.Normal))
    return pairs

#--------------------------------------------------------------------
  def collect_gate_pairs_pos(self):
#--------------------------------------------------------------------
    pairs = []
    for gate in self.heads:
      if gate.PosElement is not None and gate.Pos.is_not_none():
        pairs.append((gate.PosElement, gate.Pos))
    for gate in self.tails:
      if gate.PosElement is not None and gate.Pos.is_not_none():
        pairs.append((gate.PosElement, gate.Pos))
    return pairs

#--------------------------------------------------------------------
  def create_shape(self):
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
    print "Gate --------------------"
    gate.print_info()