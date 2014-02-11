# coding=utf-8

## @package biopredyn
## @author: $Author$
## @date: $Date$
## @copyright: $Copyright: [2013-2014] BioPreDyn $
## @version: $Revision$

import libsedml

## Base representation of a model variable in a SED-ML work flow.
class Variable:
  ## @var id
  # A unique identifier for this object.
  ## @var model
  # Reference to the Model object this refers to.
  ## @var name
  # Name of this object.
  ## @var target
  # XPath expression pointing to the element this variable refers to in
  # self.model.
  ## @var task
  # Reference to the Task object this refers to.
  
  ## Constructor. Depending on the content of the input variable, one of the
  ## input workflow or model arguments must exist.
  # @param self The object pointer.
  # @param variable A SED-ML variable element.
  # @param workflow A WorkFlow object (default None).
  # @param model A Model object (default None).
  def __init__(self, variable, workflow=None, model=None):
    self.id = variable.getId()
    self.name = variable.getName()
    self.target = variable.getTarget()
    model_ref = variable.getModelReference()
    task_ref = variable.getTaskReference()
    if task_ref is not None:
      if workflow is not None:
        self.task = workflow.get_task_by_id(variable.getTaskReference())
        self.model = self.task.get_model()
      else:
        print(
              "Error: workflow cannot be null when input Variable object" +
              "contains a taskReference attribute."
              )
    elif model_ref is not None:
      if model is not None:
        self.model = model
      elif workflow is not None:
        self.model = workflow.get_model_by_id(variable.getModelReference())
      else:
        print(
              "Error: at least one of the workflow or model input arguments" +
              " must exist."
              )
    else:
      print(
            "Invalid variable argument; at least one of the taskReference" +
            " or modelReference attributes must exist in the input Variable" +
            " element."
            )
  
  ## String representation of this. Displays it as a hierarchy.
  # @param self The object pointer.
  # @return A string representing this as a hierarchy.
  def __str__(self):
    tree = "      |-variable id=" + self.id + " name=" + self.name
    if self.task is not None:
      tree += " taskReference=" + self.task.get_id()
      tree += " modelReference=" + self.model.get_id() + "\n"
    else:
      tree += " modelReference=" + self.model.get_id() + "\n"
    return tree
  
  ## Getter. Returns self.id.
  # @param self The object pointer.
  # @return self.id
  def get_id(self):
    return self.id
  
  ## Getter. Returns self.name.
  # @param self The object pointer.
  # @return self.name
  def get_name(self):
    return self.name
  
  ## Getter. Returns self.model.
  # @param self The object pointer.
  # @return self.model
  def get_model(self):
    return self.model
  
  ## Returns the number of time points of the numerical results produced by
  # self.task.
  # @param self The object pointer.
  # @return The number of time points.
  def get_number_of_points(self):
    return self.task.get_simulation().get_number_of_points()
  
  ## Getter for self.target.
  # @param self The object pointer.
  # @return self.target
  def get_target(self):
    return self.target
  
  ## Getter. Returns self.task.
  # @param self The object pointer.
  # @return self.task
  def get_task(self):
    return self.task
  
  ## Return the numerical results associated with this as an array, if they
  # exist.
  # @param self The object pointer.
  # @return values A 1-dimensional array of numerical values.
  def get_values(self):
    values = []
    if self.id.upper() == "TIME":
      values = self.task.get_result().get_time_steps()
    else:
      values = self.task.get_result().get_quantities_per_species(self.id)
    return values