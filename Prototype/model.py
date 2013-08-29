## @package biopredyn
# Model handling module; the only accepted format for models in package
# biopredyn is SBML so far.

__author__ = "$Author$"
__date__ = "$Date$"
__copyright__ = "$Copyright: [2013] BioPreDyn $"
__credits__ = ["Bertrand Moreau"]
__license__ = "BSD"
__maintainer__ = ["Bertrand Moreau"]
__email__ = "bertrand.moreau@thecosmocompany.com"
__version__ = "$Revision$"
# $Source$

import libsbml

## Class for SBML model manipulation.
class SBMLModel:
  
  ## Constructor.
  # @param self The object pointer.
  # @param file Address of the SBML file to be read.
  def __init__(self, file):
    reader = libsbml.SBMLReader()
    self.address = file
    self.model = reader.readSBML(model)
  
  ## SBML compliance check function.
  # Checks whether self.file is compliant with the SBML standard.
  # If not, boolean value false is returned and the first error code met by the
  # reader is printed; if yes, the method returns a pointer to the SBML model
  # instead.
  # @param self The object pointer.
  def check(self):
    if self.model.getNumErrors() > 0:
      print("Error code " + str(self.model.getError(0).getErrorId()) +
            " when opening file: " +
            str(self.model.getError(0).getShortMessage()))
      sys.exit(2)
    else:
      print("Model " + self.model.getModel().getName() + " is SBML compliant.")
      # check compatiblity with different versions of SBML
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