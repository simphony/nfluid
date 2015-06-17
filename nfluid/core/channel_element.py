from Gate import * 

#==============================================================================
#Base class of Channel Elements
class ChannelElement(object):
#--------------------------------------------------------------------
  assembly = None;

  def __init__(self):
    ChannelElement.assembly.addElement(self)
    self.heads = []
    self.tails = []
    self.changed = True

#--------------------------------------------------------------------
  def getName(self):
    return "ChannelElement"

#--------------------------------------------------------------------
  def getHeadGate(self, n = 0):
    return self.heads[n]

#--------------------------------------------------------------------
  def getTailGate(self, n = 0):
    return self.tails[n]

#--------------------------------------------------------------------
  def getTailGateBif(self, n = 0):
    return self.tailsBif[n]

#--------------------------------------------------------------------
  def getNextElement(self, n = 0):
    gt = self.getTailGate(n)
    if gt is None:
      return None
    gtb = gt.buddy
    if gtb is None:
      return None
    return gtb.element

#--------------------------------------------------------------------
  def getPrevElement(self, n = 0):
    gh = self.getHeadGate(n)
    if gh is None:
      return None
    ghb = gh.buddy
    if ghb is None:
      return None
    return ghb.element

#--------------------------------------------------------------------
  def link(self, next, gateTail = 0, gateHead = 0):
    gt1 = self.getTailGate(gateTail)
    gh2 = next.getHeadGate(gateHead)
    gt1.buddy = gh2
    gh2.buddy = gt1
    return next

#--------------------------------------------------------------------
  def Print(self):
    self.forEachGate(fcnPrintXXX)
#    print "ChannelElement"

#--------------------------------------------------------------------  
  def PrintChannel(self):
    self.Print()
    next = self.getNextElement()
    if next is not None:
      next.PrintChannel()

#--------------------------------------------------------------------
# "" nothing changed
# "ok" something changed
# "other text" - fatal error
  def resolveGeometry(self):
#--------------------------------------------------------------------
    ret = ""
    res = self.resolveGeometryBase()
    print "Tail gate res = ", res
    if res == "":
      pass
    elif res == "ok":
      ret = "ok"
    else:
      return res

    res = self.resolveGeometryChild()
    print "Tail gate res = ", res
    if res == "":
      pass
    elif res == "ok":
      ret = "ok"
    else:
      return res

    return ret

#--------------------------------------------------------------------
  def resolveGeometryChild(self):
    return ""

#--------------------------------------------------------------------
# "" nothing changed
# "ok" something changed
# "other text" - fatal error
  def resolveGeometryBase(self):
#--------------------------------------------------------------------
    ret = ""
    for gate in self.heads:
      res = gate.resolveGeometry()
      print "Head gate res = ", res
      if res == "":
        pass
      elif res == "ok":
        ret = "ok"
      else:
        return res 

    for gate in self.tails:
      res = gate.resolveGeometry()
      print "Tail gate res = ", res
      if res == "":
        pass
      elif res == "ok":
        ret = "ok"
      else:
        return res

      return ret

#--------------------------------------------------------------------
  def isResolvedGeometry(self):
    msg = "xxx"
    for gate in self.heads:
      res = gate.isResolvedGeometry()
      if res != "":
        return msg + res
    for gate in self.tails:
      res = gate.isResolvedGeometry()
      if res != "":
        return msg + res
    return ""

#--------------------------------------------------------------------
#  @staticmethod
  def fcnClearGeometry(gate):
    gate.clearGeometry()

#--------------------------------------------------------------------
  def clearGeometry(self):
    self.forEachGate(fcnClearGeometryXXX)
#    self.forEachGate(ChannelElement.fcnClearGeometry)

#--------------------------------------------------------------------
  def forEachGate(self, fcn):
    for gate in self.heads:
      fcn(gate)
    for gate in self.tails:
      fcn(gate)

#--------------------------------------------------------------------
def fcnClearGeometryXXX(gate):
    gate.clearGeometry()

#--------------------------------------------------------------------
def fcnPrintXXX(gate):
    gate.Print()

