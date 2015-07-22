import sys
import unittest
from nfluid.core.channel_assembly import *
#====================================================================

def RunAllTests(test_class):
  result = unittest.TestResult() 
  test_class.suite().run(result)
  print "Total tests:", result.testsRun, "Succsessful:", result.wasSuccessful()

def GetHelp(test_class):
  suite = test_class.suite()
  for i, test in enumerate(suite):
    print i, " - ", test.id()

#====================================================================
class NFT_UnittestBase(unittest.TestCase):
#--------------------------------------------------------------------
  def setUp(self):
      print "setUp"
      self.assembly = ChannelAssembly()

#--------------------------------------------------------------------
  def tearDown(self):
      print "tearDown"

#--------------------------------------------------------------------
  def process_chain(self):
#--------------------------------------------------------------------
    print "Hello process_chain"
    print "resolve_geometry ----------------------------------"
    res = self.assembly.resolve_geometry()
    if res != "":
      print "-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-"
      print "resolve_geometry res = ", "|", res, "|"
      print "-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-"
    
    print "\n\nprint_info Assembly ---------------------------"
    self.assembly.print_info()
    
    print "Test Geometry -------------------------------------"
    res = self.assembly.is_resolved_geometry()
    if res == "":
      print "Geometry resolved"
    else:
      print "-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-"
      print "Geometry error res = ", res
      print "-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-"
      exit()
    
    res = self.assembly.create_shapes()
    if res == "":
      print "Shapes created"
    else:
      print "-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-"
      print "Shapes creation error res = ", res
      print "-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-"
    
    res = self.assembly.export("Test1.stl")
    if res == "":
      print "Shapes exported"
    else:
      print "-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-"
      print "Shapes export error res = ", res
      print "-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-"
    
    self.assembly.show_shapes()
    
    self.assembly.release_shapes()



