from nfluid.util.operator import *

#--------------------------------------------------------------------
def GetRotationMatrixAxisAngleRad(aaxis, angle):
#--------------------------------------------------------------------
  Res = Operator()
  axis = copy.copy(aaxis)
  axis.normalize()

  SinA = math.sin(angle)
  CosA = math.cos(angle)

  Res.setA(0,0, CosA + axis.x * axis.x * (1 - CosA))
  Res.setA(0,1, axis.x * axis.y * (1 - CosA) - axis.z * SinA)
  Res.setA(0,2, axis.x * axis.z * (1 - CosA) + axis.y * SinA)

  Res.setA(1,0, axis.y * axis.x * (1 - CosA) + axis.z * SinA)
  Res.setA(1,1, CosA + axis.y * axis.y * (1 - CosA))
  Res.setA(1,2, axis.y * axis.z * (1 - CosA) - axis.x * SinA)

  Res.setA(2,0, axis.z * axis.x * (1 - CosA) - axis.y * SinA)
  Res.setA(2,1, axis.z * axis.y * (1 - CosA) + axis.x * SinA)
  Res.setA(2,2, CosA + axis.z * axis.z * (1 - CosA))

  Res.round()

  return Res

#--------------------------------------------------------------------
def GetRotationMatrixAxisAngleGrad(axis, angle):
  return GetRotationMatrixAxisAngleRad(axis, math.radians(angle))

#--------------------------------------------------------------------
def GetRotationMatrixVectorToVector(From, To, AxisExt = None):
#--------------------------------------------------------------------
#STUB!!! What to do if Len == 0
  print "GetRotationMatrixVectorToVector From ", From
  print "GetRotationMatrixVectorToVector To", To
  axis = vector_product(From, To).normalize()
  if is_equal_eps(axis.get_len(), 0):
    if scalar_product(From, To) > 0:
      return Operator()

    if AxisExt is not None:
      axis = AxisExt
    else:
      print "GetRotationMatrixVectorToVector !!!! Axix not defined"
  angle = get_vector_angle_rad(From, To)
  print "GetRotationMatrixVectorToVector axis ", axis
  print "GetRotationMatrixVectorToVector angle", math.degrees(angle)
  return GetRotationMatrixAxisAngleRad(axis, angle)

#--------------------------------------------------------------------
def GetRotationMatrixVectorFaceToVector(From, To, Axis):
#--------------------------------------------------------------------
  Res = Operator()

  print "GetRotationMatrixVectorFaceToVector From ", From
  print "GetRotationMatrixVectorFaceToVector To", To
  print "GetRotationMatrixVectorFaceToVector Axis", Axis

  FromOrt = get_orthogonal(From, Axis)
  ToOrt = get_orthogonal(To, Axis)

  print "GetRotationMatrixVectorFaceToVector FromOrt", FromOrt
  print "GetRotationMatrixVectorFaceToVector ToOrt", ToOrt

  if is_equal_eps(FromOrt.get_len(), 0):
    return None, "Vector 'From' is colinear to the rotation axis"
  if is_equal_eps(ToOrt.get_len(), 0):
    return None, "Vector 'To' is colinear to the rotation axis"

  return GetRotationMatrixVectorToVector(FromOrt, ToOrt, Axis), "" 

