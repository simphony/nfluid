from NF_ChannelElement2G import *
from NF_Gates import *
#====================================================================
# Class of Cone
class NF_Cone(NF_ChannelElement2G):
#--------------------------------------------------------------------
  def __init__(self, \
    RH = None, RT = None, L = None, \
    PosH = None, PosT = None,    \
    Normal = None):

    NF_ChannelElement2G.__init__(self)
    self.heads.append(NF_GateCircle(self))
    self.tails.append(NF_GateCircle(self))

    self.length = L
    self.setNormalDef(Normal)
    self.getHeadGate().setPosDef(PosH)
    self.getTailGate().setPosDef(PosT)
    self.getHeadGate().setSizeDef(RH)
    self.getTailGate().setSizeDef(RT)

#--------------------------------------------------------------------
  def getName(self):
    return "Cone"

#--------------------------------------------------------------------
  def Print(self):
    NF_ChannelElement2G.Print(self)
    print "NF_Cone RHdef =", self.getHeadGate().getRdef(), \
      "radiusTail RTdef=", self.getTailGate().getRdef(), "length =", self.length, \
      "RH =", self.getGateSizeH(), "RT =", self.getGateSizeT() 
                                                        
