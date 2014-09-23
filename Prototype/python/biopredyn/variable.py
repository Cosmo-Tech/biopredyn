#!/usr/bin/env python
# coding=utf-8

## @package biopredyn
## $Author$
## $Date$
## $Copyright: 2014, The CoSMo Company, All Rights Reserved $
## $License: BSD 3-Clause $
## $Revision$

import libsbml
import libsedml

## Base representation of a model variable in a SED-ML work flow.
class Variable:
  ## @var id
  # A unique identifier for this object.
  ## @var model_id
  # ID of the Model object this refers to.
  ## @var name
  # Name of this object.
  ## @var symbol
  # URN symbol for implicit variable representation. So far only two symbols
  # are used in BioPreDyn: urn:sedml:symbol:time (for time steps) and
  # urn:sedml:symbol:fluxes (for flux balance analysis results).
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
  # @param variable A libsedml.SedVariable object.
  # @param workflow A WorkFlow object.
  def __init__(self, variable, workflow):
    self.id = variable.getId()
    self.name = variable.getName()
    self.target = variable.getTarget()
    self.workflow = workflow
    self.symbol = variable.getSymbol()
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
    if self.task_id is not None:
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
  
  ## Returns the number of experiments in the numerical results produced by
  ## self.task for the species self.id.
  # @param self The object pointer.
  # @return An integer.
  def get_num_experiments(self):
    return self.get_task().get_num_experiments(self.id)
  
  ## Returns the number of time points of the numerical results produced by
  # self.task; it is equal to the number of points of its associated simulation
  # plus one point, as described in the SED-ML specifications.
  # @param self The object pointer.
  # @return The number of time points.
  def get_number_of_points(self):
    return self.get_task().get_simulation().get_number_of_points() + 1
  
  ## Getter. Returns self.symbol.
  # @param self The object pointer.
  # @return self.symbol
  def get_symbol(self):
    return self.symbol
  
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
  
  ## Return the numerical values corresponding to the Result object in
  ## the Task object of self.workflow which ID is self.task_id. If self.symbol
  ## indicates a time series, returns the time steps associated with this same
  ## Task object instead. If self.symbol indicates a vector of fluxes, the Task
  ## object is encoding a flux balance analysis; in this case the resulting
  ## vector of fluxes is returned.
  # @param self The object pointer.
  # @return values A 1-dimensional array of numerical values.
  def get_values(self):
    task = self.get_task()
    values = []
    if self.symbol == "urn:sedml:symbol:time":
      values = task.get_result().get_time_steps()
    elif self.symbol == "urn:sedml:symbol:fluxes":
      values = task.get_result().get_fluxes()
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
  
  ## Setter for self.target.
  # @param self The object pointer.
  # @param target New value for self.target.
  def set_target(self, target):
    self.target = target
  
  ## Setter for self.symbol.
  # @param self The object pointer.
  # @param symbol New value for self.symbol.
  def set_symbol(self, symbol):
    self.symbol = symbol
  
  ## Setter for self.task_id.
  # @param self The object pointer.
  # @param task_id New value for self.task_id.
  def set_task_id(self, task_id):
    self.task_id = task_id
  
  ## Setter for self.model_id.
  # @param self The object pointer.
  # @param model_id New value for self.model_id.
  def set_model_id(self, model_id):
    self.model_id = model_id
