#!/usr/bin/env python

## @package biopredyn
## $Author$
## $Date$
## $Copyright: 2014, The CoSMo Company, All Rights Reserved $
## $License$
## $Revision$

import libsedml

## Base representation of a model variable in a SED-ML work flow.
class Variable:
  ## @var id
  # A unique identifier for this object.
  ## @var model_id
  # ID of the Model object this refers to.
  ## @var name
  # Name of this object.
  ## @var target
  # XPath expression pointing to the element this variable refers to in
  # self.model.
  ## @var task_id
  # ID of the Task object this refers to.
  ## @var workflow
  # Reference to the WorkFlow object this refers to.
  
  ## Constructor. Depending on the content of the input variable, one of the
  ## input workflow or model arguments must exist.
  # @param self The object pointer.
  # @param variable A SED-ML variable element.
  # @param workflow A WorkFlow object.
  def __init__(self, variable, workflow):
    self.id = variable.getId()
    self.name = variable.getName()
    self.target = variable.getTarget()
    self.workflow = workflow
    if variable.isSetTaskReference():
      # DataGenerator case
      self.task_id = variable.getTaskReference()
    elif variable.isSetModelReference():
      # ComputeChange case
      self.model_id = variable.getModelReference()
    else:
      print(
            "Invalid 'variable' argument; at least one of the taskReference" +
            " or modelReference attributes must exist in the input Variable" +
            " element."
            )
  
  ## String representation of this. Displays it as a hierarchy.
  # @param self The object pointer.
  # @return A string representing this as a hierarchy.
  def __str__(self):
    tree = "      |-variable id=" + self.id + " name=" + self.name
    if self.task is not None:
      tree += " taskReference=" + self.task_id + "\n"
    else:
      tree += " modelReference=" + self.model_id + "\n"
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
  
  ## Returns the Model objet of self.workflow which id is self.model_id.
  # @param self The object pointer.
  # @return A Model object.
  def get_model(self):
    if self.model_id is not None:
      return self.workflow.get_model_by_id(self.model_id)
    else:
      task = self.get_task()
      return task.get_model()
  
  ## Getter. Returns self.model_id.
  # @param self The object pointer.
  # @return self.model_id
  def get_model_id(self):
    return self.model_id
  
  ## Returns the number of time points of the numerical results produced by
  # self.task.
  # @param self The object pointer.
  # @return The number of time points.
  def get_number_of_points(self):
    task = self.workflow.get_task_by_id(self.task_id)
    return task.get_simulation().get_number_of_points()
  
  ## Getter for self.target.
  # @param self The object pointer.
  # @return self.target
  def get_target(self):
    return self.target
  
  ## Returns the Task objet of self.workflow which id is self.task_id.
  # @param self The object pointer.
  # @return A Task object.
  def get_task(self):
    return self.workflow.get_task_by_id(self.task_id)

  ## Getter. Returns self.task_id.
  # @param self The object pointer.
  # @return self.task_id
  def get_task_id(self):
    return self.task_id
  
  ## Return the numerical results associated with this as an array, if they
  # exist.
  # @param self The object pointer.
  # @return values A 1-dimensional array of numerical values.
  def get_values(self):
    task = self.get_task()
    values = []
    if self.id.upper() == "TIME":
      values = task.get_result().get_time_steps()
    else:
      values = task.get_result().get_quantities_per_species(self.id)
    return values
  
  ## Return the numerical value pointed by self.target in the Model object
  ## corresponding to self.model_id, if it exists.
  # @param self The object pointer.
  # @return value A numerical value.
  def get_xpath_value(self):
    model = self.get_model()
    target = model.evaluate_xpath(self.target)
    value = float(target[0])
    return value