from NF_ChannelElement2G import *
from NF_Gates import *

#====================================================================
# Class of Cylinder
class NF_Cylinder(NF_ChannelElement2G):
#--------------------------------------------------------------------
  def __init__(self, R = None, L = None, \
      PosH = None, PosT = None,    \
      Normal = None):
    NF_ChannelElement2G.__init__(self)
    self.length = L
    self.heads.append(NF_GateCircle(self))
    self.tails.append(NF_GateCircle(self))

    self.setNormalDef(Normal)
    self.getHeadGate().setPosDef(PosH)
    self.getTailGate().setPosDef(PosT)
    self.getHeadGate().setSizeDef(R)
    self.getTailGate().setSizeDef(R)

#--------------------------------------------------------------------
  def getName(self):
    return "Cylinder"

#--------------------------------------------------------------------
  def resolveGeometryChild(self):
    return self.setEqualGateSize()

#--------------------------------------------------------------------
  def Print(self):
    NF_ChannelElement2G.Print(self)
    print "NF_Cylinder radius Rdef =", self.getHeadGate().getRdef(), "length =", self.length, \
      "RH =", self.getGateSizeH(), "RT =", self.getGateSizeT()


