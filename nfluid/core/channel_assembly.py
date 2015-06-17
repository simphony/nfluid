from NF_ChannelElement import *
#====================================================================
class NF_ChannelAssembly(object):
#--------------------------------------------------------------------
  def __init__(self):
    self.elements = []
    NF_ChannelElement.assembly = self

#--------------------------------------------------------------------
  def addElement(self, element):
    self.elements.append(element)

#--------------------------------------------------------------------
  def forEachElement(self, fcn):
    for element in self.elements:
      fcn(element)

#--------------------------------------------------------------------
  def resolveGeometry(self):
#--------------------------------------------------------------------
    while True:
      print "resolveGeometry loop ---------------------------"
      Changed = False;
      for element in self.elements:
        if element.changed:
          print "resolveGeometry before --------"
          element.Print()
          res = element.resolveGeometry()
          if res != "":
            if res == "ok":
              Changed = True
            else:
              return res
          print "resolveGeometry after --------"
          element.Print()
          element.changed = False
      print "Changed", Changed
      if not Changed:
        break
    return self.isResolvedGeometry()

#--------------------------------------------------------------------        
  def isResolvedGeometry(self):
    for element in self.elements:
      res = element.isResolvedGeometry()
      if res != "":
        return res
    return ""

#--------------------------------------------------------------------
  def clearGeometry(self):
    for element in self.elements:
      element.clearGeometry()
      print "clearGeometry Assembly loop ---------------------------"        

#--------------------------------------------------------------------
  def Print(self):
    for element in self.elements:
      print "New Assembly Element --------------------------- " + element.getName()
      element.Print()


def CreateChannel(elt):
  return elt
