from ChannelAssembly import *
import os

def MakeTest1(assembly):

  print "resolve_geometry ----------------------------------"
  res = assembly.resolve_geometry()
  print "resolve_geometry res = ", "|", res, "|"

  print "Test Geometry ------------------------------------"
  res = assembly.is_resolved_geometry()
  if res == "":
    print "Geometry resolved"
  else:
    print "-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-"
    print "Geometry error res = ", res
    print "-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-"

  print "\n\nprint_info Assembly ---------------------------------"
  assembly.print_info()

