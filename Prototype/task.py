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
  ## @var result
  # Result of the execution of the task.
  ## @var simulation
  # Reference to the simulation this object is about.
  
  ## Constructor.
  # @param self The object pointer.
  # @param task A SED-ML task.
  # @param sedfile The SED-ML file from which the input task comes from.
  def __init__(self, task, sedfile):
    self.model = model.SBMLModel(sedfile.getModel(task.getModelReference()))
    self.simulation = simulation.Simulation(
      sedfile.getSimulation(task.getSimulationReference()))
  
  ## Getter. Returns self.model.
  # @param self The object pointer.
  # @return self.model
  def get_model(self):
    return self.model
  
  ## Getter. Returns self.result.
  # @param self The object pointer.
  # @return self.result
  def get_result(self):
    return self.result
  
  ## Getter. Returns self.simulation.
  # @param self The object pointer.
  # @return self.simulation
  def get_simulation(self):
    return self.simulation

## Task-derived class representing a task executed by CellNOpt.wrapper.
class CellNOptTask(Task):

  ## Execute the task.
  # @param self The object pointer.
  def run(self):
    print "TODO"

## Task-derived class representing a task executed by openCobra.
class CobraTask(Task):

  ## Execute the task.
  # @param self The object pointer.
  def run(self):
    print "TODO"

## Task-derived class representing a task executed by COPASI.
class CopasiTask(Task):

  ## Execute the task.
  # @param self The object pointer.
  def run(self):
    print "TODO"
