## @package biopredyn
## @author: $Author$
## @date: $Date$
## @copyright: $Copyright: [2013] BioPreDyn $
## @version: $Revision$

import model, simulation

## Base representation of an atomic task in a SED-ML work flow.
class Task:
  ## @var model
  # Reference to the model this object is about.
  ## @var simulation
  # Reference to the simulation this object is about.
  ## @var result
  # Result of the execution of the task.
  
  ## Constructor.
  # @param self The object pointer.
  # @param task A SED-ML task.
  # @param sedfile The SED-ML file from which the input task comes from.
  def __init__(self, task, sedfile):
    self.model = model.SBMLModel(sedfile.getModel(task.getModelReference()))
    self.simulation = simulation.Simulation(
      sedfile.getSimulation(task.getSimulationReference()))
  
  ## Execute the task.
  # @param self The object pointer.
  def run(self):
    print "TODO"