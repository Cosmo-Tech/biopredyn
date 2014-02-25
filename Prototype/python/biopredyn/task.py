#!/usr/bin/env python

## @package biopredyn
## $Author$
## $Date$
## $Copyright: 2014, The CoSMo Company, All Rights Reserved $
## $License$
## $Revision$

import libsbmlsim
import model, simulation, result

## Base representation of an atomic task in a SED-ML work flow.
class Task:
  ## @var id
  # A unique identifier associated with the object.
  ## @var model_id
  # ID of the model this object is about.
  ## @var name
  # Name of this object.
  ## @var result
  # Result of the execution of the task.
  ## @var simulation_id
  # ID of the simulation this object is about.
  ## @var workflow
  # Reference to the WorkFlow object this belongs to.
  
  ## Constructor.
  # @param self The object pointer.
  # @param task A SED-ML task.
  # @param workflow The WorkFlow object this.
  def __init__(self, task, workflow):
    self.id = task.getId()
    self.name = task.getName()
    self.workflow = workflow
    self.model_id = task.getModelReference()
    self.simulation_id = task.getSimulationReference()
  
  ## String representation of this. Displays it as a hierarchy.
  # @param self The object pointer.
  # @return A string representing this as a hierarchy.
  def __str__(self):
    tree = "  |-task id=" + self.id + " name=" + self.name
    tree += " modelReference=" + self.model_id
    tree += " simulationReference=" + self.simulation_id + "\n"
    return tree
  
  ## Default run function.
  # Uses libSBMLSim as simulation engine; encoded Task has to be a uniform
  # time course.
  # @param self The object pointer.
  def run(self):
    model = self.get_model()
    simulation = self.get_simulation()
    # First of all changes must be applied to the model
    model.apply_changes()
    if ( simulation.get_type() == "uniformTimeCourse" ):
      steps = simulation.get_number_of_points()
      start = simulation.get_output_start_time()
      end = simulation.get_output_end_time()
      # "step" is computed with respect to the output start / end times, as
      # number_of_points is defined between these two points:
      step = (end - start) / steps
      # TODO: acquire KiSAO description of the algorithm - libKiSAO dependent
      r = libsbmlsim.simulateSBMLFromString(
          model.get_sbml_doc().toSBML(),
          end,
          step,
          1,
          0,
          libsbmlsim.MTHD_RUNGE_KUTTA,
          0)
      self.result = result.Result()
      self.result.import_from_libsbmlsim(r)
    else:
      # TODO: other types of simulation
      print "TODO"
    # Model is reinitialized
    model.init_tree()

  ## Getter. Returns self.id.
  # @param self The object pointer.
  # @return self.id
  def get_id(self):
    return self.id
  
  ## Returns the Model objet of self.workflow which id is self.model_id.
  # @param self The object pointer.
  # @return A Model object.
  def get_model(self):
    return self.workflow.get_model_by_id(self.model_id)
  
  ## Getter. Returns self.model_id.
  # @param self The object pointer.
  # @return self.model_id
  def get_model_id(self):
    return self.model_id
  
  ## Getter. Returns self.name.
  # @param self The object pointer.
  def get_name(self):
    return self.name
  
  ## Getter. Returns self.result.
  # @param self The object pointer.
  # @return self.result
  def get_result(self):
    return self.result
  
  ## Returns the Simulation objet of self.workflow which id is
  ## self.simulation_id.
  # @param self The object pointer.
  # @return A Simulation object.
  def get_simulation(self):
    return self.workflow.get_simulation_by_id(self.simulation_id)
  
  ## Getter. Returns self.simulation_id.
  # @param self The object pointer.
  # @return self.simulation_id
  def get_simulation_id(self):
    return self.simulation_id
  
  ## Getter. Returns self.tool.
  # @param self The object pointer.
  # @return self.tool
  def get_tool(self):
    return self.tool
  
  ## Setter for self.id.
  # @param self The object pointer.
  # @param id New value for self.id.
  def set_id(self, id):
    self.id = id
  
  ## Setter for self.name.
  # @param self The object pointer.
  # @param name New value for self.name.
  def set_name(self, name):
    self.name = name
  
  ## Setter. Assign a new value to self.model_id.
  # @param self The object pointer.
  # @param model_id New value for self.model_id.
  def set_model_id(self, model_id):
    self.model_id = model_id
  
  ## Setter. Assign a new value to self.simulation_id.
  # @param self The object pointer.
  # @param simulation_id New value for self.simulation_id.
  def set_simulation_id(self, simulation_id):
    self.simulation_id = simulation_id
  
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
