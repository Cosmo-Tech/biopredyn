__author__     = "Bertrand Moreau"
__copyright__  = "Copyright 2013, BioPreDyn"
__credits__    = ["Bertrand Moreau"]
__license__    = "BSD"
__version__    = "0.1"
__maintainer__ = ["Bertrand Moreau"]
__email__      = "bertrand.moreau@thecosmocompany.com"
__status__     = "Alpha"

import libsbml

class SBMLModel:
  
  def __init__(self, file):
    reader = libsbml.SBMLReader()
    self.address = file
    self.file = reader.readSBML(file)
  
  # Check whether the self.file is compliant with the SBML standard; if
  # not, boolean value false is returned and the first error code met by the
  # reader is printed; if yes, the method returns a pointer to the SBML model
  # instead.
  def Check(self):
    if self.file.getNumErrors() > 0:
      print("Error code " + str(self.file.getError(0).getErrorId()) +
            " when opening file: " +
            str(self.file.getError(0).getShortMessage()))
      sys.exit(2)
    else:
      print("Model " + self.file.getModel().getName() + " is SBML compliant.")
      # Check compatiblity with different versions of SBML
      print( str(self.file.checkL1Compatibility()) +
             " compatibility errors with SBML L1." )
      print( str(self.file.checkL2v1Compatibility()) +
             " compatibility errors with SBML L2v1." )
      print( str(self.file.checkL2v2Compatibility()) +
             " compatibility errors with SBML L2v2." )
      print( str(self.file.checkL2v3Compatibility()) +
             " compatibility errors with SBML L2v3." )
      print( str(self.file.checkL2v4Compatibility()) +
             " compatibility errors with SBML L2v4." )
      print( str(self.file.checkL3v1Compatibility()) +
             " compatibility errors with SBML L3v1." )
      return self.file