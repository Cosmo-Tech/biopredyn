## @package biopredyn
# Work flow handling package; a work flow is defined as a sequence of Task
# elements (in the SED-ML sense) to be executed using one or several engines.

__author__ = "$Author$"
__date__ = "$Date$"
__copyright__ = "$Copyright: [2013] BioPreDyn $"
__credits__ = ["Bertrand Moreau"]
__license__ = "BSD"
__maintainer__ = ["Bertrand Moreau"]
__email__ = "bertrand.moreau@thecosmocompany.com"
__version__ = "$Revision$"
# $Source$

import libsedml
import COPASI
from matplotlib import pyplot as plt
import numpy as np
import model

## Class for COPASI-based work flows i.e. using COPASI as main simulation
## engine.
class CopasiFlow:
  
  def __init__(self, file):
    simulation = SedMLFlow(file)
    self.sedml = simulation.check()
  
  # Parse self.sedml and run the tasks it contains using COPASI; stores the
  # resulting time series into self.timeseries
  def run(self):
    # Parse the list of tasks in the input file
    for t in self.sedml.getListOfTasks():
      model_source = self.sedml.getModel(t.getModelReference()).getSource()
      # Import the model to COPASI
      cop_datamodel = COPASI.CCopasiDataModel()
      cop_datamodel.importSBML(model_source)
      # Import simulation
      sed_simulation = self.sedml.getSimulation(t.getSimulationReference())
      # Case where the task is a uniform time course
      if ( sed_simulation.getElementName() == "uniformTimeCourse" ):
        cop_task = cop_datamodel.addTask(COPASI.CCopasiTask.timeCourse)
        cop_problem = cop_task.getProblem()
        # Required parameters are set from values in the input SED-ML file
        cop_problem.setDuration( sed_simulation.getOutputEndTime() -
                         sed_simulation.getOutputStartTime() )
        cop_problem.setStepNumber(sed_simulation.getNumberOfPoints())
        cop_problem.setOutputStartTime(sed_simulation.getOutputStartTime())
        cop_problem.setTimeSeriesRequested(True)
        # Deterministic method is chosen
        # TODO: acquire it from KiSAO value in SED-ML file
        cop_task.setMethodType(COPASI.CCopasiMethod.deterministic)
        # Run
        cop_task.process(True)
        # Save the results
        self.series = cop_task.getTimeSeries()
  
  ## Plot the results of the work flow encoded in self.sedml using the list of
  ## outputs defined in self.sedml.
  # @param self The object pointer.
  def plot(self):
    figure = plt.figure()
    print self.series.getNumVariables()
#     x = self.series.getConcentrationDataForIndex(0)
#     for i in range(1,self.series.getNumVariables()):
#       plt.plot(x, self.series.getConcentrationDataForIndex(i))
#     plt.show(figure)

## Class for SED-ML generic work flows i.e. using libSBMLSim as main simulation
## engine.
class SedMLFlow:
  
  ## Constructor.
  # @param self The object pointer.
  # @param file Address of the SED-ML file to be read.
  def __init__(self, file):
    reader = libsedml.SedReader()
    self.address = file
    self.file = reader.readSedML(file)
  
  ## SED-ML compliance check function.
  # Check whether self.file is compliant with the SED-ML standard; if
  # not, boolean value false is returned and the first error code met by the
  # reader is printed; if yes, the method returns a pointer to the SED-ML model
  # instead.
  # @param self The object pointer.
  def check(self):
    if self.file.getNumErrors() > 0:
      print("Error code " + str(self.file.getError(0).getErrorId()) +
            " when opening file: " +
            str(self.file.getError(0).getShortMessage()))
      sys.exit(2)
    else:
      print("Document " + self.address + " is SED-ML compliant.")
      # check compatibility with SED-ML level 1
      print( str(self.file.checkCompatibility(self.file)) +
             " compatibility errors with SED-ML L1." )
      return self.file