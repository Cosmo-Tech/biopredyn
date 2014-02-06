# coding=utf-8

## @package biopredyn
## @author: $Author$
## @date: $Date$
## @copyright: $Copyright: [2013-2014] BioPreDyn $
## @version: $Revision$

## Base representation of a model pre-processing operation in a SED-ML workflow.
class Change:
  ## @var target
  # XPath expression pointing the element to be impacted by the change.
  
  ## Getter. Returns self.target.
  # @param self The object pointer.
  # @return self.target
  def get_target(self):
    return self.target
  
  ## Setter. Assign a new value to self.target.
  # @param self The object pointer.
  # @param target New value for self.target.
  def set_target(self, target):
    self.target = target

## Change-derived class for changes computed with MathML expressions.
class ComputeChange(Change):
  ## @var variables
  # A list of Variable objects.
  ## @var parameters
  # A list of Parameter objects.
  ## @var math
  # A Sympy expression.

  ## Constructor.
  # @param self The object pointer.
  # @param compute_change A SED-ML computeChange element.
  def __init__(self, compute_change):
    print "TODO"

## Change-derived class for changing attribute values.
class ChangeAttribute(Change):
  ## @var value
  # Value to be given to the changed attribute.
  
  ## Constructor.
  # @param self The object pointer.
  # @param value String value.
  def __init__(self, value):
    self.value = value