# coding=utf-8

## @package biopredyn
## @author: $Author$
## @date: $Date$
## @copyright: $Copyright: [2013-2014] BioPreDyn $
## @version: $Revision$

from sympy import *

## Base representation of a model pre-processing operation in a SED-ML workflow.
class Change:
  ## @var id
  # ID of the Change element.
  ## @var name
  # Name of the Change element.
  ## @var target
  # XPath expression pointing the element to be impacted by the change.
  ## @var model
  # Reference to the model to be modified by the change.
  
  ## Getter for self.id.
  # @param self The object pointer.
  # @return self.id
  def get_id(self):
    return self.id
  
  ## Setter for self.id.
  # @param self The object pointer.
  # @param id New value for self.id.
  def set_id(self, id):
    self.id = id
  
  ## Getter for self.name.
  # @param self The object pointer.
  # @return self.name
  def get_name(self):
    return self.name
  
  ## Setter for self.name.
  # @param self The object pointer.
  # @param name New value for self.name.
  def set_name(self, name):
    self.name = name
  
  ## Getter for self.model.
  # @param self The object pointer.
  # @return self.model
  def get_model(self):
    return self.model
  
  ## Setter for self.model.
  # @param self The object pointer.
  # @param model New value for self.model.
  def set_model(self, model):
    self.model = model
  
  ## Getter for self.target.
  # @param self The object pointer.
  # @return self.target
  def get_target(self):
    return self.target
  
  ## Setter for self.target.
  # @param self The object pointer.
  # @param target New value for self.target.
  def set_target(self, target):
    self.target = target

## Change-derived class for changes computed with MathML expressions.
class ComputeChange(Change):
  ## @var id
  # ID of the Change element.
  ## @var name
  # Name of the Change element.
  ## @var variables
  # A list of Variable objects.
  ## @var parameters
  # A list of Parameter objects.
  ## @var math
  # A Sympy expression.
  ## @var target
  # XPath expression pointing the element to be impacted by the change.
  ## @var model
  # Reference to the model to be modified by the change.

  ## Constructor.
  # @param self The object pointer.
  # @param compute_change A SED-ML computeChange element.
  # @param model Reference to the Model object to be changed.
  def __init__(self, compute_change, model):
    self.id = compute_change.getId()
    self.name = compute_change.getName()
    self.target = compute_change.getTarget()
    self.model = model
    self.variables = []
    for v in compute_change.getListOfVariables():
      self.variables.append(variable.Variable(v, model=self.model))
    self.parameters = []
    for p in compute_change.getListOfParameters():
      self.parameters.append(parameter.Parameter(p))
    self.math = self.parse_math_expression(compute_change.getMath())
  
  ## Compute the new value of self.target and change it in the model.
  # @param self The object pointer.
  def apply(self):
    print "TODO"
  
  ## Transform the input MathML mathematical expression into a SymPy
  # expression.
  # @param self The object pointer.
  # @param mathml A MathML expression.
  # @return math A SymPy expression.
  def parse_math_expression(self, mathml):
    math = sympify(libsbml.formulaToString(mathml))
    return math

## Change-derived class for changing attribute values.
class ChangeAttribute(Change):
  ## @var id
  # ID of the Change element.
  ## @var name
  # Name of the Change element.
  ## @var value
  # Value to be given to the changed attribute.
  ## @var target
  # XPath expression pointing the element to be impacted by the change.
  ## @var model
  # Reference to the model to be modified by the change.
  
  ## Constructor.
  # @param self The object pointer.
  # @param change_attribute A SED-ML changeAttribute element.
  # @param model Reference to the Model object to be changed.
  def __init__(self, change_attribute, model):
    self.id = change_attribute.getId()
    self.name = change_attribute.getName()
    self.model = model
    self.target = change_attribute.getTarget()
    self.value = change_attribute.getNewValue()
  
  ## Set the value of self.target to self.value in self.model.
  # @param self The object pointer.
  def apply(self):
    if self.target.split('/')[-1].startswith('@'):
    # Case where self.target points to an attribute
      splt = self.target.rsplit('/', 1)
      node = self.model.evaluate_xpath(splt[0])
      node[0].set(splt[1].lstrip('@'), self.value)
    else:
    # Case where self.target points to an element
      node = self.model.evaluate_xpath(self.target)
      node.text = self.value
  
  ## Getter for self.value.
  # @param self The object pointer.
  # @return self.value
  def get_value(self):
    return self.value
  
  ## Setter for self.value.
  # @param self The object pointer.
  # @param value New value for self.value.
  def set_value(self, value):
    self.value = value

## Change-derived class for adding a piece of XML code.
class AddXML(Change):
  ## @var id
  # ID of the Change element.
  ## @var name
  # Name of the Change element.
  ## @var xml
  # A piece of XML code.
  ## @var target
  # XPath expression pointing the element to be impacted by the change.
  ## @var model
  # Reference to the model to be modified by the change.
  
  ## Constructor.
  # @param self The object pointer.
  # @param add_xml A SED-ML addXML element.
  def __init__(self, add_xml):
    self.id = add_xml.getId()
    self.name = add_xml.getName()
  
  ## Compute the new value of self.target and change it in the model.
  # @param self The object pointer.
  def apply(self):
    print "TODO"
  
  ## Getter for self.xml.
  # @param self The object pointer.
  # @return self.xml
  def get_xml(self):
    return self.xml
  
  ## Setter for self.xml.
  # @param self The object pointer.
  # @param xml New value for self.xml.
  def set_xml(self, xml):
    self.xml = xml

## Change-derived class for replacing a piece of XML code.
class ChangeXML(Change):
  ## @var id
  # ID of the Change element.
  ## @var name
  # Name of the Change element.
  ## @var xml
  # A piece of XML code.
  ## @var target
  # XPath expression pointing the element to be impacted by the change.
  ## @var model
  # Reference to the model to be modified by the change.
  
  ## Constructor.
  # @param self The object pointer.
  # @param change_xml A SED-ML changeXML element.
  def __init__(self, change_xml):
    self.id = change_xml.getId()
    self.name = change_xml.getName()
  
  ## Compute the new value of self.target and change it in the model.
  # @param self The object pointer.
  def apply(self):
    print "TODO"
  
  ## Getter for self.xml.
  # @param self The object pointer.
  # @return self.xml
  def get_xml(self):
    return self.xml
  
  ## Setter for self.xml.
  # @param self The object pointer.
  # @param xml New value for self.xml.
  def set_xml(self, xml):
    self.xml = xml

## Change-derived class for removing a piece of XML code.
class RemoveXML(Change):
  ## @var id
  # ID of the Change element.
  ## @var name
  # Name of the Change element.
  ## @var target
  # XPath expression pointing the element to be impacted by the change.
  ## @var model
  # Reference to the model to be modified by the change.
  
  ## Constructor.
  # @param self The object pointer.
  # @param remove_xml A SED-ML removeXML element.
  # @param model Reference to the Model object to be changed.
  def __init__(self, remove_xml, model):
    self.id = remove_xml.getId()
    self.name = remove_xml.getName()
    self.model = model
    self.target = remove_xml.getTarget()
  
  ## Compute the new value of self.target and change it in the model.
  # @param self The object pointer.
  def apply(self):
    # self.target should not point to an attribute
    if self.target.split('/')[-1].startswith('@'):
      print(
            "XPath error: " + self.target + " points to an attribute instead " +
            "of a node."
            )
    else:
      target = self.model.evaluate_xpath(self.target)
      # target is removed by its parent
      parent = target[0].getparent()
      parent.remove(target[0])