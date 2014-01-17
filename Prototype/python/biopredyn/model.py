# coding=utf-8

## @package biopredyn
## @author: $Author$
## @date: $Date$
## @copyright: $Copyright: [2013-2014] BioPreDyn $
## @version: $Revision$

import libsedml
import libsbml
import sys

## Class for SBML model manipulation.
class SBMLModel:
  ## @var source
  # Address of the SBML file associated with the object.
  ## @var id
  # A unique identifier for this object.
  ## @var model
  # An SBML model.
  
  ## Constructor; one of the two argument 'model' or 'source' must be passed to
  ## the constructor.
  # @param self The object pointer.
  # @param manager An instance of ResourceManager.
  # @param model A SED-ML model element; optional (default None).
  # @param source The address of a SBML model file; optional (default None).
  def __init__(self, manager, model=None, source=None):
    reader = libsbml.SBMLReader()
    if model is not None:
      self.id = model.getId()
      self.source = model.getSource()
    elif source is not None:
      self.source = source
    file = manager.get_resource(self.source)
    self.model = reader.readSBMLFromString(file.read())

  
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
  # @return self.model
  def check(self):
    if self.model.getNumErrors() > 0:
      print("Error code " + str(self.model.getError(0).getErrorId()) +
            " when opening file: " +
            str(self.model.getError(0).getShortMessage()))
      sys.exit(2)
    else:
      print("Model " + self.model.getModel().getName() + " is SBML compliant.")
      # Check compatibility with different versions of SBML
      print( str(self.model.checkL1Compatibility()) +
             " compatibility errors with SBML L1." )
      print( str(self.model.checkL2v1Compatibility()) +
             " compatibility errors with SBML L2v1." )
      print( str(self.model.checkL2v2Compatibility()) +
             " compatibility errors with SBML L2v2." )
      print( str(self.model.checkL2v3Compatibility()) +
             " compatibility errors with SBML L2v3." )
      print( str(self.model.checkL2v4Compatibility()) +
             " compatibility errors with SBML L2v4." )
      print( str(self.model.checkL3v1Compatibility()) +
             " compatibility errors with SBML L3v1." )
      return self.model
  
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
  
  ## Getter. Returns self.model.
  # @param self The object pointer.
  # @return self.model
  def get_model(self):
    return self.model