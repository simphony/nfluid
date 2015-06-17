from Vector import *

#====================================================================
class Gate(object):
#--------------------------------------------------------------------
  def __init__(self, element):
    self.buddy = None
    self.element = element
    self.x = 0
    self.y = 0
    self.z = 0
    self.SizeDef = []
    self.Size = []
    self.PosDef = None
    self.Pos = Vector()
    self.NormalDef = None
    self.Normal = Vector()

#--------------------------------------------------------------------
# Position -------------------
  def set_pos_def(self, PosDef):
#    print "Gate set_pos_def"
    self.PosDef = PosDef

#--------------------------------------------------------------------
  def set_size_def(self, s0, s1 = None, s2 = None, s3 = None):
    SizeLen = len(self.SizeDef)
    if SizeLen > 0:
      self.SizeDef[0] = s0
    if SizeLen > 1:
      self.SizeDef[1] = s1
    if SizeLen > 2:
      self.SizeDef[2] = s2
    if SizeLen > 3:
      self.SizeDef[3] = s3

#--------------------------------------------------------------------
  def set_size_arg(self, s0, s1 = None, s2 = None, s3 = None):
    SizeLen = len(self.Size)
    Size = []
    if SizeLen > 0:
      Size.append(s0)
    if SizeLen > 1:
      Size.append(s1)
    if SizeLen > 2:
      Size.append(s2)
    if SizeLen > 3:
      Size.append(s3)

    return self.set_size(Size)

#--------------------------------------------------------------------
#No effect - return ""
#Done - return "ok"
#Error - other text
  def set_size(self, Size):
#--------------------------------------------------------------------
    if len(self.Size) != len(Size):
      return "Incompatible size array length"

    ret = ""
    for i in range(0, len(Size)):
      if self.Size[i] is not None:
        if Size[i] is not None:
          if (self.Size[i] != Size[i]):
            return "Gate set_size incompatible sizes i = ", i, \
              " self.Size[i] = ", self.Size[i], "  Size[i] = ", Size[i]
      else:
        self.Size[i] = Size[i]
        ret = "ok"

    if ret == "ok":
      if self.buddy is not None:
        res = self.buddy.set_size_ext(self.Size)
        if res != "":
          return res

    return ""

#--------------------------------------------------------------------
#Ok - return ""
#Error - not empty
  def set_size_ext(self, Size):
#--------------------------------------------------------------------
    if len(self.Size) != len(Size):
      return "Incompatible size array length"

    ret = ""
    for i in range(0, len(Size)):
      if self.Size[i] is not None:
        if (self.Size[i] != Size[i]):
          return "Circle set_size incompatible sizes i = ", i, \
            " self.Size[i] = ", self.Size[i], "  Size[i] = ", Size[i]
      else:
        self.Size[i] = Size[i]
        ret = "ok"

    if ret == "ok":
      self.element.changed = True

    return ""

#--------------------------------------------------------------------
#from element
# "" - nothing changed
# "ok" - changed
# other - error
  def set_pos(self, Pos):
#--------------------------------------------------------------------
    print "Gate set_pos"
    res = self.Pos.set_v(Pos)
# nothing changed
    if res == "":
      return ""
# changed
    elif res == "ok":
      if self.buddy is not None:
        res = self.buddy.set_pos_ext(self.Pos)
        if res != "":
          return res
      return "ok"
# error
    else:
      return res

#--------------------------------------------------------------------
# from buddy
# "" - no errors
# other - error
  def set_pos_ext(self, Pos):
#--------------------------------------------------------------------
    print "Gate set_pos_ext"
    res = self.Pos.set_v(Pos)
# nothing changed
    if res == "":
      return ""
# changed
    elif res == "ok":
      self.element.changed = True
      return ""
# error
    else:
      return res

#--------------------------------------------------------------------
# Orientation ----------------------
  def set_normal_def(self, NormalDef):
#    print "Gate set_normal_def"
    self.NormalDef = NormalDef

#--------------------------------------------------------------------
#from element
# "" - nothing changed
# "ok" - changed
# other - error
  def set_normal(self, Normal):
#--------------------------------------------------------------------
    print "Gate set_normal"
    res = self.Normal.set_v(Normal)
# nothing changed
    if res == "":
      return ""
# changed
    elif res == "ok":
      if self.buddy is not None:
        res = self.buddy.set_normal_ext(self.Normal)
        if res != "":
          return res
      return "ok"
# error
    else:
      return res

#--------------------------------------------------------------------
#from buddy
# "" - no errors
# other - error
  def set_normal_ext(self, Normal):
#--------------------------------------------------------------------
    print "Gate set_normal_ext"
    res = self.Normal.set_v(Normal)
# nothing changed
    if res == "":
      return ""
# changed
    elif res == "ok":
      self.element.changed = True
      return ""
# error
    else:
      return res

#--------------------------------------------------------------------
  def clear_geometry(self):
    for size in self.Size:
      size = None
    self.Pos.clear_geometry()
    self.Normal.clear_geometry()
    print "Gate clear_geometry"

#--------------------------------------------------------------------
  def is_resolved_geometry(self):
    for size in self.Size:
      if size is None:
        return "Gate size is none"

    res = self.Pos.is_resolved_geometry()
    if res != "":
      return res
    res = self.Normal.is_resolved_geometry()
    if res != "":
      return res
    return ""

#--------------------------------------------------------------------
# "" nothing changed
# "ok" something changed
# "other text" - fatal error
  def resolve_geometry(self):
#--------------------------------------------------------------------
    print "Gate resolve_geometry"
    self.print_info()
    ret = ""

    
#    if self.Rdef is not None:
    res = self.set_size(self.SizeDef)
    if res == "":
      pass
    elif res == "ok":
      ret = "ok"
    else:
      return res
    

    if self.PosDef is not None:
      res =  self.set_pos(self.PosDef)
      if res == "":
        pass
      elif res == "ok":
        ret = "ok"
      else:
        return res 

    if self.NormalDef is not None:
      res =  self.set_normal(self.NormalDef)
      if res == "":
        pass
      elif res == "ok":
        ret = "ok"
      else:
        return res

    return ret

#--------------------------------------------------------------------
  def print_info(self):
    if self.PosDef is not None:
      self.PosDef.print_info()
    else:
      print "Pos def is None"

    self.Pos.print_info()

    if self.NormalDef is not None:
      self.NormalDef.print_info()
    else:
      print "Normal def is None"

    self.Normal.print_info()

