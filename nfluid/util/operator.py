from nfluid.util.vector import *

#==============================================================================                             
class Operator(object):
  def __init__(self):
    self.VA = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]

  def reset(self):
    self.VA = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]

  def is_empty(self): 
    for i in xrange(0, 9):
      if not is_equal_eps(self.VA[i], 0):
        return False
    return True

  def set_empty(self):
    for i in xrange(0, 9): Res.VA[i] = 0
    
  def A(self, row, col):
    return self.VA[3 * row + col]
  
  def setA(self, row, col, val):
    self.VA[3 * row + col] = val

  def V(self, pos):
    return self.VA[pos]  

  def setV(self, pos, val):
    self.VA[pos] = val

  def scale(self, val):
    for i in xrange(0, 9):
      self.VA[i] *= val

#--------------------------------------------------------------------
  def get_invert(self): 
#--------------------------------------------------------------------
    Res = Operator()
  
    if self.is_empty():
      Res.set_empty()
    else:
      Res.setA(0,0, self.A(1,1)*self.A(2,2) - self.A(1,2)*self.A(2,1))
      Res.setA(0,1, self.A(0,2)*self.A(2,1) - self.A(0,1)*self.A(2,2))
      Res.setA(0,2, self.A(0,1)*self.A(1,2) - self.A(0,2)*self.A(1,1))
                                                  
      Res.setA(1,0, self.A(1,2)*self.A(2,0) - self.A(1,0)*self.A(2,2))
      Res.setA(1,1, self.A(0,0)*self.A(2,2) - self.A(0,2)*self.A(2,0))
      Res.setA(1,2, self.A(0,2)*self.A(1,0) - self.A(0,0)*self.A(1,2))
                                                  
      Res.setA(2,0, self.A(1,0)*self.A(2,1) - self.A(1,1)*self.A(2,0))
      Res.setA(2,1, self.A(2,0)*self.A(0,1) - self.A(0,0)*self.A(2,1))
      Res.setA(2,2, self.A(0,0)*self.A(1,1) - self.A(0,1)*self.A(1,0))
    
      Res.scale(1.0 / self.get_deterninant())
#      Res.TryRound()
    return Res

#--------------------------------------------------------------------
  def get_deterninant(self): 
#--------------------------------------------------------------------
    return \
        self.A(0,0)*(self.A(1,1)*self.A(2,2)-self.A(1,2)*self.A(2,1)) \
      - self.A(0,1)*(self.A(2,2)*self.A(1,0)-self.A(1,2)*self.A(2,0)) \
      + self.A(0,2)*(self.A(1,0)*self.A(2,1)-self.A(1,1)*self.A(2,0))  

#--------------------------------------------------------------------
  def trace(self): 
#--------------------------------------------------------------------
    for i in xrange(0, 3):
      print self.A(i,0), self.A(i,1), self.A(i,2)

    new_x = self * Vector(1, 0, 0)
    print "X axis will be ", new_x
    new_y = self * Vector(0, 1, 0)
    print "Y axis will be ", new_y
    new_z = self * Vector(0, 0, 1)
    print "Z axis will be ", new_z

#=======================================================================
#--------------------------------------------------------------------
  def __mul__(self, right):
#--------------------------------------------------------------------
    if isinstance(right, Vector):
      Res = Vector()
      for i in xrange(0, 3):
        sum = 0
        for j in xrange(0, 3):
              sum += self.A(i,j) * right.X(j)
        Res.setX(i, sum)

      Res.round()
      return Res

    elif isinstance(right, Operator):
      Res = Operator()
      for i in xrange(0, 3):
        for j in xrange(0, 3):
          sum = 0
          for k in xrange(0, 3):
            sum += self.A(i,k) * right.A(k,j)
     
          Res.setA(i, j, sum)
     
      Res.round()
      return Res

    elif isinstance(right, (int, long, float)):
      Res = Operator()
      for i in xrange(0, 9):
        Res.setV(i, self.V(i) * right)
      return Res

    else:
      raise TypeError('unsupported operand type(s)')
  
#--------------------------------------------------------------------
  def __div__(self, right):
#--------------------------------------------------------------------
    if isinstance(right, (int, long, float)):
      Res = Operator()
      for i in xrange(0, 9):
        Res.setV(i, self.V(i) / right)
      return Res

    else:
      raise TypeError('unsupported operand type(s)')

#--------------------------------------------------------------------
  def round(self):
#--------------------------------------------------------------------
    for i in xrange(0, 9):
      if is_equal_eps(self.VA[i], 0):
        self.VA[i] = 0.0

 
