from NF_Gate import *

#====================================================================
class NF_GateCircle(NF_Gate):
#--------------------------------------------------------------------
  def __init__(self, aelement):
    NF_Gate.__init__(self, aelement)
    self.SizeDef = [None]
    self.Size = [None]

#--------------------------------------------------------------------
  def getRdef(self):
    return self.SizeDef[0]

#--------------------------------------------------------------------
  def getR(self):
    return self.Size[0]

#  def setR(self, v):
#    self.Size[0] = v

#--------------------------------------------------------------------
  def Print(self):
    NF_Gate.Print(self)
    print "NF_GateCircle", "radius =", self.getR()


#====================================================================
class NF_GateRect(NF_Gate):
#--------------------------------------------------------------------
  def __init__(self, aelement):
    NF_Gate.__init__(self, aelement)
    self.SizeDef = [None, None]
    self.Size = [None, None]

#--------------------------------------------------------------------
  def getAdef(self):
    return self.SizeDef[0]

#--------------------------------------------------------------------
  def getBdef(self):
    return self.SizeDef[1]

#--------------------------------------------------------------------
  def getA(self):
    return self.Size[0]

#--------------------------------------------------------------------
  def getB(self):
    return self.Size[1]

#--------------------------------------------------------------------
  def Print(self):
    NF_Gate.Print(self)
    print "NF_GateRect", "A = ", self.getA(), "B = ", self.getB()



