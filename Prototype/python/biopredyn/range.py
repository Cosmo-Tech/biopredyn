#!/usr/bin/env python

## @package biopredyn
## $Author$
## $Date$
## $Copyright: 2014, The CoSMo Company, All Rights Reserved $
## $License: BSD 3-Clause $
## $Revision$

import libsbml

## Base class for expressing ranges in SED-ML repeatedTask elements.
class Range:
  ## @var id
  # A unique identifier associated with the object.
  
  ## Constructor.
  # @param self The object pointer.
  # @param range A SED-ML range element.
  def __init__(self, range):
    self.id = range.getId()
  
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

## Range-derived class for computed range of values in SED-ML repeatedTask
## elements.
class FunctionalRange(Range):
  ## @var math
  # A SymPy expression.
  ## @var parameters
  # A list of Parameter objects.
  ## @var variables
  # A list of Variable objects.
  
  ## Constructor.
  # @param self The object pointer.
  # @param range A SED-ML functionalRange element.
  # @param workflow A WorkFlow object.
  def __init__(self, range, workflow):
    Range.__init__(self, range)
    self.variables = []
    for v in range.getListOfVariables():
      self.variables.append(variable.Variable(v, workflow))
    self.parameters = []
    for p in range.getListOfParameters():
      self.parameters.append(parameter.Parameter(p))
    self.math = self.parse_math_expression(range.getMath())
  
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
  
  ## Getter for self.values.
  # @param self The object pointer.
  # @return self.values
  def get_values(self):
    return self.values