#!/usr/bin/env python
# coding=utf-8

## @package biopredyn
## Copyright: [2012-2015] The CoSMo Company, All Rights Reserved
## License: BSD 3-Clause

from sympy import *
from lxml import etree
import libsbml
import variable, parameter

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
  
  ## Constructor; either 'change' or 'idf' and 'target' must be passed as
  ## keyword argument(s).
  # @param self The object pointer.
  # @param change A libsedml.SedChange element; optional (default=None).
  # @param idf A unique identifier; optional (default=None).
  # @param target A valid XPath expression; optional (default=None).
  def __init__(self, change=None, idf=None, target=None):
    if (change is None) and (idf is None or target is None):
      sys.exit("Error: either 'change' or 'target' and 'idf' " +
        "input arguments must be passed to the constructor.")
    else:
      if change is not None:
        self.id = change.getId()
        self.name = change.getName()
        self.target = change.getTarget()
      elif idf is not None and target is not None:
        self.id = idf
        self.target = target
  
  ## String representation of this. Displays it as a hierarchy.
  # @param self The object pointer.
  # @return A string representing this as a hierarchy.
  def __str__(self):
    tree = "      |-" + self.type + " id=" + self.id + " name=" + self.name
    tree += " target=" + self.target + "\n"
    return tree
  
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
  ## @var variables
  # A list of Variable objects.
  ## @var parameters
  # A list of Parameter objects.
  ## @var math
  # A Sympy expression.

  ## Constructor; either 'change' or 'idf' and 'target' and 'math' must be
  ## passed as keyword arguments.
  # @param self The object pointer.
  # @param workflow A biopredyn.workflow.WorkFlow object.
  # @param model Reference to the biopredyn.model.Model object to be changed.
  # @param change A libsedml.SedComputeChange element; optional (default: None).
  # @param idf A unique identifier; optional (default: None).
  # @param target A valid XPath expression; optional (default: None).
  # @param math A valid Python mathematical expression. Symbols it contains must
  # correspond to identifiers of elements listed in self.variables and / or
  # self.parameters.
  def __init__(self, workflow, model, change=None, idf=None, target=None,
    math=None):
    if (change is None) and (idf is None or target is None or math is None):
      sys.exit("Error: either 'change' or 'target' and 'idf' " +
        "input arguments must be passed to the constructor.")
    else:
      self.model = model
      self.variables = []
      self.parameters = []
      if change is not None:
        Change.__init__(self, change=change)
        for v in change.getListOfVariables():
          self.add_variable(variable.Variable(v, workflow))
        for p in change.getListOfParameters():
          self.add_parameter(parameter.Parameter(p))
        self.math = self.parse_math_expression(change.getMath())
      elif idf is not None and target is not None and math is not None:
        Change.__init__(self, idf=idf, target=target)
        self.math = sympify(math)
  
  ## Appends the input biopredyn.parameter.Parameter object to self.parameters.
  # @param self The object pointer.
  # @param par A biopredyn.parameter.Parameter object.
  def add_parameter(self, par):
    self.parameters.append(par)
  
  ## Appends the input biopredyn.variable.Variable object to self.variables.
  # @param self The object pointer.
  # @param var A biopredyn.variable.Variable object.
  def add_variable(self, var):
    self.variables.append(var)

  ## Compute the new value of self.target and change it in the model.
  # @param self The object pointer.
  def apply(self):
    result = self.math
    # SymPy substitution - variables
    for v in self.variables:
      v_id = v.get_id()
      value = v.get_xpath_value()
      result = result.subs(v_id, value)
    # SymPy substitution - parameters
    for p in self.parameters:
      p_id = p.get_id()
      result = result.subs(p_id, p.get_value())
    # Target attribute is changed in self.model
    if self.target.split('/')[-1].startswith('@'):
      # Case where self.target points to an attribute
      splt = self.target.rsplit('/', 1)
      node = self.model.evaluate_xpath(splt[0])
      node[0].set(splt[1].lstrip('@'), str(result))
    else:
      # Case where self.target points to an element
      node = self.model.evaluate_xpath(self.target)
      node.text = str(result)
  
  ## Transform the input MathML mathematical expression into a SymPy
  # expression.
  # @param self The object pointer.
  # @param mathml A MathML expression.
  # @return math A SymPy expression.
  def parse_math_expression(self, mathml):
    math = sympify(libsbml.formulaToString(mathml))
    return math
  
  ## Getter for self.math.
  # @param self The object pointer.
  # @return self.math
  def get_math(self):
    return self.math
  
  ## Setter for self.math.
  # @param self The object pointer.
  # @param math A SymPy expression.
  def set_math(self, math):
    self.math = math

## Change-derived class for changing attribute values.
class ChangeAttribute(Change):
  ## @var value
  # Value to be given to the changed attribute.
  
  ## Constructor.
  # @param self The object pointer.
  # @param model Reference to the biopredyn.model.Model object to be changed.
  # @param change A libsedml.SedChangeAttribute element; optional (default:
  # None).
  # @param idf A unique identifier; optional (default: None).
  # @param target A valid XPath expression; optional (default: None).
  # @param value Value to be given to the target attribute; optional (default:
  # None).
  def __init__(self, model, change=None, idf=None, target=None, value=None):
    if (change is None) and (idf is None or target is None or value is None):
      sys.exit("Error: either 'change' or 'idf', 'target' and 'value' must " +
        "be passed as arguments.")
    else:
      self.model = model
      if change is not None:
        Change.__init__(self, change=change)
        self.value = change.getNewValue()
      elif idf is not None and target is not None and value is not None:
        Change.__init__(self, idf=idf, target=target)
        self.value = value
  
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
  ## @var xml
  # A piece of XML code.
  
  ## Constructor; either 'change' or 'idf', 'target' and 'xml' must be passed as
  ## arguments.
  # @param self The object pointer.
  # @param model Reference to the Model object to be changed.
  # @param change A libsedml.SedAddXML element; optional (default: None).
  # @param idf A unique identifier; optional (default: None).
  # @param target A valid XPath expression; optional (default: None).
  # @param xml A valid XML string; optional (default: None).
  def __init__(self, model, change=None, idf=None, target=None, xml=None):
    if (change is None) and (idf is None or target is None or xml is None):
      sys.exit("Error: either 'change' or 'idf', 'target' and 'xml' must be " +
        "passed as arguments.")
    else:
      self.model = model
      if change is not None:
        Change.__init__(self, change=change)
        self.xml = change.getNewXML().toXMLString()
      elif idf is not None and target is not None and xml is not None:
        Change.__init__(self, idf=idf, target=target)
        self.xml = xml
  
  ## Add self.xml as a child of self.target in self.model.
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
      new_element = etree.XML(self.xml)
      target[0].append(new_element)
  
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
  ## @var xml
  # A piece of XML code.
  
  ## Constructor; either 'change' or 'idf', 'target' and 'xml' must be passed as
  ## arguments.
  # @param self The object pointer.
  # @param model Reference to the Model object to be changed.
  # @param change A libsedml.SedChangeXML element; optional (default: None).
  # @param idf A unique identifier; optional (default: None).
  # @param target A valid XPath expression; optional (default: None).
  # @param xml A valid XML string; optional (default: None).
  def __init__(self, model, change=None, idf=None, target=None, xml=None):
    if (change is None) and (idf is None or target is None or xml is None):
      sys.exit("Error: either 'change' or 'idf', 'target' and 'xml' must be " +
        "passed as arguments.")
    else:
      self.model = model
      if change is not None:
        Change.__init__(self, change=change)
        self.xml = change.getNewXML().toXMLString()
      elif idf is not None and target is not None and xml is not None:
        Change.__init__(self, idf=idf, target=target)
        self.xml = xml
  
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
      new_element = etree.XML(self.xml)
      parent = target[0].getparent()
      parent.append(new_element)
      parent.remove(target[0])
  
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
  
  ## Constructor; either 'change' or 'idf' and 'target' must be passed as
  ## arguments.
  # @param self The object pointer.
  # @param model Reference to the Model object to be changed.
  # @param change A libsedml.SedChangeXML element; optional (default: None).
  # @param idf A unique identifier; optional (default: None).
  # @param target A valid XPath expression; optional (default: None).
  def __init__(self, model, change=None, idf=None, target=None):
    if (change is None) and (idf is None or target is None):
      sys.exit("Error: either 'change' or 'idf' and 'target' must be " +
        "passed as arguments.")
    else:
      self.model = model
      if change is not None:
        Change.__init__(self, change=change)
      elif idf is not None and target is not None and xml is not None:
        Change.__init__(self, idf=idf, target=target)
  
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

## Class for RepeatedTask change elements; does not inherit from Change, as it
## works differently from the other changes.
class SetValue:
  ## @var id
  # ID of the Change element.
  ## @var math
  # A Sympy expression.
  ## @var model_id
  # ID of the model to be modified by this.
  ## @var name
  # Name of the Change element.
  ## @var parameters
  # A list of Parameter objects.
  ## @var range
  # ID of a Range object from the parent RepeatedTask element.
  ## @var target
  # XPath expression pointing the element to be impacted by the change.
  ## @var variables
  # A list of Variable objects.
  ## @var workflow
  # A WorkFlow object.
  
  ## Constructor.
  # @param self The object pointer.
  # @param setvalue A SED-ML setValue element.
  # @param task A RepeatedTask object.
  # @param workflow A WorkFlow object.
  def __init__(self, setvalue, task, workflow):
    self.id = setvalue.getId()
    self.name = setvalue.getName()
    self.target = setvalue.getTarget()
    self.task = task
    self.workflow = workflow
    if setvalue.isSetRange():
      self.range = setvalue.getRange()
    self.model_id = setvalue.getModelReference()
    self.variables = []
    for v in setvalue.getListOfVariables():
      self.variables.append(variable.Variable(v, workflow))
    self.parameters = []
    for p in setvalue.getListOfParameters():
      self.parameters.append(parameter.Parameter(p))
    self.math = self.parse_math_expression(setvalue.getMath())
  
  ## Compute the new value of self.target and change it in self.model.
  # @param self The object pointer.
  # @param iteration Current iteration of self.task.
  def apply(self, iteration):
    model = self.workflow.get_model_by_id(self.model_id)
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
    # Target attribute is changed in model
    if self.target.split('/')[-1].startswith('@'):
      # Case where self.target points to an attribute
      splt = self.target.rsplit('/', 1)
      node = model.evaluate_xpath(splt[0])
      node[0].set(splt[1].lstrip('@'), str(result))
    else:
      # Case where self.target points to an element
      node = model.evaluate_xpath(self.target)
      node.text = str(result)
  
  ## Getter for self.id.
  # @param self The object pointer.
  # @return self.id
  def get_id(self):
    return self.id
  
  ## Getter for self.model_id.
  # @param self The object pointer.
  # @return self.model_id
  def get_model_id(self):
    return self.model_id
  
  ## Getter for self.name.
  # @param self The object pointer.
  # @return self.name
  def get_name(self):
    return self.name
  
  ## Getter for self.target.
  # @param self The object pointer.
  # @return self.target
  def get_target(self):
    return self.target
  
  ## Transform the input MathML mathematical expression into a SymPy
  # expression.
  # @param self The object pointer.
  # @param mathml A MathML expression.
  # @return math A SymPy expression.
  def parse_math_expression(self, mathml):
    math = sympify(libsbml.formulaToString(mathml))
    return math
  
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
  
  ## Setter for self.model_id.
  # @param self The object pointer.
  # @param model_id New value for self.model_id.
  def set_model_id(self, model_id):
    self.model_id = model_id
  
  ## Setter for self.target.
  # @param self The object pointer.
  # @param target New value for self.target.
  def set_target(self, target):
    self.target = target
