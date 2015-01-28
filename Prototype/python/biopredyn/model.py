#!/usr/bin/env python
# coding=utf-8

## @package biopredyn
## Copyright: [2012-2015] The CoSMo Company, All Rights Reserved
## License: BSD 3-Clause

import libsbml
import libsedml
from lxml import etree
import sys
import urlparse
from bioservices import BioModels
import change

## Class for SedML model manipulation.
class Model:
  ## @var source
  # Address of the SBML file associated with the object.
  ## @var id
  # A unique identifier for this object.
  ## @var namespaces
  # Dictionary of namespaces defining the associated SBML model.
  ## @var tree
  # XML tree representation of a SBML model.
  ## @var changes
  # A list of changes to be applied to the model before it runs.
  ## @var resource_manager
  # Resource manager for the current work flow.
  
  ## Constructor; either 'model' and 'workflow' or 'source' and 'idf' must be
  ## passed to the constructor.
  # @param self The object pointer.
  # @param manager An instance of ResourceManager.
  # @param model A SED-ML model element; optional (default None). If a model is
  # provided, this will be initialized as an element of a SED-ML workflow (the
  # list of changes will be initialized); if not, this will be initialized as
  # a stand-alone SBML model using the input source and idf (if provided).
  # @param workflow A WorkFlow object; required if a SED-ML model is provided
  # (default None).
  # @param source The address of a SBML model file; optional (default None).
  # @param idf A unique identifier; optional (default None).
  # @param name A name for 'self'; optional (default: None).
  def __init__(self, manager, model=None, workflow=None, source=None, idf=None,
    name=None):
    if (model is None or workflow is None) and (source is None or idf is None):
      sys.exit("Error: either 'model' and 'workflow' or 'source' and 'idf' " +
               "input arguments must be passed to the constructor.")
    else:
      self.resource_manager = manager
      self.changes = []
      if model is not None:
        self.id = model.getId()
        self.name = model.getName()
        self.source = model.getSource()
        for c in model.getListOfChanges():
          if c.getElementName() == "changeAttribute":
            self.add_change(change.ChangeAttribute(self, change=c))
          elif c.getElementName() == "computeChange":
            self.add_change(change.ComputeChange(workflow, self, change=c))
          elif c.getElementName() == "changeXML":
            self.add_change(change.ChangeXML(self, change=c))
          elif c.getElementName() == "addXML":
            self.add_change(change.AddXML(self, change=c))
          elif c.getElementName() == "removeXML":
            self.add_change(change.RemoveXML(self, change=c))
      else:
        self.id = idf
        self.name = name
        self.source = source
      self.init_tree()
      self.init_namespaces()
  
  ## String representation of this. Displays it as a hierarchy.
  # @param self The object pointer.
  # @return A string representing this as a hierarchy.
  def __str__(self):
    tree = "  |-model id=" + self.id + " source=" + self.source + "\n"
    tree += "    |-listOfChanges\n"
    for c in self.changes:
      tree += str(c)
    return tree

  ## Appends the input biopredyn.change.Change object to self.changes.
  # @param self The object pointer.
  # @param ch A biopredyn.change.Change object.
  def add_change(self, ch):
    self.changes.append(ch)
  
  ## Sequentially apply all changes in the model.
  # @param self The object pointer.
  def apply_changes(self):
    for c in self.changes:
      c.apply()
  
  ## SBML compliance check function.
  # Checks whether self.file is compliant with the SBML standard.
  # If not, boolean value false is returned and the first error code met by the
  # reader is printed; if yes, the method returns a pointer to the SBML model
  # instead.
  # @param self The object pointer.
  # @return True if self is SBML compliant, False otherwise.
  def check(self):
    doc = self.get_sbml_doc()
    if doc.getNumErrors() > 0:
      print("Error code " + str(doc.getError(0).getErrorId()) + " at line " +
            str(doc.getError(0).getLine()) + " when opening file: " +
            str(doc.getError(0).getShortMessage()))
      return False
    else:
      print("Model " + doc.getModel().getName() + " is SBML compliant.")
      # Check compatibility with different versions of SBML
      print( str(doc.checkL1Compatibility()) +
             " compatibility errors with SBML L1." )
      print( str(doc.checkL2v1Compatibility()) +
             " compatibility errors with SBML L2v1." )
      print( str(doc.checkL2v2Compatibility()) +
             " compatibility errors with SBML L2v2." )
      print( str(doc.checkL2v3Compatibility()) +
             " compatibility errors with SBML L2v3." )
      print( str(doc.checkL2v4Compatibility()) +
             " compatibility errors with SBML L2v4." )
      print( str(doc.checkL3v1Compatibility()) +
             " compatibility errors with SBML L3v1." )
      return True
  
  ## Evaluate the input XPath expression and return the corresponding element(s)
  ## of self.tree, if any.
  # @param self The object pointer.
  # @param xpath An XPath expression related to self.tree.
  # @return target A list containing the elements of self.tree matching the
  # input xpath.
  def evaluate_xpath(self, xpath):
    target = self.tree.xpath(xpath, namespaces=self.namespaces)
    if len(target) > 0:
      return target
    else:
      sys.exit("XPath error: " + xpath + " could not be resolved in " +
               self.source)
  
  ## Getter. Returns self.changes.
  # @param self The object pointer.
  # @return self.changes
  def get_changes(self):
    return self.changes

  ## Returns the list of SBML species identifiers in the COPASI.CTimeSeries
  ## sense: uses 'name' attributes if they exist, 'id' attributes otherwise.
  # @param self The object pointer.
  # @return identifiers A list of string identifiers.
  def get_species_copasi_ids(self):
    sbml_doc = self.get_sbml_doc()
    identifiers = []
    for s in sbml_doc.getModel().getListOfSpecies():
      if (len(s.getName()) > 0):
        identifiers.append(s.getName())
      else:
        identifiers.append(s.getId())
    return identifiers
  
  ## Getter. Returns self.source.
  # @param self The object pointer.
  # @return self.source
  def get_source(self):
    return self.source
  
  ## Setter for self.source.
  # @param self The object pointer.
  # @param source New value for self.source.
  def set_source(self, source):
    self.source = source
  
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
  
  ## Converts self.tree as a SBMLDocument object and return it.
  # @param self The object pointer.
  # @return model A SBMLDocument object.
  def get_sbml_doc(self):
    reader = libsbml.SBMLReader()
    doc = reader.readSBMLFromString(
      etree.tostring(self.tree, encoding='UTF-8', xml_declaration=True))
    return doc
  
  ## Getter. Returns self.tree.
  # @param self The object pointer.
  # @return self.tree
  def get_tree(self):
    return self.tree
  
  ## Setter for self.tree.
  # @param self The object pointer.
  # @param tree New value for self.tree.
  def set_tree(self, tree):
    self.tree = tree
  
  ## Extracts namespaces from self.tree and stores them as a dictionary in
  ## self.namespaces.
  # @param self The object pointer.
  def init_namespaces(self):
    self.namespaces = dict()
    doc = self.get_sbml_doc()
    ns = doc.getNamespaces()
    for n in range(ns.getLength()):
      if not ns.getPrefix(n) and ('sbml' in ns.getURI(n)):
        # Case where no prefix is provided for SBML namespace
        self.namespaces['sbml'] = ns.getURI(n)
      else:
        self.namespaces[ns.getPrefix(n)] = ns.getURI(n)
  
  ## Retrieves the SBML document encoded in self.source and stores it as a XML
  ## tree in self.tree.
  # @param self The object pointer.
  def init_tree(self):
    url = urlparse.urlparse(self.source)
    if url.scheme == 'urn':
      # Case where the model is identified by a BioModels URN
      split = self.source.split(':')
      s = BioModels()
      doc = s.getModelSBMLById(split.pop())
      self.tree = etree.fromstring(doc.encode('utf8'))
    else:
      file = self.resource_manager.get_resource(self.source)
      self.tree = etree.parse(file)
  
  ## Print a string representation of self.tree.
  # @param self The object pointer.
  def print_tree(self):
    print(etree.tostringlist(self.tree, pretty_print=True))
  
  ## Write self.tree as a SBML document at the input 'filename' location.
  # @param self The object pointer.
  # @param filename Absolute path to the location where the output file should
  # be written.
  def write_sbml(self, filename):
    writer = libsbml.SBMLWriter()
    doc = self.get_sbml_doc()
    writer.writeSBMLToFile(doc, filename)
