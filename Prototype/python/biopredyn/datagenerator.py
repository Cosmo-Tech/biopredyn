#!/usr/bin/env python

## @package biopredyn
## $Author$
## $Date$
## $Copyright: 2014, The CoSMo Company, All Rights Reserved $
## $License: BSD 3-Clause $
## $Revision$

import libsedml
import libsbml
from sympy import *
import variable, parameter

## Data generation class, used for creating outputs from task results in a
## SED-ML work flow.
class DataGenerator:
  ## @var id
  # A unique identifier for this object.
  ## @var math
  # A SymPy expression.
  ## @var name
  # Name of this object.
  ## @var parameters
  # A list of Parameter objects.
  ## @var variables
  # A list of Variable objects.
  
  ## Constructor.
  # @param self The object pointer.
  # @param data_generator A SED-ML dataGenerator element.
  # @param workflow A WorkFlow object.
  def __init__(self, data_generator, workflow):
    self.id = data_generator.getId()
    self.name = data_generator.getName()
    # Parse the input data_generator object for parameters
    self.parameters = []
    for p in data_generator.getListOfParameters():
      self.parameters.append(parameter.Parameter(p))
    # Parse the input data_generator object for variables
    self.variables = []
    for v in data_generator.getListOfVariables():
      self.variables.append(variable.Variable(v, workflow))
    self.math = self.parse_math_expression(data_generator.getMath())
  
  ## String representation of this. Displays it as a hierarchy.
  # @param self The object pointer.
  # @return A string representing this as a hierarchy.
  def __str__(self):
    tree = "  |-dataGenerator id=" + self.id + " name=" + self.name + "\n"
    tree += "    |-listOfParameters\n"
    for p in self.parameters:
      tree += str(p)
    tree += "    |-listOfVariables\n"
    for v in self.variables:
      tree += str(v)
    return tree
  
  ## Getter. Returns self.id.
  # @param self The object pointer.
  # @return self.id
  def get_id(self):
    return self.id
  
  ## Setter for self.id.
  # @param self The object pointer.
  # @param id New value for self.id.
  def set_id(self, id):
    self.id = id
  
  ## Getter. Returns self.math.
  # @param self The object pointer.
  # @return self.math
  def get_math(self):
    return self.math
  
  ## Setter for self.math.
  # @param self The object pointer.
  # @param math New value for self.id.
  def set_math(self, math):
    self.math = math
  
  ## Getter. Returns self.name.
  # @param self The object pointer.
  # @return self.name
  def get_name(self):
    return self.name
  
  ## Setter for self.name.
  # @param self The object pointer.
  # @param name New value for self.name.
  def set_name(self, name):
    self.name = name
  
  ## Returns the number of time points in the variables used by this.
  # @param self The object pointer.
  # @return The number of time points in the variables used by this.
  def get_number_of_points(self):
    return self.variables[0].get_number_of_points()
  
  ## Evaluate the values encoded by this and returned them as a 1-dimensional
  # array of numerical values.
  # @param self The object pointer.
  # @return results A 1-dimensional array of numerical values.
  def get_values(self):
    # The number of time points to be considered must be known
    # It is assumed that all the variables have the same number of time points
    num_time_points = self.variables[0].get_number_of_points()
    results = []
    # Initialization 
    for i in range(num_time_points):
      results.append(self.math)
    # SymPy substitution - variables
    for v in self.variables:
      v_id = v.get_id()
      values = v.get_values()
      for n in range(num_time_points):
        results[n] = results[n].subs(v_id, values[n])
    # SymPy substitution - parameters
    for p in self.parameters:
      p_id = p.get_id()
      for n in range(num_time_points):
        results[n] = results[n].subs(p_id, p.get_value())
    return results
  
  ## Transform the input MathML mathematical expression into a SymPy
  # expression.
  # @param self The object pointer.
  # @param mathml A MathML expression.
  # @return math A SymPy expression.
  def parse_math_expression(self, mathml):
    math = sympify(libsbml.formulaToString(mathml))
    return math
