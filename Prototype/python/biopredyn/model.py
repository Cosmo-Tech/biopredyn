# coding=utf-8

## @package biopredyn
## @author: $Author$
## @date: $Date$
## @copyright: $Copyright: [2013-2014] BioPreDyn $
## @version: $Revision$

import libsedml
import libsbml
from lxml import etree
from StringIO import StringIO
import sys
import urlparse
from bioservices import BioModels

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
  
  ## Constructor; one of the two argument 'model' or 'source' must be passed to
  ## the constructor.
  # @param self The object pointer.
  # @param manager An instance of ResourceManager.
  # @param model A SED-ML model element; optional (default None). If a model is
  # provided, this will be initialized as an element of a SED-ML workflow (the
  # list of changes will be initialized); if not, this will be initialized as
  # a stand-alone SBML model using the input source (if provided).
  # @param source The address of a SBML model file; optional (default None).
  def __init__(self, manager, model=None, source=None):
    if (model is None) and (source is None):
      sys.exit("Error: one of the input arguments 'model' or 'source' must" +
               " be passed to the constructor.")
    else:
      if model is not None:
        self.id = model.getId()
        self.source = model.getSource()
        # TODO: populate list of changes
      elif source is not None:
        self.source = source
      self.init_tree(manager)
      self.init_namespaces()
  
  ## String representation of this. Displays it as a hierarchy.
  # @param self The object pointer.
  # @return A string representing this as a hierarchy.
  def __str__(self):
    tree = "  |-model id=" + self.id + " source=" + self.source + "\n"
    return tree
  
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
      print("Error code " + str(doc.getError(0).getErrorId()) +
            " when opening file: " +
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
  def evaluate_xpath(self, xpath):
    return self.tree.xpath(xpath, self.namespaces)
  
  ## Getter. Returns self.source.
  # @param self The object pointer.
  # @return self.source
  def get_source(self):
    return self.source
  
  ## Getter. Returns self.id.
  # @param self The object pointer.
  # @return self.id
  def get_id(self):
    return self.id
  
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
  
  ## Extracts namespaces from self.tree and stores them as a dictionary in
  ## self.namespaces.
  # @param self The object pointer.
  def init_namespaces(self):
    self.namespaces = dict()
    doc = self.get_sbml_doc()
    ns = doc.getNamespaces()
    for n in range(ns.getLength()):
      self.namespaces[ns.getPrefix(n)] = ns.getURI(n)
  
  ## Retrieves the SBML document encoded in self.source and stores it as a XML
  ## tree in self.tree.
  # @param self The object pointer.
  # @param manager A ResourceManager instance.
  def init_tree(self, manager):
    url = urlparse.urlparse(self.source)
    if url.scheme == 'urn':
      # Case where the model is identified by a BioModels URN
      split = self.source.split(':')
      s = BioModels()
      doc = s.getModelSBMLById(split.pop())
      self.tree = etree.fromstring(doc.encode('utf8'))
    else:
      file = manager.get_resource(self.source)
      self.tree = etree.parse(file)