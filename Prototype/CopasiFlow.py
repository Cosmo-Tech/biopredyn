__author__     = "Bertrand Moreau"
__copyright__  = "Copyright 2013, BioPreDyn"
__credits__    = ["Bertrand Moreau"]
__license__    = "BSD"
__version__    = "0.1"
__maintainer__ = ["Bertrand Moreau"]
__email__      = "bertrand.moreau@thecosmocompany.com"
__status__     = "Alpha"

import COPASI
import SBMLModel
import SedMLFlow
from matplotlib import pyplot as plt
import numpy as np

class CopasiFlow:
  
  def __init__(self, file):
    simulation = SedMLFlow.SedMLFlow(file)
    self.sedml = simulation.Check()
  
  # Parse self.sedml and run the tasks it contains using COPASI; stores the
  # resulting time series into self.timeseries
  def Run(self):
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
  
  # Plot self.series
  def Plot(self):
    figure = plt.figure()
    print self.series.getNumVariables()
#     x = self.series.getConcentrationDataForIndex(0)
#     for i in range(1,self.series.getNumVariables()):
#       plt.plot(x, self.series.getConcentrationDataForIndex(i))
#     plt.show(figure)