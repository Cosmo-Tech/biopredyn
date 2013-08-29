## @package biopredyn
# Work flow handling package; a work flow is defined as a sequence of Task
# elements (in the SED-ML sense) to be executed using one or several engines.

__author__ = "$Author$"
__date__ = "$Date$"
__copyright__ = "$Copyright: [2013] BioPreDyn $"
__credits__ = ["Bertrand Moreau"]
__license__ = "BSD"
__maintainer__ = ["Bertrand Moreau"]
__email__ = "bertrand.moreau@thecosmocompany.com"
__version__ = "$Revision$"

import lisbmlsim
import COPASI

## Result class for libSBMLSim runs.
class LibSBMLSimResult:
  
  ## Constructor.
  # @param self The object pointer.
  # @param result The result of a libSBMLSim run.
  def __init__(self, result):
    self.result = result
  
  ## Returns a list containing all the quantity values for the input species
  ## over time.
  # @param self The object pointer.
  # @param species The species which quantity values are wanted. 
  def get_quantities_per_species(self, species):
    quantities = []
    for i in range(self.result.getNumOfRows()):
      quantities.append(self.result.getSpeciesValueAtIndex(species, i))
    return quantities
  
  ## Returns the list of all time steps in self.result.
  # @param self The object pointer.
  def get_time_steps(self):
    time = []
    for i in range(self.result.getNumOfRows()):
      time.append(self.result.getTimeValueAtIndex(i))
    return time

## Result class for COPASI runs.
class CopasiResult:
  
  ## Constructor.
  # @param self The object pointer.
  # @param result The result of a COPASI run.
  def __init__(self, result):
    self.result = result