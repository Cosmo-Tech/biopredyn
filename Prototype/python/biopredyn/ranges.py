#!/usr/bin/env python
# coding=utf-8

## @package biopredyn
## Copyright: [2012-2015] The CoSMo Company, All Rights Reserved
## License: BSD 3-Clause

import libsbml
import numpy as np
from sympy import *
import variable

## Base class for expressing ranges in SED-ML repeatedTask elements.
class Range:
  ## @var id
  # A unique identifier associated with the object.
  ## @var values
  # A range of values encoded by the element.
  
  ## Constructor.
  # @param self The object pointer.
  # @param range A SED-ML range element.
  def __init__(self, range):
    self.id = range.getId()
    self.values = []
  
  ## Getter for self.id.
  # @param self The object pointer.
  # @return self.id
  def get_id(self):
    return self.id
  
  ## Setter for self.id.
  # @param self The object pointer.
  # @param id A new value for self.id.
  def set_id(self, id):
    self.id = id
  
  ## Returns the value of self.values which index is equal to the input
  ## iteration argument.
  # @param self The object pointer.
  # @param iteration Current iteration of the parent RepeatedTask of this.
  # @return A numerical value.
  def get_value(self, iteration):
    return self.values[iteration]
  
  ## Getter for self.values.
  # @param self The object pointer.
  # @return self.values
  def get_values(self):
    return self.values

## Range-derived class for computed range of values in SED-ML repeatedTask
## elements. 
# Contrarily to the other Range-derived classes, values encoded by
# FunctionalRange objects are computed on the fly, as model parameters can be
# used in the computation. This way, the value currently stored in the model is
# used instead of the initial value.
class FunctionalRange(Range):
  ## @var math
  # A SymPy expression.
  ## @var parameters
  # A list of Parameter objects.
  ## @var range
  # ID of another Range object stored in self.task.
  ## @var variables
  # A list of Variable objects.
  ## @var task
  # Reference to the parent RepeatedTask of the object.
  
  ## Constructor.
  # @param self The object pointer.
  # @param range A SED-ML functionalRange element.
  # @param workflow A WorkFlow object.
  # @param task A RepeatedTask object.
  def __init__(self, range, workflow, task):
    Range.__init__(self, range)
    self.task = task
    if range.isSetRange():
      self.range = range.getRange()
    self.variables = []
    for v in range.getListOfVariables():
      self.variables.append(variable.Variable(workflow, variable=v))
    self.parameters = []
    for p in range.getListOfParameters():
      self.parameters.append(parameter.Parameter(parameter=p))
    self.math = self.parse_math_expression(range.getMath())
  
  ## Computes and returns the value encoded by the element for the current
  ## iteration of self.task. Overrides Range.get_value.
  # @param self The object pointer.
  # @param iteration Current iteration of self.task.
  # @return result A numerical value.
  def get_value(self, iteration):
    result = self.math
    # SymPy substitution - range
    if self.range is not None:
      range = self.task.get_range_by_id(self.range)
      r_value = range.get_value(iteration)
      result = result.subs(self.range, r_value)
    # SymPy substitution - variables
    for v in self.variables:
      v_id = v.get_id()
      value = v.get_xpath_value()
      result = result.subs(v_id, value)
    # SymPy substitution - parameters
    for p in self.parameters:
      p_id = p.get_id()
      result = result.subs(p_id, p.get_value())
    return result
  
  ## Transform the input MathML mathematical expression into a SymPy
  # expression.
  # @param self The object pointer.
  # @param mathml A MathML expression.
  # @return math A SymPy expression.
  def parse_math_expression(self, mathml):
    math = sympify(libsbml.formulaToString(mathml))
    return math

## Range-derived class for uniformly distributed ranges of values in SED-ML
## repeatedTask elements.
class UniformRange(Range):
  ## @var start
  # Start point for the returned range of values.
  ## @var end
  # End point for the returned range of values.
  ## @var number_of_points
  # Number of intervals the range defined by start / end must be divided into.
  ## @var type
  # Type of range; can be either 'start' or 'end'.
  
  ## Constructor.
  # @param self The object pointer.
  # @param range A SED-ML uniformRange element.
  def __init__(self, range):
    Range.__init__(self, range)
    self.end = range.getEnd()
    self.number_of_points = range.getNumberOfPoints()
    self.start = range.getStart()
    self.type = range.getType()
    self.compute_values()
  
  ## Computes the range of values encoded by the element.
  # @param self The object pointer.
  def compute_values(self):
    if self.type == 'linear':
      step = (self.end - self.start) / self.number_of_points
      factor = 0
      value = 0
      while value < self.end:
        value = self.start + factor * step
        self.values.append(value)
        factor += 1
    elif self.type == 'log':
      if self.start <= 0 or self.end <= 0:
        print("Invalid boundary value in range element " + self.id + ".")
      else:
        start = np.log10(self.start)
        end = np.log10(self.end)
        step = (end - start) / self.number_of_points
        factor = 0
        value = 0
        while value < end:
          value = start + factor * step
          self.values.append(10**value)
          factor += 1
    else:
      print("Invalid type value in range element " + self.id + ": " +
            self.type)
  
  ## Getter for self.end.
  # @param self The object pointer.
  # @return self.end
  def get_end(self):
    return self.end
  
  ## Getter for self.number_of_points.
  # @param self The object pointer.
  # @return self.number_of_points
  def get_number_of_points(self):
    return self.number_of_points
  
  ## Getter for self.start.
  # @param self The object pointer.
  # @return self.start
  def get_start(self):
    return self.start
  
  ## Getter for self.type.
  # @param self The object pointer.
  # @return self.type
  def get_type(self):
    return self.type
  
  ## Setter for self.end.
  # @param self The object pointer.
  # @param end New value for self.end.
  def set_end(self, end):
    self.end = end
  
  ## Setter for self.number_of_points.
  # @param self The object pointer.
  # @param number_of_points New value for self.number_of_points.
  def set_number_of_points(self, number_of_points):
    self.number_of_points = number_of_points
  
  ## Setter for self.start.
  # @param self The object pointer.
  # @param start New value for self.start.
  def set_start(self, start):
    self.start = start
  
  ## Setter for self.type.
  # @param self The object pointer.
  # @param type New value for self.type.
  def set_type(self, type):
    self.type = type

## Range-derived class for vectors of values in SED-ML repeatedTask elements.
class VectorRange(Range):
  ## @var values
  # Range of values encoded by the range element.
  
  ## Constructor.
  # @param self The object pointer.
  # @param range A SED-ML vectorRange element.
  def __init__(self, range):
    Range.__init__(self, range)
    self.values = []
    for v in range.getValues():
      self.values.append(v)
