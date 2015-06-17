from Gate import *

#====================================================================
class GateCircle(Gate):
#--------------------------------------------------------------------
  def __init__(self, aelement):
    Gate.__init__(self, aelement)
    self.SizeDef = [None]
    self.Size = [None]

#--------------------------------------------------------------------
  def get_r_def(self):
    return self.SizeDef[0]

#--------------------------------------------------------------------
  def get_r(self):
    return self.Size[0]

#  def setR(self, v):
#    self.Size[0] = v

#--------------------------------------------------------------------
  def print_info(self):
    Gate.print_info(self)
    print "GateCircle", "radius =", self.get_r()


#====================================================================
class GateRect(Gate):
#--------------------------------------------------------------------
  def __init__(self, aelement):
    Gate.__init__(self, aelement)
    self.SizeDef = [None, None]
    self.Size = [None, None]

#--------------------------------------------------------------------
  def get_a_def(self):
    return self.SizeDef[0]

#--------------------------------------------------------------------
  def get_b_def(self):
    return self.SizeDef[1]

#--------------------------------------------------------------------
  def get_a(self):
    return self.Size[0]

#--------------------------------------------------------------------
  def get_b(self):
    return self.Size[1]

#--------------------------------------------------------------------
  def print_info(self):
    Gate.print_info(self)
    print "GateRect", "A = ", self.get_a(), "B = ", self.get_b()



