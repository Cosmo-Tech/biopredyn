## @package biopredyn
## @author: $Author$
## @date: $Date$
## @copyright: $Copyright: [2013] BioPreDyn $
## @version: $Revision$

## Base class for N-dimensional data set description.
class Data:
  ## @var id
  # A unique identifier.
  
  ## Constructor.
  # @param self The object pointer.
  # @param id ID of the 
  def __init__(self, id):
    self.id = id
  
  ## Getter. Returns self.id.
  # @param self The object pointer.
  def get_id(self):
    return self.id

class Curve(Data):
  
  def __init__(self):
    print "TODO"

class Surface(Data):
  
  def __init__(self):
    print "TODO"