#!/usr/bin/env python

## @package biopredyn
## $Author$
## $Date$
## $Copyright: 2014, The CoSMo Company, All Rights Reserved $
## $License$
## $Revision$

import libsedml

## Base representation of a model parameter in a SED-ML work flow.
class Parameter:
  ## @var id
  # A unique identifier for this object.
  ## @var name
  # Name of this object.
  ## @var value
  # Value of this object.
  
  ## Constructor.
  # @param self The object pointer.
  # @param parameter A SED-ML parameter element.
  def __init__(self, parameter):
    self.id = parameter.getId()
    self.name = parameter.getName()
    self.value = parameter.getValue()
  
  ## String representation of this. Displays it as a hierarchy.
  # @param self The object pointer.
  # @return A string representing this as a hierarchy.
  def __str__(self):
    tree = "      |-parameter id=" + self.id + " name=" + self.name
    tree += " value=" + self.value + "\n"
    return tree
  
  ## Getter. Returns self.id.
  # @param self The object pointer.
  def get_id(self):
    return self.id
  
  ## Setter for self.id.
  # @param self The object pointer.
  # @param id New value for self.id.
  def set_id(self, id):
    self.id = id
  
  ## Getter. Returns self.name.
  # @param self The object pointer.
  def get_name(self):
    return self.name
  
  ## Setter for self.name.
  # @param self The object pointer.
  # @param name New value for self.name.
  def set_name(self, name):
    self.name = name
  
  ## Getter. Returns self.value.
  # @param self The object pointer.
  def get_value(self):
    return self.value
  
  ## Setter for self.value.
  # @param self The object pointer.
  # @param value New value for self.value.
  def set_value(self, value):
    self.value = value