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
from scipy.stats import norm, pearsonr
from scikits.statsmodels.sandbox.stats.runs import runstest_1samp

def main():
  # required inputs
  model_file = "FEBS_antimony_fitted.xml"
  validation_data = "validation_data.txt"
  start = 0.0
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
  end = val_data.get_time_steps()[-1]
  steps = len(val_data.get_time_steps())

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

  # using BioPreDyn API for extracting the results
  model_result = res.Result()
  model_result.import_from_copasi_time_series(
    trajectory_task.getTimeSeries())

  # because science is fun
  plt.xkcd()

  for m in metabolites:
    if not str.lower(m).__contains__("time") and m in observables:
      # plotting residuals vs fitted values
      plt.figure(m)
      plt.subplot(311)
      prediction = model_result.get_quantities_per_species(m)
      prediction.pop(0) # first element is removed (initial condition)
      prediction = np.array(prediction)
      experiment = np.array(val_data.get_quantities_per_species(m))
      residuals = experiment - prediction
      plt.plot(prediction, residuals, '+')
      plt.legend()
      # add y=0 line for reference and axis labels
      plt.axhline(0, color='grey')
      plt.xlabel('Fitted value')
      plt.ylabel('Residual')

      # plotting residuals versus time-ordered data
      plt.subplot(312)
      val_time_points = np.array(val_data.get_time_steps())
      plt.plot(val_time_points, residuals, 'r--')
      plt.legend()
      # add y=0 line for reference and axis labels
      plt.axhline(0, color='grey')
      plt.xlabel('Observation order')
      plt.ylabel('Residual')

      # plotting residuals as a histogram
      plt.subplot(313)
      (res_h, res_edges, res_p) = plt.hist(residuals)
      plt.xlabel('Residual')
      plt.ylabel('Frequency')
      
      # statistical measures
      res_min = residuals.min()
      res_max = residuals.max()
      res_mean = residuals.mean()
      res_var = residuals.var()
      res_std = residuals.std()
      print("===============================================================")
      print("Statistics for metabolite " + m)
      print("Minimum of the residuals: " + str(res_min))
      print("Maximum of the residuals: " + str(res_max))
      print("Mean of the residuals: " + str(res_mean))
      print("Variance of the residuals: " + str(res_var))
      print("Coefficient of variation: " + str(res_var / res_mean))
      # generate theoretical bins from the corresponding normal distribution
      dist = norm(loc = res_mean, scale = res_std)
      (norm_h, norm_edges) = np.histogram(
        dist.rvs(size = steps), bins = len(res_h))
      # plotting corresponding pdf
      x = np.linspace(res_min, res_max, 100)
      plt.plot(x, dist.pdf(x), 'k-', lw=2)

      # Pearson's chi-squared test
      (h_chi, p_chi) = pearsonr(res_h, norm_h)
      print("Pearson's chi-squared test - H0: residuals follow a N(0,1)")
      print("P value = " + str(p_chi))
      if p_chi <= 0.05:
        print("Reject null hypothesis: residuals do not have a random behavior.")
      else:
        print("Not possible to reject null hypothesis.")

      # Runs test
      (h_runs, p_runs) = runstest_1samp(residuals)
      print("Wald-Wolfowitz test - H0: residuals are uncorrelated")
      print("P value = " + str(p_runs))
      if p_runs <= 0.05:
        print("Reject null hypothesis: residuals show some correlation.")
      else:
        print("Not possible to reject null hypothesis.")

  plt.show()

if(__name__ == '__main__'):
  main() 
