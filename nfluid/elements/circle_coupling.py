from ChannelElement2G import *
from Gates import *

#====================================================================
# Class of Coupling
class Coupling(ChannelElement2G):
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
    return "Coupling"

#--------------------------------------------------------------------
  def resolveGeometryChild(self):
    return self.setEqualGateSize()

#--------------------------------------------------------------------
  def Print(self):
    ChannelElement2G.Print(self)
    print "Coupling radius Rdef =", self.getHeadGate().getRdef(), "length =", self.length, \
      "RH =", self.getGateSizeH(), "RT =", self.getGateSizeT()


