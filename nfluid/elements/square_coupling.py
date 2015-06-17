from NF_ChannelElement2G import *
from NF_Gates import *
#====================================================================
# Class of Bar
class NF_Bar(NF_ChannelElement2G):
#--------------------------------------------------------------------
  def __init__(self, A = None, B = None, L = None, \
      PosH = None, PosT = None,    \
      Normal = None):
    NF_ChannelElement2G.__init__(self)
    self.length = L
    self.heads.append(NF_GateRect(self))
    self.tails.append(NF_GateRect(self))

    self.setNormalDef(Normal)
    self.getHeadGate().setPosDef(PosH)
    self.getTailGate().setPosDef(PosT)
    self.getHeadGate().setSizeDef(A, B)
    self.getTailGate().setSizeDef(A, B)

#--------------------------------------------------------------------
  def getName(self):
    return "Bar"

#--------------------------------------------------------------------
  def resolveGeometryChild(self):
    return self.setEqualGateSize()

#--------------------------------------------------------------------
  def Print(self):
    NF_ChannelElement2G.Print(self)
    print "NF_Bar AHdef =", self.getHeadGate().getAdef(), \
      " BHdef =", self.getHeadGate().getBdef(),           \
      "length =", self.length, \
      " AH =", self.getGateSizeH(), "AT =", self.getGateSizeT() 


