## @package biopredyn
## @author: $Author$
## @date: $Date$
## @copyright: $Copyright: [2013] BioPreDyn $
## @version: $Revision$

## Base class for N-dimensional data set description.
class DataGenerator:
  ## @var id
  # A unique identifier.
  
  ## Constructor.
  # @param self The object pointer.
  # @param data_generator A SED-ML dataGenerator element.
  # @param workflow A WorkFlow object.
  def __init__(self, data_generator, workflow):
    self.id = id
  
  ## Getter. Returns self.id.
  # @param self The object pointer.
  def get_id(self):
    return self.id

## DataGenerator-derived class for 2-dimensional data set description.
class Curve(DataGenerator):
  
  ## Overridden constructor.
  # @param self The object pointer.
  # @param curve A SED-ML curve element.
  # @param workflow A WorkFlow object.
  def __init__(self, curve, workflow):
    print "Curve constructor - TODO"

## DataGenerator-derived class for 3-dimensional data set description.
class Surface(DataGenerator):
  
  ## Overridden constructor.
  # @param self The object pointer.
  # @param surface A SED-ML surface element.
  # @param workflow A WorkFlow object.
  def __init__(self, surface, workflow):
    print "Surface constructor - TODO"