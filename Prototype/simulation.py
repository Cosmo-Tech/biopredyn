## @package biopredyn
## @author: $Author$
## @date: $Date$
## @copyright: $Copyright: [2013] BioPreDyn $
## @version: $Revision$

## Description of the execution of an algorithm, independent from the model or
## data set it has to be run with.
class Simulation:
  ## @var algorithm
  # KiSAO identifier of the algorithm to execute.
  
  ## Constructor.
  # @param self The object pointer.
  # @param simulation A SED-ML simulation.
  def __init__(self, simulation):
    self.algorithm = simulation.getAlgorithm().getKisaoID()
  
  ## Returns the KiSAO identifier of the algorithm to be executed.
  # @param self The object pointer.
  # @return self.algorithm
  def get_algorithm(self):
    return self.algorithm