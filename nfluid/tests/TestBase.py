from NF_ChannelAssembly import *
import os

def MakeTest1(assembly):

  print "resolveGeometry ----------------------------------"
  res = assembly.resolveGeometry()
  print "resolveGeometry res = ", "|", res, "|"

  print "Test Geometry ------------------------------------"
  res = assembly.isResolvedGeometry()
  if res == "":
    print "Geometry resolved"
  else:
    print "-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-"
    print "Geometry error res = ", res
    print "-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-"

  print "\n\nPrint Assembly ---------------------------------"
  assembly.Print()

