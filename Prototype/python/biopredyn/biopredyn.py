#!/usr/bin/env python
# coding=utf-8

## @package biopredyn
## Copyright: [2012-2015] The CoSMo Company, All Rights Reserved
## License: BSD 3-Clause

import sys
import getopt
import textwrap
import libsbml
import libsedml
import libnuml
import model, workflow, result, resources
import matplotlib.pyplot as plt

COMMAND_SYNTAX_MESSAGE = 'python biopredyn.py [options]'

HELP_MESSAGE = "This program is a prototype for the BioPreDyn software suite developed within the scope of the BioPreDyn FP7 project; it applies an analysis pattern encoded as a SEDML file to a SBML model defining a biological system."

# Optional parameters.
HELP_OPTION = {
"-h, --help"   : [  "Display this help message."],
"--sbml"       : [  "Open the input file as an SBML model; SBML compliance " +
                  "will be checked."],
"--sedml"      : [  "Open the input SED-ML model file, execute its tasks " +
                  "using the libSBMLSim library, process its graphical " +
                  "outputs and display them."],
"--numl"       : [  "Open the input NuML result file, import it in a Result " +
                  "object and plot its content."],
"-o, --output" : [  "Write the result of the SEDML experiment in the input " +
                  ".csv ot .xml file."],
"--csv"        : [  "Open the input CSV result file, import it in a Result " +
                  "object and plot its content."]
}

HELP_KEYWORD_SIZE = 16   # Left column
HELP_WRAP_SIZE = 79   # Total. 79 is windows limit

## Display help information.
def print_help():
  # General help message
  print(" ")
  lines = textwrap.wrap(HELP_MESSAGE, HELP_WRAP_SIZE)
  for line in lines:
    print(line)
  print(" ")
  
  # Command syntax
  print("Usage: ")
  print(COMMAND_SYNTAX_MESSAGE)
  print(" ")
  print("List of available options: ")
  
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
        print((arg).ljust(HELP_KEYWORD_SIZE) + line)
        firstLine = False
      else:
        print(''.ljust(HELP_KEYWORD_SIZE) + line)
  print("")

# main
try:
  opts, args = getopt.getopt(sys.argv[1:], 'o:', [
      'help', 'sbml=', 'sedml=', 'numl=', 'output=', 'csv='])
except getopt.error as msg:
  print( COMMAND_SYNTAX_MESSAGE )
  print( "Type biopredyn.py --help for more information" )
  print( msg )
  sys.exit(2)

output = None

for o, a in opts:
  if o in ("--help", "-h"):
    print_help()
    sys.exit(0)
  elif o in ("--output", "-o"):
    output = a

# Installing resource manager
manager = resources.ResourceManager()

for o, a in opts:
  if o == "--sbml":
    model = model.Model(manager, source=a)
    model.check()
  elif o == "--sedml":
    flow = workflow.WorkFlow(a, res_man=manager)
    flow.run_tasks()
    flow.process_outputs(test=False, filename=output)
  elif o == "--numl":
    res = result.TimeSeries()
    res.import_from_numl_file(a, manager)
    plt.figure("numl_test")
    for i in res.get_result():
      if str.lower(i) != "time":
        plt.plot(res.get_time_steps(), res.get_quantities_per_species(i))
    plt.legend()
    plt.show()
  elif o == "--csv":
    res = result.TimeSeries()
    res.import_from_csv_file(a, manager)
    values = res.get_result()
    plt.figure("csv_test")
    for i in res.get_result():
      if str.lower(i) != "time":
        plt.plot(res.get_time_steps(), res.get_quantities_per_species(i))
    plt.legend()
    plt.show()
