import copy
import math


#====================================================================
def IsEqualEps(v1, v2, eps = 1e-8):
  if v1 is None or v2 is None:
    return False
  return math.fabs(v1 - v2) <= eps 
#====================================================================
class NF_Vector(object):
  def __init__(self, x = None, y = None, z = None):
    self.x = x
    self.y = y
    self.z = z

#--------------------------------------------------------------------
  def set(self, x, y, z):
    changed = False

    if x is not None:
      if self.x is not None:
        if not IsEqualEps(self.x, x): return "x is not equal to already defined value self.x", self.x, "x", x
      else:
        self.x = x
        changed = True

    if y is not None:
      if self.y is not None:
        if not IsEqualEps(self.y, y): return "y is not equal to already defined value self.y", self.y, "y", y
      else:
        self.y = y
        changed = True

    if z is not None:
      if self.z is not None:
        if not IsEqualEps(self.z, z): return "z is not equal to already defined value self.z", self.z, "z", z
      else:
        self.z = z
        changed = True

    if changed:
      return "ok"
    else:
      return ""

#--------------------------------------------------------------------
  def setv(self, v):
    return self.set(v.x, v.y, v.z)

#--------------------------------------------------------------------
  def add(self, v):
    ret = ""
    if self.x is not None:
      if v.x is None:
        self.x = None
      else:
        self.x += v.x
      ret = "ok"

    if self.y is not None:
      if v.y is None:
        self.y = None
      else:
        self.y += v.y
      ret = "ok"

    if self.z is not None:
      if v.z is None:
        self.z = None
      else:
        self.z += v.z
      ret = "ok"

#    print "NF_Vector add ", ret
    return ret

#--------------------------------------------------------------------
  def sub(self, v):
    ret = ""
    if self.x is not None:
      if v.x is None:
        self.x = None
      else:
        self.x -= v.x
      ret = "ok"

    if self.y is not None:
      if v.y is None:
        self.y = None
      else:
        self.y -= v.y
      ret = "ok"

    if self.z is not None:
      if v.z is None:
        self.z = None
      else:
        self.z -= v.z
      ret = "ok"

#    print "NF_Vector add ", ret
    return ret

#--------------------------------------------------------------------
  def scale(self, s):
    if self.x is not None:
      self.x *= s
    if self.y is not None:
      self.y *= s
    if self.z is not None:
      self.z *= s

#--------------------------------------------------------------------
  def getLen(self):
    if self.x is None or self.y is None or self.z is None:
      return None
    else:
      return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

#--------------------------------------------------------------------
  def isResolvedGeometry(self):
    if self.x is None:
      return "x is None" 
    if self.y is None: 
      return "y is None"
    if self.z is None: 
      return "z is None" 
    return "" 

#--------------------------------------------------------------------
  def clearGeometry(self):
    self.x = None 
    self.y = None 
    self.z = None 

#--------------------------------------------------------------------
  def Print(self):
    print "NF_Vector x=", self.x, " y =", self.y, " z =", self.z

