## @package biopredyn
## @author: $Author$
## @date: $Date$
## @copyright: $Copyright: [2013] BioPreDyn $
## @version: $Revision$

import sys
import libsedml
from matplotlib import pyplot as plt
import numpy as np
import model, output, result, task

## Class for SED-ML generic work flows.
class WorkFlow:
  ## @var address
  # Address of the SED-ML file associated with the object.
  ## @var outputs
  # A list of Output elements
  ## @var sedml
  # A SED-ML document.
  ## @var tasks
  # A list of Task elements.
  
  ## Constructor.
  # @param self The object pointer.
  # @param file Address of the SED-ML file to be read.
  def __init__(self, file):
    self.address = file
    reader = libsedml.SedReader()
    self.sedml = reader.readSedML(file)
    self.check()
    self.tasks = []
    # Parsing self.sedml for task elements
    for t in self.sedml.getListOfTasks():
      # TODO: check whether the tools are set
      self.tasks.append(task.Task(t, self.sedml))
    self.outputs = []
    # Parsing self.sedml for output elements
    for o in self.sedml.getListOfOutputs():
      name = o.getElementName()
      if name == "SedPlot2D":
        self.outputs.append(output.Plot2D(o))
      elif name == "SedPlot3D":
        self.outputs.append(output.Plot3D(o))
      elif name == "SedReport":
        self.outputs.append(output.Report(o))
      else:
        self.outputs.append(output.Output(o))
  
  ## SED-ML compliance check function.
  # Check whether self.sedml is compliant with the SED-ML standard; if
  # not, boolean value false is returned and the first error code met by the
  # reader is printed; if yes, the method returns a pointer to the SED-ML model
  # instead.
  # @param self The object pointer.
  # @return self.sedml
  def check(self):
    if self.sedml.getNumErrors() > 0:
      print("Error code " + str(self.sedml.getError(0).getErrorId()) +
            " when opening file: " +
            str(self.sedml.getError(0).getShortMessage()))
      sys.exit(2)
    else:
      print("Document " + self.address + " is SED-ML compliant.")
      # check compatibility with SED-ML level 1
      print( str(self.sedml.checkCompatibility(self.sedml)) +
             " compatibility errors with SED-ML L1." )
      return self.sedml
  
  ## Executes the pipeline encoded in self.sedml.
  # Each task in self.tasks is executed.
  # libSBMLSim is used as simulation engine.
  # @param self The object pointer.
  def run_tasks(self):
    # Parse the list of tasks in the input file
    for t in self.tasks:
      t.run()
  
  ## Parse self.outputs and produce the corresponding outputs.
  # @param self The object pointer.
  # @param interactive Boolean value stating whether the plots have to be
  #   drawn in interactive mode or not.
  def process_outputs(self, interactive):
    for o in self.outputs:
      print "TODO"
  
  ## Getter. Returns self.address.
  # @param self The object pointer.
  def get_address(self):
    return self.address
  
  ## Getter. Returns self.outputs.
  # @param self The object pointer.
  def get_outputs(self):
    return self.outputs
  
  ## Getter. Returns self.sedml.
  # @param self The object pointer.
  def get_sedml(self):
    return self.sedml
  
  ## Getter. Returns a task referenced by the input id listed in self.tasks.
  # @param self The object pointer.
  # @param id The id of the task to be returned.
  # @return task A task object.
  def get_task_by_id(self, id):
    for t in self.tasks:
      if t.getId() == id:
        return t
    print("Task not found: " + id)
    return 0
  
  ## Getter. Returns self.tasks.
  # @param self The object pointer.
  def get_tasks(self):
    return self.tasks