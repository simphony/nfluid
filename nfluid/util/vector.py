import copy
import math


#====================================================================
def is_equal_eps(v1, v2, eps = 1e-8):
#--------------------------------------------------------------------
  if v1 is None or v2 is None:
    return False
  return math.fabs(v1 - v2) <= eps 
#====================================================================
class Vector(object):
#--------------------------------------------------------------------
  def __init__(self, x = None, y = None, z = None):
    self.x = x
    self.y = y
    self.z = z

#--------------------------------------------------------------------
  def __add__(self, right):
#--------------------------------------------------------------------
    if type(right) is not Vector:
      raise TypeError('unsupported operand type(s)')        

    if self.x is not None and right.x is not None:
      x = self.x + right.x
    else:
      x = None 

    if self.y is not None and right.y is not None:
      y = self.y + right.y
    else:
      y = None 

    if self.z is not None and right.z is not None:
      z = self.z + right.z
    else:
      z = None 

    return Vector(x, y, z) 

#--------------------------------------------------------------------
  def __sub__(self, right):
#--------------------------------------------------------------------
    if type(right) is not Vector:
      raise TypeError('unsupported operand type(s)')

    if self.x is not None and right.x is not None:
      x = self.x - right.x
    else:
      x = None

    if self.y is not None and right.y is not None:
      y = self.y - right.y
    else:
      y = None

    if self.z is not None and right.z is not None:
      z = self.z - right.z
    else:
      z = None

    return Vector(x, y, z)

#--------------------------------------------------------------------
  def __mul__(self, right):
#--------------------------------------------------------------------
    if not isinstance(right, (int, long, float)):
      raise TypeError('unsupported operand type(s)')

    if self.x is not None and right is not None:
      x = self.x * right
    else:
      x = None

    if self.y is not None and right is not None:
      y = self.y * right
    else:
      y = None

    if self.z is not None and right is not None:
      z = self.z * right
    else:
      z = None

    return Vector(x, y, z)

#--------------------------------------------------------------------
  def __div__(self, right):
#--------------------------------------------------------------------
    if right == 0:
      raise TypeError('division on 0')

    if self.x is not None and right is not None:
      x = self.x / right
    else:
      x = None
    
    if self.y is not None and right is not None:
      y = self.y / right
    else:
      y = None
    
    if self.z is not None and right is not None:
      z = self.z / right
    else:
      z = None
    
    return Vector(x, y, z)     
    
#--------------------------------------------------------------------
  def set(self, x, y, z):
#--------------------------------------------------------------------
    changed = False

    if x is not None:
      if self.x is not None:
        if not is_equal_eps(self.x, x): return "x is not equal to already defined value self.x", self.x, "x", x
      else:
        self.x = x
        changed = True

    if y is not None:
      if self.y is not None:
        if not is_equal_eps(self.y, y): return "y is not equal to already defined value self.y", self.y, "y", y
      else:
        self.y = y
        changed = True

    if z is not None:
      if self.z is not None:
        if not is_equal_eps(self.z, z): return "z is not equal to already defined value self.z", self.z, "z", z
      else:
        self.z = z
        changed = True

    if changed:
      return "ok"
    else:
      return ""

#--------------------------------------------------------------------
  def set_v(self, v):
    return self.set(v.x, v.y, v.z)

#--------------------------------------------------------------------
  def is_not_none(self):
    if self.x is not None and self.y is not None and self.z is not None:
      return True 
    else:
      return False 

#--------------------------------------------------------------------
  def is_none(self):
    if self.x is not None and self.y is not None and self.z is not None:
      return False
    else:
      return True

#--------------------------------------------------------------------
  def add(self, v):
#--------------------------------------------------------------------
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

#    print "Vector add ", ret
    return ret

#--------------------------------------------------------------------
  def sub(self, v):
#--------------------------------------------------------------------
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

#    print "Vector add ", ret
    return ret

#--------------------------------------------------------------------
  def normalize(self):
    len = self.get_len()
    if len is not None:
      if len != 0:
        self.scale(1 / len)
        
#--------------------------------------------------------------------
  def scale(self, s):
    if self.x is not None:
      self.x *= s
    if self.y is not None:
      self.y *= s
    if self.z is not None:
      self.z *= s

#--------------------------------------------------------------------
  def get_len(self):
    if self.is_none():
      return None
    else:
      return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

#--------------------------------------------------------------------
  def is_resolved_geometry(self):
    if self.x is None:
      return "x is None" 
    if self.y is None: 
      return "y is None"
    if self.z is None: 
      return "z is None" 
    return "" 

#--------------------------------------------------------------------
  def clear_geometry(self):
    self.x = None 
    self.y = None 
    self.z = None 

#--------------------------------------------------------------------
  def __str__(self):
    return "Vector x = {0} y = {1} z = {2}".format(self.x, self.y, self.z)

#======================================================================
def scalar_product(v1, v2):
#--------------------------------------------------------------------
  if type(v1) is not Vector or type(v2) is not Vector :
    raise TypeError('unsupported operand type(s)')

  if v1.is_not_none() and v2.is_not_none():
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

  return None

#--------------------------------------------------------------------
def get_vector_angle(v1, v2):
#--------------------------------------------------------------------
  if type(v1) is not Vector or type(v2) is not Vector :
    raise TypeError('unsupported operand type(s)')

  if v1.is_not_none() and v2.is_not_none():
    L2 =v1.get_len() * v2.get_len()
    if L2 == 0:
      raise TypeError('Zero vector length')

    cos_angle = scalar_product(v1, v2)/L2
    print "cos_angle = ", cos_angle
    angle = math.degrees(math.acos(cos_angle))
    print "angle = ", angle
    return angle

  return None

#--------------------------------------------------------------------
def get_projection(v, axis):
#--------------------------------------------------------------------
  if type(v) is not Vector or type(axis) is not Vector :
    raise TypeError('unsupported operand type(s)')

  if v.is_not_none() or axis.is_not_none():
    return None #TODO or None Vector
  AxisNorm = Vector(axis.x, axis.y, axis.z)
  AxisNorm.normalize()
  AxisNorm.scale(scalar_product(AxisNorm, v))

  return AxisNorm

