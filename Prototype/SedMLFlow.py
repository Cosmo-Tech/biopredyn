__author__     = "Bertrand Moreau"
__copyright__  = "Copyright 2013, BioPreDyn"
__credits__    = ["Bertrand Moreau"]
__license__    = "BSD"
__version__    = "0.1"
__maintainer__ = ["Bertrand Moreau"]
__email__      = "bertrand.moreau@thecosmocompany.com"
__status__     = "Alpha"

import libsedml

class SedMLFlow:
  
  def __init__(self, file):
    reader = libsedml.SedReader()
    self.address = file
    self.file = reader.readSedML(file)
  
  # Check whether self.file is compliant with the SED-ML standard; if
  # not, boolean value false is returned and the first error code met by the
  # reader is printed; if yes, the method returns a pointer to the SED-ML model
  # instead.
  def Check(self):
    if self.file.getNumErrors() > 0:
      print("Error code " + str(self.file.getError(0).getErrorId()) +
            " when opening file: " +
            str(self.file.getError(0).getShortMessage()))
      sys.exit(2)
    else:
      print("Document " + self.address + " is SED-ML compliant.")
      # Check compatibility with SED-ML level 1
      print( str(self.file.checkCompatibility(self.file)) +
             " compatibility errors with SED-ML L1." )
      return self.file