from ChannelElement2G import *
from Gates import *
#====================================================================
# Class of CouplingSquare
class CouplingSquare(ChannelElement2G):
#--------------------------------------------------------------------
  def __init__(self, A = None, B = None, L = None, \
      PosH = None, PosT = None,    \
      Normal = None):
    ChannelElement2G.__init__(self)
    self.length = L
    self.heads.append(GateRect(self))
    self.tails.append(GateRect(self))

    self.setNormalDef(Normal)
    self.getHeadGate().setPosDef(PosH)
    self.getTailGate().setPosDef(PosT)
    self.getHeadGate().setSizeDef(A, B)
    self.getTailGate().setSizeDef(A, B)

#--------------------------------------------------------------------
  def getName(self):
    return "CouplingSquare"

#--------------------------------------------------------------------
  def resolveGeometryChild(self):
    return self.setEqualGateSize()

#--------------------------------------------------------------------
  def Print(self):
    ChannelElement2G.Print(self)
    print "CouplingSquare AHdef =", self.getHeadGate().getAdef(), \
      " BHdef =", self.getHeadGate().getBdef(),           \
      "length =", self.length, \
      " AH =", self.getGateSizeH(), "AT =", self.getGateSizeT() 


