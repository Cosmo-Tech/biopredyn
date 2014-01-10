# coding=utf-8

## @package biopredyn
## @author: $Author$
## @date: $Date$
## @copyright: $Copyright: [2013-2014] BioPreDyn $
## @version: $Revision$

import sys
import os
import matplotlib.pyplot as plt

# Find the path to the libsedml Python package
for r, d, f in os.walk(os.path.join(os.path.dirname(__file__), '../bin')):
  for filename in f:
    if filename == "libsedml.py":
      sys.path.append(os.path.abspath(r))
      break

# Find the path to the libsbmlsim Python package
for r, d, f in os.walk(os.path.join(os.path.dirname(__file__), '../bin')):
  for filename in f:
    if filename == "libsbmlsim.py":
      sys.path.append(os.path.abspath(r))
      break

# Find the path to the libnuml Python package
for r, d, f in os.walk(os.path.join(os.path.dirname(__file__), '../bin')):
  for filename in f:
    if filename == "libnuml.py":
      sys.path.append(os.path.abspath(r))
      break

# Find the path to the biopredyn Python package
for r, d, f in os.walk(os.path.join(os.path.dirname(__file__),
  '../python/biopredyn')):
  for filename in f:
    if filename == "main.py":
      sys.path.append(os.path.abspath(r))
      break

import getopt
import sys
import textwrap
import numpy as np
import matplotlib.pyplot as plt

import libsbml
import libsedml
import libnuml
import model
import workflow
import result

COMMAND_SYNTAX_MESSAGE = 'python main.py /path/to/input/file [options]'

HELP_MESSAGE = "Test file for BioPreDyn project; contains all tests."

# Optional parameters.
HELP_OPTION = {
"help"    : [  "Display this help message."],
"sbml"    : [  "Open the input file as an SBML model; SBML compliance will " +
              "be checked."],
"sedml"   : [  "Open the input SED-ML model file, execute its tasks using " +
              "the libSBMLSim library, process its graphical outputs and " +
              "display them."],
"numl"    : [  "Open the input NuML result file, import it in a Result " +
              "object and plot its content."],
}

HELP_KEYWORD_SIZE = 16   # Left column
HELP_WRAP_SIZE = 79   # Total. 79 is windows limit

## Display help information.
def print_help():
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
    print_help_argument(arg, HELP_OPTION[arg])

## Display help information for the input option.
# @param arg Name of the help option to be displayed.
# @param listhelplines Information about the help option being displayed.
def print_help_argument(arg, listhelplines):
  firstLine = True
  # Go trough list of help line
  for helpline in listhelplines:
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
  opts, args = getopt.getopt(sys.argv[2:], "", [
      'help', 'sbml', 'sedml', 'numl'])
except getopt.error, msg:
  print( COMMAND_SYNTAX_MESSAGE )
  print( "Type main.py --help for more information" )
  print( msg )
  sys.exit(2)

for o, a in opts:
  if o == "--help":
    print_help()
    sys.exit(0)
  elif o == "--sbml":
    model = model.SBMLModel(source=sys.argv[1])
    model.check()
  elif o == "--sedml":
    flow = workflow.WorkFlow(sys.argv[1])
    flow.run_tasks()
    flow.process_outputs(True)
  elif o == "--numl":
    res = result.Result()
    res.import_from_numl_file(sys.argv[1])
    plot = plt.figure("numl_test")
    ax = plot.add_subplot(111)
    for i in res.get_result():
      if str.lower(i) != "time":
        ax.plot(res.get_time_steps(), res.get_quantities_per_species(i))
    plot.show()

