class STLShape(object):
  def __init__(self):
    print "ShapeSTL.__init__"

  def export(self, file):
    print "ShapeSTL.export"

  def show(self):
    print "ShapeSTL.show"

class STLCircleCoupling(STLShape):
  def __init__(self, R, L, PosH, PosT):
    self.Radius = R
    self.Length = L
    self.PosH = PosH
    self.PosT = PosT
    print "STLCircleCoupling.__init__"

class STLFlowAdapter(STLShape):
  def __init__(self, RH, RT, L, PosH, PosT):
    self.RadiusH = RH
    self.RadiusT = RT
    self.Length = L
    self.PosH = PosH
    self.PosT = PosT

    print "STLFlowAdapter.__init__"
