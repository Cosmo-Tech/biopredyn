## @package biopredyn
## @author: $Author$
## @date: $Date$
## @copyright: $Copyright: [2013] BioPreDyn $
## @version: $Revision$

import libsedml
import variable, parameter

class DataGenerator:
  ## @var id
  # A unique identifier for this object.
  ## @var name
  # Name of this object.
  ## @var parameters
  # A list of Parameter objects.
  ## @var variables
  # A list of Variable objects.
  
  ## Constructor.
  # @param self The object pointer.
  # @param data_generator A SED-ML dataGenerator element.
  # @param workflow A WorkFlow object.
  def __init__(self, data_generator, workflow):
    self.id = data_generator.getId()
    self.name = data_generator.getName()
    # Parse the input data_generator object for parameters
    parameters = []
    for p in data_generator.getListOfParameters():
      parameters.append(parameter.Parameter(p))
    # Parse the input data_generator object for variables
    variables = []
    for v in data_generator.getListOfVariables():
      variables.append(variable.Variable(v, workflow))
  
  ## Getter. Returns self.id.
  # @param self The object pointer.
  def get_id(self):
    return self.id
  
  ## Getter. Returns self.name.
  # @param self The object pointer.
  def get_name(self):
    return self.name