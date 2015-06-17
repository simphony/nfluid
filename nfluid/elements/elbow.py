from ChannelElement2G import *
from Gates import *

#====================================================================
# Class of Elbow
class Elbow(ChannelElement2G):
#--------------------------------------------------------------------
  def __init__(self, R = None, L = None, \
      PosH = None, PosT = None,    \
      Normal = None):
    ChannelElement2G.__init__(self)
    self.length = L
    self.heads.append(GateCircle(self))
    self.tails.append(GateCircle(self))

    self.setNormalDef(Normal)
    self.getHeadGate().setPosDef(PosH)
    self.getTailGate().setPosDef(PosT)
    self.getHeadGate().setSizeDef(R)
    self.getTailGate().setSizeDef(R)

#--------------------------------------------------------------------
  def getName(self):
    return "Elbow"

#--------------------------------------------------------------------
  def resolveGeometryChild(self):
    return self.setEqualGateSize()

#--------------------------------------------------------------------
  def getGatesDiff(self):
    return Vector(0, 3000, 4000)

#--------------------------------------------------------------------
  def getNormalTailFromHead(self, NormalH):
    return Vector(1, 0, 0)

#--------------------------------------------------------------------
  def getNormalHeadFromTail(self, NormalT):
    return Vector(0, 0, 1)

#--------------------------------------------------------------------
  def Print(self):
    ChannelElement2G.Print(self)
    print "Cylinder radius Rdef =", self.getHeadGate().getRdef(), "length =", self.length, \
      "RH =", self.getGateSizeH(), "RT =", self.getGateSizeT() 


