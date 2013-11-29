## @package biopredyn
## @author: $Author$
## @date: $Date$
## @copyright: $Copyright: [2013] BioPreDyn $
## @version: $Revision$

import libsedml

class Parameter:
  ## @var id
  # A unique identifier for this object.
  ## @var name
  # Name of this object.
  
  ## Constructor.
  # @param self The object pointer.
  # @param variable A SED-ML parameter element.
  def __init__(self, parameter):
    self.id = parameter.getId()
    self.name = parameter.getName()
  
  ## Getter. Returns self.id.
  # @param self The object pointer.
  def get_id(self):
    return self.id
  
  ## Getter. Returns self.name.
  # @param self The object pointer.
  def get_name(self):
    return self.name