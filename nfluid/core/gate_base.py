from NF_Vector import *

#====================================================================
class NF_Gate(object):
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
    self.Pos = NF_Vector()
    self.NormalDef = None
    self.Normal = NF_Vector()

#--------------------------------------------------------------------
# Position -------------------
  def setPosDef(self, PosDef):
#    print "Gate setPosDef"
    self.PosDef = PosDef

#--------------------------------------------------------------------
  def setSizeDef(self, s0, s1 = None, s2 = None, s3 = None):
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
  def setSizeArg(self, s0, s1 = None, s2 = None, s3 = None):
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

    return self.setSize(Size)

#--------------------------------------------------------------------
#No effect - return ""
#Done - return "ok"
#Error - other text
  def setSize(self, Size):
#--------------------------------------------------------------------
    if len(self.Size) != len(Size):
      return "Incompatible size array length"

    ret = ""
    for i in range(0, len(Size)):
      if self.Size[i] is not None:
        if Size[i] is not None:
          if (self.Size[i] != Size[i]):
            return "NF_Gate setSize incompatible sizes i = ", i, \
              " self.Size[i] = ", self.Size[i], "  Size[i] = ", Size[i]
      else:
        self.Size[i] = Size[i]
        ret = "ok"

    if ret == "ok":
      if self.buddy is not None:
        res = self.buddy.setSizeExt(self.Size)
        if res != "":
          return res

    return ""

#--------------------------------------------------------------------
#Ok - return ""
#Error - not empty
  def setSizeExt(self, Size):
#--------------------------------------------------------------------
    if len(self.Size) != len(Size):
      return "Incompatible size array length"

    ret = ""
    for i in range(0, len(Size)):
      if self.Size[i] is not None:
        if (self.Size[i] != Size[i]):
          return "NF_Circle setSize incompatible sizes i = ", i, \
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
  def setPos(self, Pos):
#--------------------------------------------------------------------
    print "Gate setPos"
    res = self.Pos.setv(Pos)
# nothing changed
    if res == "":
      return ""
# changed
    elif res == "ok":
      if self.buddy is not None:
        res = self.buddy.setPosExt(self.Pos)
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
  def setPosExt(self, Pos):
#--------------------------------------------------------------------
    print "Gate setPosExt"
    res = self.Pos.setv(Pos)
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
  def setNormalDef(self, NormalDef):
#    print "Gate setNormalDef"
    self.NormalDef = NormalDef

#--------------------------------------------------------------------
#from element
# "" - nothing changed
# "ok" - changed
# other - error
  def setNormal(self, Normal):
#--------------------------------------------------------------------
    print "Gate setNormal"
    res = self.Normal.setv(Normal)
# nothing changed
    if res == "":
      return ""
# changed
    elif res == "ok":
      if self.buddy is not None:
        res = self.buddy.setNormalExt(self.Normal)
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
  def setNormalExt(self, Normal):
#--------------------------------------------------------------------
    print "Gate setNormalExt"
    res = self.Normal.setv(Normal)
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
  def clearGeometry(self):
    for size in self.Size:
      size = None
    self.Pos.clearGeometry()
    self.Normal.clearGeometry()
    print "NF_Gate clearGeometry"

#--------------------------------------------------------------------
  def isResolvedGeometry(self):
    for size in self.Size:
      if size is None:
        return "Gate size is none"

    res = self.Pos.isResolvedGeometry()
    if res != "":
      return res
    res = self.Normal.isResolvedGeometry()
    if res != "":
      return res
    return ""

#--------------------------------------------------------------------
# "" nothing changed
# "ok" something changed
# "other text" - fatal error
  def resolveGeometry(self):
#--------------------------------------------------------------------
    print "Gate resolveGeometry"
    self.Print()
    ret = ""

    
#    if self.Rdef is not None:
    res = self.setSize(self.SizeDef)
    if res == "":
      pass
    elif res == "ok":
      ret = "ok"
    else:
      return res
    

    if self.PosDef is not None:
      res =  self.setPos(self.PosDef)
      if res == "":
        pass
      elif res == "ok":
        ret = "ok"
      else:
        return res 

    if self.NormalDef is not None:
      res =  self.setNormal(self.NormalDef)
      if res == "":
        pass
      elif res == "ok":
        ret = "ok"
      else:
        return res

    return ret

#--------------------------------------------------------------------
  def Print(self):
    if self.PosDef is not None:
      self.PosDef.Print()
    else:
      print "Pos def is None"

    self.Pos.Print()

    if self.NormalDef is not None:
      self.NormalDef.Print()
    else:
      print "Normal def is None"

    self.Normal.Print()

