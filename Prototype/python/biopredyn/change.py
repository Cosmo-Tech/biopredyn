#!/usr/bin/env python
# coding=utf-8

## @package biopredyn
## Copyright: [2012-2015] The CoSMo Company, All Rights Reserved
## License: BSD 3-Clause

from sympy import *
from lxml import etree
import libsbml
import libsedml
import variable, parameter

## Base representation of a model pre-processing operation in a SED-ML workflow.
class Change:
  ## @var id
  # ID of the Change element.
  ## @var name
  # Name of the Change element.
  ## @var target
  # XPath expression pointing the element to be impacted by the change.
  ## @var chn_type
  # Type of change; can be either 'computeChange', 'changeAttribute',
  # 'changeXML', 'addXML', 'removeXML'.
  ## @var model
  # Reference to the model to be modified by the change.
  
  ## Constructor; either 'change' or 'idf' and 'target' must be passed as
  ## keyword argument(s).
  # @param self The object pointer.
  # @param change A libsedml.SedChange element; optional (default=None).
  # @param idf A unique identifier; optional (default=None).
  # @param name A name for 'self'; optional (default: None).
  # @param target A valid XPath expression; optional (default=None).
  # @param typ The type of change encoded in 'self'; can be either
  # 'computeChange', 'changeAttribute', 'changeXML', 'addXML' or 'removeXML'.
  # Optional (default: None).
  def __init__(self, change=None, idf=None, name=None, target=None, typ=None):
    if (change is None) and (idf is None or target is None or typ is None):
      raise RuntimeError("Either 'change' or 'target', 'idf' and 'typ' " +
        "must be passed as keyword arguments.")
    else:
      if change is not None:
        self.id = change.getId()
        self.name = change.getName()
        self.target = change.getTarget()
        self.chn_type = change.getElementName()
      elif idf is not None and target is not None:
        self.id = idf
        self.name = name
        self.target = target
        self.chn_type = typ
  
  ## String representation of this. Displays it as a hierarchy.
  # @param self The object pointer.
  # @return A string representing this as a hierarchy.
  def __str__(self):
    tree = "      |-" + self.chn_type + " id=" + self.id + " name=" + self.name
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
  
  ## Getter for self.chn_type.
  # @param self The object pointer.
  # @return self.chn_type
  def get_type(self):
    return self.chn_type
  
  ## Setter for self.target.
  # @param self The object pointer.
  # @param target New value for self.target.
  def set_target(self, target):
    self.target = target

## Change-derived class for changes computed with MathML expressions.
class ComputeChange(Change):
  ## @var variables
  # A list of biopredyn.variable.Variable objects.
  ## @var parameters
  # A list of biopredyn.parameter.Parameter objects.
  ## @var math
  # A Sympy expression.

  ## Constructor; either 'change' or 'idf' and 'target' and 'math' must be
  ## passed as keyword arguments.
  # @param self The object pointer.
  # @param workflow A biopredyn.workflow.WorkFlow object.
  # @param model Reference to the biopredyn.model.Model object to be changed.
  # @param change A libsedml.SedComputeChange element; optional (default: None).
  # @param idf A unique identifier; optional (default: None).
  # @param name A name for 'self'; optional (default: None).
  # @param target A valid XPath expression; optional (default: None).
  # @param math A valid Python mathematical expression. Symbols it contains must
  # correspond to identifiers of elements listed in self.variables and / or
  # self.parameters. Optional (default: None).
  def __init__(self, workflow, model, change=None, idf=None, name=None,
    target=None, math=None):
    if (change is None) and (idf is None or target is None or math is None):
      raise RuntimeError("Either 'change' or 'target', 'math' and 'idf' " +
        "must be passed as keyword arguments.")
    else:
      self.model = model
      self.variables = []
      self.parameters = []
      if change is not None:
        Change.__init__(self, change=change)
        for v in change.getListOfVariables():
          self.add_variable(variable.Variable(workflow, variable=v))
        for p in change.getListOfParameters():
          self.add_parameter(parameter.Parameter(parameter=p))
        self.math = self.parse_math_expression(change.getMath())
      elif idf is not None and target is not None and math is not None:
        Change.__init__(self, idf=idf, name=name, target=target,
          typ='computeChange')
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
  
  ## Getter for self.parameters.
  # @param self The object pointer.
  # @return self.parameters
  def get_parameters(self):
    return self.parameters
  
  ## Getter for self.variables.
  # @param self The object pointer.
  # @return self.variables
  def get_variables(self):
    return self.variables
  
  ## Setter for self.math.
  # @param self The object pointer.
  # @param math A valid Python mathematical expression. Symbols it contains must
  # correspond to identifiers of elements listed in self.variables and / or
  # self.parameters.
  def set_math(self, math):
    self.math = sympify(math)

  ## Returns the libsedml.SedComputeChange representation of this.
  # @param self The object pointer.
  # @param level Level of SED-ML language to be used.
  # @param version Version of SED-ML language to be used.
  # @return A libsedml.SedComputeChange object.
  def to_sedml(self, level, version):
    ch = libsedml.SedComputeChange(level, version)
    ch.setId(self.get_id())
    if self.get_name() is not None:
      ch.setName(str(self.get_name()))
    ch.setTarget(self.get_target())
    # adding parameters and variables
    for p in self.get_parameters():
      ch.addParameter(p.to_sedml(level, version))
    for v in self.get_variables():
      ch.addVariable(v.to_sedml(level, version))
    ch.setMath(libsbml.parseFormula(printing.ccode(self.math)))
    return ch

## Change-derived class for changing attribute values.
class ChangeAttribute(Change):
  ## @var value
  # Value to be given to the changed attribute.
  
  ## Constructor; either 'change' or 'idf', 'target' and 'value' must be passed
  ## as keyword arguments.
  # @param self The object pointer.
  # @param model Reference to the biopredyn.model.Model object to be changed.
  # @param change A libsedml.SedChangeAttribute element; optional (default:
  # None).
  # @param idf A unique identifier; optional (default: None).
  # @param name A name for 'self'; optional (default: None).
  # @param target A valid XPath expression; optional (default: None).
  # @param value Value to be given to the target attribute; optional (default:
  # None).
  def __init__(self, model, change=None, idf=None, name=None, target=None,
    value=None):
    if (change is None) and (idf is None or target is None or value is None):
      raise RuntimeError("Either 'change' or 'idf', 'target' and " +
        "'value' must be passed as keyword arguments.")
    else:
      self.model = model
      if change is not None:
        Change.__init__(self, change=change)
        self.value = change.getNewValue()
      elif idf is not None and target is not None and value is not None:
        Change.__init__(self, idf=idf, name=name, target=target,
          typ='changeAttribute')
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

  ## Returns the libsedml.SedChangeAttribute representation of this.
  # @param self The object pointer.
  # @param level Level of SED-ML language to be used.
  # @param version Version of SED-ML language to be used.
  # @return A libsedml.SedChangeAttribute object.
  def to_sedml(self, level, version):
    ch = libsedml.SedChangeAttribute(level, version)
    ch.setId(self.get_id())
    if self.get_name() is not None:
      ch.setName(str(self.get_name()))
    ch.setTarget(self.get_target())
    ch.setNewValue(self.get_value())
    return ch

## Change-derived class for adding a piece of XML code.
class AddXML(Change):
  ## @var xml
  # A piece of XML code.
  
  ## Constructor; either 'change' or 'idf', 'target' and 'xml' must be passed as
  ## keyword arguments.
  # @param self The object pointer.
  # @param model Reference to the Model object to be changed.
  # @param change A libsedml.SedAddXML element; optional (default: None).
  # @param idf A unique identifier; optional (default: None).
  # @param name A name for 'self'; optional (default: None).
  # @param target A valid XPath expression; optional (default: None).
  # @param xml A valid XML string; optional (default: None).
  def __init__(self, model, change=None, idf=None, name=None, target=None,
    xml=None):
    if (change is None) and (idf is None or target is None or xml is None):
      raise RuntimeError("Either 'change' or 'idf', 'target' and " +
        "'xml' must be passed as keyword arguments.")
    else:
      self.model = model
      if change is not None:
        Change.__init__(self, change=change)
        self.xml = change.getNewXML().toXMLString()
      elif idf is not None and target is not None and xml is not None:
        Change.__init__(self, idf=idf, name=name, target=target, typ='addXML')
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

  ## Returns the libsedml.SedAddXML representation of this.
  # @param self The object pointer.
  # @param level Level of SED-ML language to be used.
  # @param version Version of SED-ML language to be used.
  # @return A libsedml.SedAddXML object.
  def to_sedml(self, level, version):
    ch = libsedml.SedAddXML(level, version)
    ch.setId(self.get_id())
    if self.get_name() is not None:
      ch.setName(str(self.get_name()))
    ch.setTarget(str(self.get_target()))
    ch.setNewXML(libsbml.XMLNode_convertStringToXMLNode(self.get_xml()))
    return ch

## Change-derived class for replacing a piece of XML code.
class ChangeXML(Change):
  ## @var xml
  # A piece of XML code.
  
  ## Constructor; either 'change' or 'idf', 'target' and 'xml' must be passed as
  ## keyword arguments.
  # @param self The object pointer.
  # @param model Reference to the Model object to be changed.
  # @param change A libsedml.SedChangeXML element; optional (default: None).
  # @param idf A unique identifier; optional (default: None).
  # @param name A name for 'self'; optional (default: None).
  # @param target A valid XPath expression; optional (default: None).
  # @param xml A valid XML string; optional (default: None).
  def __init__(self, model, change=None, idf=None, name=None, target=None,
    xml=None):
    if (change is None) and (idf is None or target is None or xml is None):
      raise RuntimeError("Either 'change' or 'idf', 'target' and " +
        "'xml' must be passed as arguments.")
    else:
      self.model = model
      if change is not None:
        Change.__init__(self, change=change)
        self.xml = change.getNewXML().toXMLString()
      elif idf is not None and target is not None and xml is not None:
        Change.__init__(self, idf=idf, name=name, target=target,
          typ='changeXML')
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

  ## Returns the libsedml.SedChangeXML representation of this.
  # @param self The object pointer.
  # @param level Level of SED-ML language to be used.
  # @param version Version of SED-ML language to be used.
  # @return A libsedml.SedChangeXML object.
  def to_sedml(self, level, version):
    ch = libsedml.SedChangeXML(level, version)
    ch.setId(self.get_id())
    if self.get_name() is not None:
      ch.setName(str(self.get_name()))
    ch.setTarget(self.get_target())
    ch.setNewXML(libsbml.XMLNode_convertStringToXMLNode(self.get_xml()))
    return ch

## Change-derived class for removing a piece of XML code.
class RemoveXML(Change):
  
  ## Constructor; either 'change' or 'idf' and 'target' must be passed as
  ## keyword arguments.
  # @param self The object pointer.
  # @param model Reference to the Model object to be changed.
  # @param change A libsedml.SedChangeXML element; optional (default: None).
  # @param idf A unique identifier; optional (default: None).
  # @param name A name for 'self'; optional (default: None).
  # @param target A valid XPath expression; optional (default: None).
  def __init__(self, model, change=None, idf=None, name=None, target=None):
    if (change is None) and (idf is None or target is None):
      raise RuntimeError("Either 'change' or 'idf' and 'target' must " +
        "be passed as arguments.")
    else:
      self.model = model
      if change is not None:
        Change.__init__(self, change=change)
      elif idf is not None and target is not None:
        Change.__init__(self, idf=idf, name=name, target=target,
          typ='removeXML')
  
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

  ## Returns the libsedml.SedRemoveXML representation of this.
  # @param self The object pointer.
  # @param level Level of SED-ML language to be used.
  # @param version Version of SED-ML language to be used.
  # @return A libsedml.SedRemoveXML object.
  def to_sedml(self, level, version):
    ch = libsedml.SedRemoveXML(level, version)
    ch.setId(self.get_id())
    if self.get_name() is not None:
      ch.setName(str(self.get_name()))
    ch.setTarget(self.get_target())
    return ch

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
  ## @var sv_type
  # Type of 'self'; set to 'setValue'.
  ## @var variables
  # A list of Variable objects.
  ## @var workflow
  # A WorkFlow object.
  
  ## Constructor; either 'setvalue' or 'idf', 'target', 'mod_ref' and 'math'
  ## must be passed as keyword arguments.
  # @param self The object pointer.
  # @param task A libsedml.SedRepeatedTask object.
  # @param workflow A WorkFlow object.
  # @param setvalue A libsedml.SedSetValue element; optional (default: None).
  # @param idf A unique identifier; optional (default: None).
  # @param name A name for 'self'; optional (default: None).
  # @param target A valid XPath expression; optional (default: None).
  # @param mod_ref Identifier of the biopredyn.model.Model object which should
  # be modified; optional (default: None).
  # @param rng_ref Reference to a biopredyn.ranges.Range object in 'task'.
  # @param math A valid Python mathematical expression. Symbols it contains must
  # correspond to identifiers of elements listed in self.variables and / or
  # self.parameters. Optional (default: None).
  def __init__(self, task, workflow, setvalue=None, idf=None, name=None,
    target=None, mod_ref=None, rng_ref=None, math=None):
    if setvalue is None and (idf is None or target is None or mod_ref is None or
      math is None):
      raise RuntimeError("Either 'setvalue' or 'idf', 'target', " +
        "'mod_ref' and 'math' must be passed as keyword argument(s).")
    else:
      self.task = task
      self.sv_type = 'setValue'
      self.workflow = workflow
      self.parameters = []
      self.variables = []
      self.range = None
      if setvalue is not None:
        self.id = setvalue.getId()
        self.name = setvalue.getName()
        self.target = setvalue.getTarget()
        if setvalue.isSetRange():
          self.set_range(setvalue.getRange())
        self.model_id = setvalue.getModelReference()
        for v in setvalue.getListOfVariables():
          self.add_variable(variable.Variable(workflow, variable=v))
        for p in setvalue.getListOfParameters():
          self.add_parameter(parameter.Parameter(parameter=p))
        self.math = self.parse_math_expression(setvalue.getMath())
      else:
        self.id = idf
        self.name = name
        self.target = target
        self.model_id = mod_ref
        self.range = rng_ref
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
  
  ## Getter for self.parameters.
  # @param self The object pointer.
  # @return self.parameters
  def get_parameters(self):
    return self.parameters
  
  ## Getter for self.range.
  # @param self The object pointer.
  # @return self.range
  def get_range(self):
    return self.range
  
  ## Getter for self.target.
  # @param self The object pointer.
  # @return self.target
  def get_target(self):
    return self.target
  
  ## Getter for self.sv_type.
  # @param self The object pointer.
  # @return self.sv_type
  def get_type(self):
    return self.sv_type
  
  ## Getter for self.variables.
  # @param self The object pointer.
  # @return self.variables
  def get_variables(self):
    return self.parameters
  
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
  
  ## Setter for self.range.
  # @param self The object pointer.
  # @param rng Reference to the identifier of a biopredyn.ranges.Range object
  # of self.task.
  def set_range(self, rng):
    self.range = rng

  ## Returns the libsedml.SedSetValue representation of this.
  # @param self The object pointer.
  # @param level Level of SED-ML language to be used.
  # @param version Version of SED-ML language to be used.
  # @return A libsedml.SedSetValue object.
  def to_sedml(self, level, version):
    ch = libsedml.SedSetValue(level, version)
    ch.setId(self.get_id())
    if self.get_name() is not None:
      ch.setName(str(self.get_name()))
    if self.get_range() is not None:
      ch.setRange(self.get_range())
    ch.setTarget(self.get_target())
    ch.setModelReference(self.get_model_id())
    # adding parameters and variables
    for p in self.get_parameters():
      ch.addParameter(p.to_sedml(level, version))
    for v in self.get_variables():
      ch.addVariable(v.to_sedml(level, version))
    ch.setMath(libsbml.parseFormula(printing.ccode(self.math)))
    return ch
