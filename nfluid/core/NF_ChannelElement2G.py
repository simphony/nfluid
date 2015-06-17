from NF_ChannelElement import *

#====================================================================
class NF_ChannelElement2G(NF_ChannelElement):
#--------------------------------------------------------------------
  def __init__(self):
    NF_ChannelElement.__init__(self)
    self.length = None

  def getGateSizeH(self, n = 0):
    return self.getHeadGate().Size[n]

  def setGateSizeH(self, s0, s1 = None, s2 = None, s3 = None):
    return self.getHeadGate().setSizeArg(s0, s1, s2, s3)

  def getGateSizeT(self, n = 0):
    return self.getTailGate().Size[n]

  def setGateSizeT(self, s0, s1 = None, s2 = None, s3 = None):
    return self.getTailGate().setSizeArg(s0, s1, s2, s3)

#--------------------------------------------------------------------
  def resolveGeometryBase(self):
#--------------------------------------------------------------------
    ret = ""
    res = NF_ChannelElement.resolveGeometryBase(self)
    if res == "":
      pass
    elif res == "ok":
      ret = "ok"
    else: 
      return res

    NormalH = copy.copy(self.getHeadGate().Normal)
    res = self.getTailGate().setNormal(self.getNormalTailFromHead(NormalH))
    if res == "":
      pass
    elif res == "ok":
      ret = "ok"
    else: 
      return res

    NormalT = copy.copy(self.getTailGate().Normal)
    res = self.getHeadGate().setNormal(self.getNormalHeadFromTail(NormalT))
    if res == "":
      pass
    elif res == "ok":
      ret = "ok"
    else:
      return res

    PosH = copy.copy(self.getHeadGate().Pos)
#    print "XXX---------------"
#    PosH.Print()
#    print "111---------------"
#    self.getGatesDiff().Print()
#    print "222---------------"
    res = PosH.add(self.getGatesDiff())
#    PosH.Print()
#    print "333--------------- res = ", res
    if res == "ok":
      res = self.getTailGate().setPos(PosH)
      if res == "":
        pass
      elif res == "ok":
        ret = "ok"
      else: 
        return res

    PosT = copy.copy(self.getTailGate().Pos)
#    print "XXX---------------"
#    PosT.Print()
#    self.getGatesDiff().Print()
    res = PosT.sub(self.getGatesDiff())
#    PosT.Print()
#    print "--------------- res = ", res
    if res == "ok":
      res = self.getHeadGate().setPos(PosT)
      if res == "":
        pass
      elif res == "ok":
        ret = "ok"
      else: 
        return res
#    print "AAA---------------"
    self.getHeadGate().Pos.Print()

    return ret

#--------------------------------------------------------------------
  def getGatesDiff(self):
#--------------------------------------------------------------------
    Normal = copy.copy(self.getHeadGate().Normal)
    print "getGatesDiff Normal"
    Normal.Print()
    Len = Normal.getLen()
    print "getGatesDiff Len", Len, "self.length", self.length
    if Len is None or  Len == 0:
      print "getGatesDiff bad"
      return NF_Vector()
    else:
      if self.length is None:
        x = None
        if IsEqualEps(Normal.x, 0):
          x = 0
        y = None
        if IsEqualEps(Normal.y, 0):
          y = 0
        z = None
        if IsEqualEps(Normal.z, 0):
          z = 0
        return NF_Vector(x, y, z)
      else:
        Normal.scale(self.length / Len)
        print "getGatesDiff Normal Scaled"
        Normal.Print()
        return Normal
#    return NF_Vector(10, 20, self.length)

#--------------------------------------------------------------------
  def setEqualGateSize(self):
#--------------------------------------------------------------------
    ret = ""
    SizeH = self.getHeadGate().Size
    res = self.getTailGate().setSize(SizeH)
    if res == "":
      pass
    elif res == "ok":
      ret = "ok"
    else:
      return res

    SizeT = self.getTailGate().Size
    res = self.getHeadGate().setSize(SizeT)
    if res == "":
      pass
    elif res == "ok":
      ret = "ok"
    else:
      return res

    return ret

#--------------------------------------------------------------------
  def setNormalDef(self, NormalDef):
    self.getHeadGate().setNormalDef(NormalDef)
    self.getTailGate().setNormalDef(NormalDef)

#--------------------------------------------------------------------
  def getNormalTailFromHead(self, NormalH):
    return NormalH

#--------------------------------------------------------------------
  def getNormalHeadFromTail(self, NormalT):
    return NormalT

#--------------------------------------------------------------------
  def getLen(self):
    if self.length is not None:
      return self.length
    else:
      DifPos = copy.copy(self.getHeadGate().Pos)
      DifPos.sub(self.getTailGate().Pos)
      return DifPos.getLen()

#--------------------------------------------------------------------
  def Print(self):
    NF_ChannelElement.Print(self)
    print "Len = ", self.getLen()



