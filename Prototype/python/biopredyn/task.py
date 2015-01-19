#!/usr/bin/env python
# coding=utf-8

## @package biopredyn
## $Author$
## $Date$
## $Copyright: 2014, The CoSMo Company, All Rights Reserved $
## $License: BSD 3-Clause $
## $Revision$

import model, simulation, result, change, ranges

## Abstract representation of an atomic task in a SED-ML work flow.
class AbstractTask:
  ## @var id
  # A unique identifier associated with the object.
  ## @var name
  # Name of this object.
  ## @var tool
  # Name of the tool to be used when calling the run function.

  ## Constructor.
  # @param self The object pointer.
  # @param task A SED-ML task.
  def __init__(self, task):
    self.id = task.getId()
    self.name = task.getName()
    self.tool = None

  ## Getter. Returns self.id.
  # @param self The object pointer.
  # @return self.id
  def get_id(self):
    return self.id
  
  ## Getter. Returns self.name.
  # @param self The object pointer.
  def get_name(self):
    return self.name
  
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
  
  ## Setter. Assign a new value to self.tool.
  # @param self The object pointer.
  # @param tool New value for self.tool.
  def set_tool(self, tool):
    self.tool = tool

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
    self.result = None
  
  ## String representation of this. Displays it as a hierarchy.
  # @param self The object pointer.
  # @return A string representing this as a hierarchy.
  def __str__(self):
    tree = "  |-task id=" + self.id + " name=" + self.name
    tree += " modelReference=" + self.model_id
    tree += " simulationReference=" + self.simulation_id + "\n"
    return tree
  
  ## Run self.simulation on self.model using self.tool as a simulation engine.
  ## Results are stored as self.result.
  # @param self The object pointer.
  # @param apply_changes Boolean value; if true, changes of the model apply
  # before the simulation run, otherwise they do not.
  def run(self, apply_changes):
    model = self.get_model()
    # self.result must be initialized if it does not exist yet
    if self.result is None:
      sim_type = self.get_simulation().get_type()
      if sim_type == 'uniformTimeCourse' or sim_type == 'oneStep':
        self.result = result.TimeSeries()
      elif sim_type == 'steadyState':
        self.result = result.Fluxes()
    # Changes must be applied to the model
    if apply_changes:
      model.apply_changes()
    self.get_simulation().run(model, self.tool, self.result)
  
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
  
  ## Returns the maximum number of experiment in self.result.
  # @param self The object pointer.
  # @param species The species which dimensionality is required.
  # @return An integer.
  def get_num_experiments(self, species):
    return self.result.get_num_experiments(species)
  
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

## AbstractTask-derived class for nested loops of tasks in SED-ML work flows.
class RepeatedTask(AbstractTask):
  ## @var workflow
  # Reference to the WorkFlow object this belongs to.
  ## @var changes
  # A list of Change objects.
  ## @var master_range
  # Reference to the reference Range object in self.ranges; it cannot be a
  # FunctionalRange, as it should define a number of iterations.
  ## @var ranges
  # A list of Range objects.
  ## @var reset_model
  # Boolean value stating whether the model should be reset between two
  # repetitions of the task.
  ## @var subtasks
  # A list of AbstractTask objects.
  
  ## Constructor.
  # @param self The object pointer.
  # @param task A SED-ML repeatedTask element.
  # @param workflow 
  def __init__(self, task, workflow):
    AbstractTask.__init__(self, task)
    self.workflow = workflow
    self.reset_model = task.getResetModel()
    self.master_range = task.getRangeId()
    self.changes = []
    for c in task.getListOfTaskChanges():
      # Change objects in RepeatedTask objects can only be SetValue objects
      self.changes.append(change.SetValue(c, self, workflow))
    self.ranges = []
    for r in task.getListOfRanges():
      r_name = r.getElementName()
      if r_name == "functionalRange":
        self.ranges.append(ranges.FunctionalRange(r, workflow, self))
      elif r_name == "uniformRange":
        self.ranges.append(ranges.UniformRange(r))
      elif r_name == "vectorRange":
        self.ranges.append(ranges.VectorRange(r))
      else:
        self.ranges.append(ranges.Range(r))
    self.subtasks = []
    for s in task.getListOfSubTasks():
      self.subtasks.append(SubTask(s, workflow))
    self.subtasks.sort()
  
  ## Getter. Returns a range referenced by the input id listed in self.ranges.
  # @param self The object pointer.
  # @param id The id of the range to be returned.
  # @return range A range object.
  def get_range_by_id(self, id):
    for r in self.ranges:
      if r.get_id() == id:
        return r
    print("Range not found: " + id)
    return 0
  
  ## Run the repeated task.
  # The following operations are executed at each iteration defined by
  # self.master_range:
  #  1. If self.reset_model is True, the model is reset.
  #  2. Each SetValue change in self.changes is executed.
  #  3. Each SubTask in self.subtasks is executed.
  # @param self The object pointer.
  # @param apply_changes Boolean value; if true, changes of the model apply
  # before each sub task simulation run, otherwise they do not.
  def run(self, apply_changes):
    num_iter = len(self.get_range_by_id(self.master_range).get_values())
    # Main loop
    for i in range(num_iter):
      # 1. Models initialization
      if self.reset_model == True:
        # All model references in self.subtasks are retrieved
        models = []
        for s in self.subtasks:
          model_ref = s.get_task().get_model_id()
          if model_ref not in models:
            models.append(model_ref)
        # All models are reset
        for m in models:
          self.workflow.get_model_by_id(m).init_tree()
      else:
        apply_changes = False
      # 2. Changes are executed
      for c in self.changes:
        c.apply(i)
      # 3. Sub-tasks are executed
      for t in self.subtasks:
        t.run(apply_changes)

## Base-class for RepeatedTask element sub-tasks.
class SubTask:
  ## @var order
  # Order of execution of this object (relatively to the SubTask objects of the
  # same RepeatedTask object).
  ## @var task_id
  # ID of the AbstractTask object this object refers to.
  ## @var workflow
  # Reference to the WorkFlow object this object belongs to.
  
  ## Constructor.
  # @param self The object pointer.
  # @param subtask A SED-ML subTask element.
  # @param workflow A WorkFlow object.
  def __init__(self, subtask, workflow):
    self.order = subtask.getOrder()
    self.task_id = subtask.getTask()
    self.workflow = workflow
  
  ## Comparison operator (order wise).
  # @param self The object pointer.
  # @param other A SubTask object.
  # @return -1 if self.get_order() is smaller than other.get_order(), 1 if
  # self.get_order() is greater, 0 otherwise.
  def __cmp__(self, other):
    self_order = float(self.get_order())
    other_order = float(other.get_order())
    if self_order < other_order:
      return -1
    elif self_order > other_order:
      return 1
    else:
      return 0
  
  ## Getter for self.order.
  # @param self The object pointer.
  # @return self.order
  def get_order(self):
    return self.order
  
  ## Returns the Task object in self.workflow which ID is self.task_id, if it
  ## exists.
  # @param self The object pointer.
  # @return An AbstractTask object.
  def get_task(self):
    return self.workflow.get_task_by_id(self.task_id)
  
  ## Getter for self.task_id.
  # @param self The object pointer.
  # @return self.task_id
  def get_task_id(self):
    return self.task_id
  
  ## Calls the Task object of self.workflow which id is self.task_id.
  # @param self The object pointer.
  # @param apply_changes Boolean value; if true, changes of the model apply
  # before the simulation run, otherwise they do not.
  def run(self, apply_changes):
    self.get_task().run(apply_changes)
  
  ## Setter for self.order.
  # @param self The object pointer.
  # @param order New value for self.order.
  def set_order(self, order):
    self.order = order
  
  ## Setter for self.task_id.
  # @param self The object pointer.
  # @param task_id New value for self.task_id.
  def set_task_id(self, task_id):
    self.task_id = task_id
