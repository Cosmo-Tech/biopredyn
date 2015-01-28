#!/usr/bin/env python
# coding=utf-8

## @package biopredyn
## Copyright: [2012-2015] The CoSMo Company, All Rights Reserved
## License: BSD 3-Clause

## Representation of an algorithm in SED-ML workflows; an algorithm is defined
## using a KiSAO id along with several optional algorithm parameters.
class Algorithm:
  ## @var id
  # A unique identifier for this object.
  ## @var kisao_id
  # A KiSAO identifier (syntax KISAO:0000XYZ) for the algorithm encoded by this.
  ## @var name
  # Name of this object.
  ## @var parameters
  # A list of AlgorithmParameter objects.

  ## Constructor; either 'algo' or 'idf' and 'kid' must be passed as keyword
  ## argument(s).
  # @param self The object pointer.
  # @param algo A libsedml.SedAlgorithm element; optional (default: None).
  # @param idf A unique identifier; optional (default: None).
  # @param name A name for 'self'; optional (default: None).
  # @param kid A valid KiSAO identifier; optional (default: None).
  def __init__(self, algo=None, idf=None, name=None, kid=None):
    if algo is None and (idf is None or kid is None):
      sys.exit("Error: either 'algo' or 'idf' and 'kid' must be passed as " +
        "keyword argument(s).")
    else:
      self.parameters = []
      if algo is not None:
        self.id = algo.getId()
        self.name = algo.getName()
        self.kisao_id = algo.getKisaoID()
        for p in algo.getListOfAlgorithmParameters():
          self.add_parameter(AlgorithmParameter(parameter=p))
      else:
        self.id = idf
        self.name = name
        self.kisao_id = kid

  ## Appends the input biopredyn.parameter.Parameter object to self.parameters.
  # @param self The object pointer.
  # @param par A biopredyn.parameter.Parameter object.
  def add_parameter(self, par):
    self.parameters.append(par)

  ## Getter. Returns self.id.
  # @param self The object pointer.
  # @return self.id
  def get_id(self):
    return self.id

  ## Getter. Returns self.kisao_id.
  # @param self The object pointer.
  # @return self.kisao_id
  def get_kisao_id(self):
    return self.kisao_id

  ## Getter. Returns self.name.
  # @param self The object pointer.
  # @return self.name
  def get_name(self):
    return self.name

  ## Getter. Returns the first AlgorithmParameter object with the input id in
  ## self.parameters.
  # @param self The object pointer.
  # @param id ID of the object to be returned in self.parameters.
  # @return An AlgorithmParameter object.
  def get_parameter_by_id(self, id):
    res = None
    for p in self.parameters:
       if (p.get_id() == id):
          res = p
    return res

  ## Getter. Returns the first AlgorithmParameter object with the input name in
  ## self.parameters.
  # @param self The object pointer.
  # @param name Name of the object to be returned in self.parameters.
  # @return An AlgorithmParameter object.
  def get_parameter_by_name(self, name):
    res = None
    for p in self.parameters:
       if (p.get_name() == name):
          res = p
    return res

  ## Getter. Returns self.parameters.
  # @param self The object pointer.
  # @return self.parameters
  def get_parameters(self):
    return self.parameters
 
  ## Setter for self.id.
  # @param self The object pointer.
  # @param id New value for self.id
  def set_id(self, id):
    self.id = id

  ## Setter for self.kisao_id.
  # @param self The object pointer.
  # @param kisao_id New value for self.kisao_id
  def set_kisao_id(self, kisao_id):
    self.kisao_id = kisao_id

  ## Setter for self.name.
  # @param self The object pointer.
  # @param name New value for self.name
  def set_name(self, name):
    self.name = name

## Representation of an algorithm parameter in SED-ML workflows; an algorithm
## parameter is defined using a KiSAO id, and has a value.
class AlgorithmParameter:
  ## @var id
  # A unique identifier for this object.
  ## @var kisao_id
  # A KiSAO identifier (syntax KISAO:0000XYZ) for the parameter encoded by this.
  ## @var name
  # Name of this object.
  ## @var value
  # A string value for this parameter.

  ## Constructor; either 'parameter' or 'idf', 'kid' and 'value' must be passed
  ## as keyword argument(s).
  # @param self the object pointer.
  # @param parameter A libsedml.SedAlgorithmParameter object; optional (default:
  # None).
  # @param idf A unique identifier; optional (default: None).
  # @param name A name for 'self'; optional (default: None).
  # @param kid A valid KiSAO identifier; optional (default: None).
  # @param value A string value for this parameter; optional (default: None).
  def __init__(self, parameter=None, idf=None, name=None, kid=None, value=None):
    if parameter is None and (idf is None or kid is None or value is None):
      sys.exit("Error; either 'parameter' or 'idf', 'kid' and 'value' must " +
        "be passed as keyword argument(s).")
    else:
      if parameter is not None:
        self.id = parameter.getId()
        self.name = parameter.getName()
        self.kisao_id = parameter.getKisaoID()
        self.value = parameter.getValue()
      else:
        self.id = idf
        self.name = name
        self.kisao_id = kid
        self.value = value

  ## Getter. Returns self.id.
  # @param self The object pointer.
  # @return self.id
  def get_id(self):
    return self.id

  ## Getter. Returns self.kisao_id.
  # @param self The object pointer.
  # @return self.kisao_id
  def get_kisao_id(self):
    return self.kisao_id

  ## Getter. Returns self.name.
  # @param self The object pointer.
  # @return self.name
  def get_name(self):
    return self.name

  ## Getter. Returns self.value.
  # @param self The object pointer.
  # @return self.value
  def get_value(self):
    return self.value

  ## Setter for self.id.
  # @param self The object pointer.
  # @param id New value for self.id
  def set_id(self, id):
    self.id = id

  ## Setter for self.kisao_id.
  # @param self The object pointer.
  # @param kisao_id New value for self.kisao_id
  def set_kisao_id(self, kisao_id):
    self.kisao_id = kisao_id

  ## Setter for self.name.
  # @param self The object pointer.
  # @param name New value for self.name
  def set_name(self, name):
    self.name = name

  ## Setter for self.value.
  # @param self The object pointer.
  # @param value New value for self.value
  def set_value(self, value):
    self.value = value
