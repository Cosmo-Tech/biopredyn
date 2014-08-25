#!/usr/bin/env python
# coding=utf-8

import libsbml
from COPASI import *
import sys
from random import random
from biopredyn import result as res
from biopredyn import resources
from matplotlib import pyplot as plt
import numpy as np

def main():
  # required inputs
  model_file = "FEBS_antimony_fitted.xml"
  validation_data = "validation_data.txt"
  start = 0.0
  end = 20.0
  observables = ["sp_C"] # names of the observables

  # create a datamodel
  data_model = CCopasiRootContainer.addDatamodel()
  # first we load a simple model
  try:
    # load the model 
    data_model.importSBML(model_file)
  except:
    sys.stderr.write("Error while importing the model.\n")
    return 1

  model = data_model.getModel()

  # importing data as a res.Result object column-aligned
  rm = resources.ResourceManager()
  val_data = res.Result()
  metabolites = val_data.import_from_csv_file(
    validation_data, rm, separator=',', alignment='column')
  steps = len(val_data.get_time_steps()) - 1 # N intervals mean N+1 time steps

  # we run a simulation with the fitted model
  trajectory_task = data_model.getTask("Time-Course")

  # run a deterministic time course
  trajectory_task.setMethodType(CCopasiMethod.deterministic)
  trajectory_task.getProblem().setModel(data_model.getModel())
  problem = trajectory_task.getProblem()

  # input parameters are used for the simulation
  problem.setStepNumber(steps)
  model.setInitialTime(start)
  problem.setDuration(end)

  result = True
  try:
    result = trajectory_task.processWithOutputFlags(
      True, CCopasiTask.ONLY_TIME_SERIES)
  except:
    sys.stderr.write(" Error. Running the time course simulation failed.\n")
    if CCopasiMessage.size() > 0:
      sys.stderr.write(CCopasiMessage.getAllMessageText(True) + "\n")
      return 1
  if result == False:
    sys.stderr.write(
      "An error occured while running the time course simulation.\n")
    if CCopasiMessage.size() > 0:
      sys.stderr.write(CCopasiMessage.getAllMessageText(True) + "\n")
      return 1

  # we use BioPreDyn API for extracting the results
  model_result = res.Result()
  model_result.import_from_copasi_time_series(
    trajectory_task.getTimeSeries())
  time = np.array(model_result.get_time_steps())

  # plotting residuals vs fitted values
  for m in metabolites:
    if not str.lower(m).__contains__("time") and m in observables:
      plt.figure(m)
      prediction = np.array(model_result.get_quantities_per_species(m))
      experiment = np.array(val_data.get_quantities_per_species(m))
      residuals = experiment - prediction
      print prediction
      print residuals
      plt.plot(prediction, residuals, label=m)
      plt.legend()

  plt.show()

if(__name__ == '__main__'):
  main() 
