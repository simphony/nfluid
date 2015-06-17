from ChannelElement2G import *
from Gates import *
#====================================================================
# Class of FlowAdapter
class FlowAdapter(ChannelElement2G):
#--------------------------------------------------------------------
  def __init__(self, \
    RH = None, RT = None, L = None, \
    PosH = None, PosT = None,    \
    Normal = None):

    ChannelElement2G.__init__(self)
    self.heads.append(GateCircle(self))
    self.tails.append(GateCircle(self))

    self.length = L
    self.setNormalDef(Normal)
    self.getHeadGate().setPosDef(PosH)
    self.getTailGate().setPosDef(PosT)
    self.getHeadGate().setSizeDef(RH)
    self.getTailGate().setSizeDef(RT)

#--------------------------------------------------------------------
  def getName(self):
    return "FlowAdapter"

#--------------------------------------------------------------------
  def Print(self):
    ChannelElement2G.Print(self)
    print "FlowAdapter RHdef =", self.getHeadGate().getRdef(), \
      "radiusTail RTdef=", self.getTailGate().getRdef(), "length =", self.length, \
      "RH =", self.getGateSizeH(), "RT =", self.getGateSizeT() 
                                                        
