from nfluid.core.channel_element import *
#====================================================================
class ChannelAssembly(object):
#--------------------------------------------------------------------
  def __init__(self):
    self.elements = []
    ChannelElement.assembly = self
    print "-------------------test_---"

#--------------------------------------------------------------------
  def add_element(self, element):
    self.elements.append(element)

#--------------------------------------------------------------------
  def for_each_element(self, fcn):
    for element in self.elements:
      fcn(element)

#--------------------------------------------------------------------
  def resolve_geometry(self):
#--------------------------------------------------------------------
    while True:
      print "resolve_geometry loop ---------------------------"
      Changed = False;
      for element in self.elements:
        if element.changed:
          print "resolve_geometry before --------"
          element.print_info()
          res = element.resolve_geometry()
          print "assembly.resolve_geometry res = ", res
          if res != "":
            if res == "ok":
              Changed = True
            else:
              return res
          print "resolve_geometry after --------"
          element.print_info()
          element.changed = False
      print "Changed", Changed
      if not Changed:
        break
    return self.is_resolved_geometry()

#--------------------------------------------------------------------        
  def is_resolved_geometry(self):
    for element in self.elements:
      res = element.is_resolved_geometry()
      if res != "":
        return res
    return ""

#--------------------------------------------------------------------
  def clear_geometry(self):
    for element in self.elements:
      element.clear_geometry()
      print "clear_geometry Assembly loop ---------------------------"        

#--------------------------------------------------------------------
  def print_info(self):
#--------------------------------------------------------------------
    for element in self.elements:
      print "New Assembly Element --------------------------- " + element.get_name()
      element.print_info()
      res = element.is_resolved_geometry()
      if res != "":
        print "-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-"
        print "GEOMETRY NOT RESOLVED: ", res 
        print "-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-"

#--------------------------------------------------------------------
  def create_shapes(self):
    for element in self.elements:
      res = element.create_shape()
      if res != "":
        return res
    return ""

#--------------------------------------------------------------------    
  def release_shapes(self):
    for element in self.elements:
      element.release_shape()

#--------------------------------------------------------------------
  def export(self, file_name):
  # open file
    file = open(file_name, "w")
    for element in self.elements:
      element.export(file)
  # close file
    file.close()
    return ""

#--------------------------------------------------------------------    
  def show_shapes(self):
    for element in self.elements:
      element.show_shape()

#--------------------------------------------------------------------      
def create_channel(elt):
  return elt
  
  
