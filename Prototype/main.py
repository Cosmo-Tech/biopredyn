#!/usr/bin/python

__author__     = "Bertrand Moreau"
__copyright__  = "Copyright 2013, BioPreDyn"
__credits__    = ["Bertrand Moreau"]
__license__    = "BSD"
__version__    = "0.1"
__maintainer__ = ["Bertrand Moreau"]
__email__      = "bertrand.moreau@thecosmocompany.com"
__status__     = "Alpha"

# Third-party dependencies
import getopt
import sys
import textwrap
import libsbml
import libsedml
import COPASI
import numpy as np
import matplotlib.pyplot as plt

# Internal dependencies
import SBMLModel
import SedMLFlow
import CopasiFlow

COMMAND_SYNTAX_MESSAGE = 'python main.py /path/to/input/file [options]'

HELP_MESSAGE = "This program is a prototype for the BioPreDyn software suite developed within the scope of the BioPreDyn FP7 project; it applies an analysis pattern to an SBML model defining a biological system."

# Optional parameters.
HELP_OPTION = {
"help"    : [  "Display this help message."],
"cobra"   : [  "Open the input file using the cobrapy library."],
"copasi"  : [  "Open the input SED-ML file and execute its tasks using the Copasi library."],
"sbml"    : [  "Open the input file as an SBML model; SBML compliance will be checked."],
"sedml"   : [  "Open the input file as an SED-ML model; SED-ML compliance will be checked."],
}

HELP_KEYWORD_SIZE = 16   # Left column
HELP_WRAP_SIZE = 79   # Total. 79 is windows limit

# Display help information.
def PrintHelp():
  # General help message
  print " "
  lines = textwrap.wrap(HELP_MESSAGE, HELP_WRAP_SIZE)
  for line in lines:
    print line
  print " "
  
  # Command syntax
  print "Usage: "
  print (COMMAND_SYNTAX_MESSAGE)
  print " "
  print "List of available options: "
  
  # Optional arguments
  for arg in HELP_OPTION:
    PrintHelpArgument(arg, HELP_OPTION[arg])

# Display help information for the input option.
def PrintHelpArgument(arg, listHelpLines):
  firstLine = True
  # Go trough list of help line
  for helpline in listHelpLines:
    lines = textwrap.wrap(helpline, HELP_WRAP_SIZE - HELP_KEYWORD_SIZE)
    for line in lines:
      # First line: Print arg name.
      if firstLine:
        print ('--' + arg).ljust(HELP_KEYWORD_SIZE) + line
        firstLine = False
      else:
        print ''.ljust(HELP_KEYWORD_SIZE) + line
  print ""

# main
try:
  opts, args = getopt.getopt(sys.argv[2:], "",
                             ['help', 'cobra', 'copasi', 'sbml', 'sedml'])
except getopt.error, msg:
  print( COMMAND_SYNTAX_MESSAGE )
  print( "Type main.py --help for more information" )
  print( msg )
  sys.exit(2)

for o, a in opts:
  print str(o)
  if o == "--help":
    PrintHelp()
    sys.exit(0)
  elif o == "--sbml":
    model = SBMLModel.SBMLModel(sys.argv[1])
    model.Check()
  elif o == "--sedml":
    flow = SedMLFlow.SedMLFlow(sys.argv[1])
    flow.Check()
  elif o == "--cobra":
    print("Something will happen with cobrapy here soon.")
  elif o == "--copasi":
    flow = CopasiFlow.CopasiFlow(sys.argv[1])
    flow.Run()
    flow.Plot()