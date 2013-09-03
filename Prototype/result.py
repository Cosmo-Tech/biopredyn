## @package biopredyn
## @author: $Author$
## @date: $Date$
## @copyright: $Copyright: [2013] BioPreDyn $
## @version: $Revision$

import COPASI

## Result class for libSBMLSim runs.
class LibSBMLSimResult:
  ## @var result
  # A matrix of values resulting from a libSBMLSim simulation run.
  
  ## Constructor.
  # @param self The object pointer.
  # @param result The result of a libSBMLSim run.
  def __init__(self, result):
    self.result = result
  
  ## Returns a list containing all the quantity values for the input species
  ## over time.
  # @param self The object pointer.
  # @param species The species which quantity values are wanted. 
  # @return A list of quantity values for the input species over time.
  def get_quantities_per_species(self, species):
    quantities = []
    for i in range(self.result.getNumOfRows()):
      quantities.append(self.result.getSpeciesValueAtIndex(species, i))
    return quantities
  
  ## Returns the list of all time steps in self.result.
  # @param self The object pointer.
  # @return The list of time steps.
  def get_time_steps(self):
    time = []
    for i in range(self.result.getNumOfRows()):
      time.append(self.result.getTimeValueAtIndex(i))
    return time

## Result class for COPASI runs.
class CopasiResult:
  ## @var result
  # A time series resulting from a COPASI simulation run.
  
  ## Constructor.
  # @param self The object pointer.
  # @param result The result of a COPASI run.
  def __init__(self, result):
    self.result = result