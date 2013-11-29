## @package biopredyn
## @author: $Author$
## @date: $Date$
## @copyright: $Copyright: [2013] BioPreDyn $
## @version: $Revision$

import libsbmlsim
import model, simulation, result

## Base representation of an atomic task in a SED-ML work flow.
class Task:
  ## @var id
  # A unique identifier associated with the object.
  ## @var model
  # Reference to the model this object is about.
  ## @var result
  # Result of the execution of the task.
  ## @var simulation
  # Reference to the simulation this object is about.
  ## @var tool
  # Reference to the software tool with which the task encoded by this object
  # has to be run.
  
  ## Constructor.
  # @param self The object pointer.
  # @param task A SED-ML task.
  # @param sedfile The SED-ML file from which the input task comes from.
  def __init__(self, task, sedfile):
    self.id = task.getId()
    self.model = model.SBMLModel(
      sedfile.getModel(task.getModelReference()).getSource())
    simu = sedfile.getSimulation(task.getSimulationReference())
    if simu.getElementName() == "uniformTimeCourse":
      self.simulation = simulation.UniformTimeCourse(simu)
    else:
      self.simulation = simulation.Simulation(simu)
    # TODO: set self.tool
  
  ## Default run function.
  # Uses libSBMLSim as simulation engine; encoded Task has to be a uniform
  # time course.
  # @param self The object pointer.
  def run(self):
    if ( self.simulation.get_type() == "uniformTimeCourse" ):
      steps = self.simulation.get_number_of_points()
      start = self.simulation.get_output_start_time()
      end = self.simulation.get_output_end_time()
      # "step" is computed with respect to the output start / end times, as
      # number_of_points is defined between these two points:
      step = (end - start) / steps
      # TODO: acquire KiSAO description of the algorithm - libKiSAO dependent
      r = libsbmlsim.simulateSBMLFromFile(
          self.model.get_address(),
          end,
          step,
          1,
          0,
          libsbmlsim.MTHD_RUNGE_KUTTA,
          0)
      # TODO: process the result - libNUML dependent
      self.result = result.LibSBMLSimResult(r)
    else:
      print "TODO"

  ## Getter. Returns self.id.
  # @param self The object pointer.
  # @return self.id
  def get_id(self):
    return self.id
  
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
  
  ## Getter. Returns self.tool.
  # @param self The object pointer.
  # @return self.tool
  def get_tool(self):
    return self.tool
  
  ## Setter. Assign a new value to self.model.
  # @param self The object pointer.
  # @param model New value for self.model.
  def set_model(self, model):
    self.model = model
  
  ## Setter. Assign a new value to self.simulation.
  # @param self The object pointer.
  # @param simulation New value for self.simulation.
  def set_simulation(self, simulation):
    self.simulation = simulation
  
  ## Setter. Assign a new value to self.tool.
  # @param self The object pointer.
  # @param tool New value for self.tool.
  def set_tool(self, tool):
    print "Task::set_tool - TODO"

## Task-derived class representing a task executed by CellNOpt.wrapper.
class CellNOptTask(Task):

  ## Execute the task.
  # @param self The object pointer.
  def run(self):
    print "CellNOptTask::run - TODO"

## Task-derived class representing a task executed by openCobra.
class CobraTask(Task):

  ## Execute the task.
  # @param self The object pointer.
  def run(self):
    print "CobraTask::run - TODO"

## Task-derived class representing a task executed by COPASI.
class CopasiTask(Task):

  ## Execute the task.
  # @param self The object pointer.
  def run(self):
    # TODO: direct copy/paste from the not-so-long dead CopasiFlow class; to
    # be fixed.
    if ( sed_simulation.getElementName() == "uniformTimeCourse" ):
      cop_task = cop_datamodel.addTask(COPASI.CCopasiTask.timeCourse)
      cop_problem = cop_task.getProblem()
      # Required parameters are set from values in the input SED-ML file
      cop_problem.setDuration( sed_simulation.getOutputEndTime() -
                       sed_simulation.getOutputStartTime() )
      cop_problem.setStepNumber(sed_simulation.getNumberOfPoints())
      cop_problem.setOutputStartTime(sed_simulation.getOutputStartTime())
      cop_problem.setTimeSeriesRequested(True)
      # Deterministic method is chosen
      # TODO: acquire it from KiSAO value in SED-ML file
      cop_task.setMethodType(COPASI.CCopasiMethod.deterministic)
      # Run
      cop_task.process(True)
      # Save the results
      self.series = cop_task.getTimeSeries()
    else:
      # TODO: case of a generic simulation element
      print("Something to be done with Simulation element here")
