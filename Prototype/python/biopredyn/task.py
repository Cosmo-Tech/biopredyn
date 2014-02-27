#!/usr/bin/env python

## @package biopredyn
## $Author$
## $Date$
## $Copyright: 2014, The CoSMo Company, All Rights Reserved $
## $License: BSD 3-Clause $
## $Revision$

import libsbmlsim
import model, simulation, result

## Abstract representation of an atomic task in a SED-ML work flow.
class AbstractTask:
  ## @var id
  # A unique identifier associated with the object.
  ## @var name
  # Name of this object.

  ## Constructor.
  # @param task A SED-ML task.
  def __init__(self, task):
    self.id = task.getId()
    self.name = task.getName()

  ## Getter. Returns self.id.
  # @param self The object pointer.
  # @return self.id
  def get_id(self):
    return self.id
  
  ## Getter. Returns self.name.
  # @param self The object pointer.
  def get_name(self):
    return self.name
  
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

## AbstractTask-derived class for atomic executable tasks in SED-ML work flows.
class Task(AbstractTask):
  ## @var model_id
  # ID of the model this object is about.
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
    AbstractTask.__init__(self, task)
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

## AbstractTask-derived class for nested loops of tasks in SED-ML work flows.
class RepeatedTask(AbstractTask):
  ## @var workflow
  # Reference to the WorkFlow object this belongs to.
  ## @var changes
  # A list of Change objects.
  ## @var ranges
  # A list of Range objects.
  ## @var subtasks
  # A list of AbstractTask objects.
  
  ## Constructor.
  # @param self The object pointer.
  # @param task A SED-ML repeatedTask element.
  # @param workflow 
  def __init__(self, task, workflow):
    AbstractTask.__init__(self, task)
    self.workflow = workflow
    self.changes = []
    self.ranges = []
    self.subtasks = []