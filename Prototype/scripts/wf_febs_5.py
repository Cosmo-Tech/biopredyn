#!/usr/bin/env python
# coding=utf-8

import libsbml
from COPASI import *
import sys
from random import random
from biopredyn import result as res
from biopredyn import resources
from matplotlib import colors, pyplot as plt
import numpy as np
from scipy.stats import f
from scipy.linalg import svd

def main():
  # required inputs
  model_file = "FEBS_antimony.xml"
  fitted_model = "FEBS_antimony_fitted.xml"
  data_file = "calibration_data.txt"
  start = 0.0
  end = 20.0
  observables = ["sp_C"] # names of the observables
  unknowns = ["k1", "k2", "k3"] # names of the parameters to be estimated
  min_unknown_values = [0.0, 0.0, 0.0] # lower bound of the parameter value ranges
  max_unknown_values = [10.0, 10.0, 10.0] # upper bound of the parameter value ranges
  alpha = 0.05

  # create a datamodel
  data_model = CCopasiRootContainer.addDatamodel()
  # first we load a simple model
  try:
    # load the model 
    data_model.importSBML(model_file)
  except:
    sys.stderr.write("Error while importing the model.\n")
    return 1

  # importing data as a res.Result object column-aligned
  rm = resources.ResourceManager()
  data = res.Result()
  metabolites = data.import_from_csv_file(
    data_file, rm, separator=',', alignment='column')
  steps = len(data.get_time_steps()) - 1 # 100 intervals mean 101 time steps

  # task definition
  fit_task = data_model.addTask(CFitTask.parameterFitting)
  fit_problem = fit_task.getProblem()
 
  # experiment definition
  experiment_set = fit_problem.getParameter("Experiment Set")
  experiment = CExperiment(data_model)
  experiment.setFileName(data_file)
  experiment.setSeparator(",")
  experiment.setFirstRow(1)
  experiment.setLastRow(steps + 1)
  experiment.setHeaderRow(1)
  experiment.setExperimentType(CCopasiTask.timeCourse)
  experiment.setNumColumns(len(metabolites))

  # defining the object map, where time series are linked with model species
  object_map = experiment.getObjectMap()
  object_map.setNumCols(len(metabolites))
  model = data_model.getModel()

  # assigning roles and names with respect to the content of the data file
  index = 0
  for name in metabolites:
    if str.lower(name).__contains__("time"):
      # case where the current 'metabolite' is time
      object_map.setRole(index, CExperiment.time)
      time_reference = model.getObject(CCopasiObjectName("Reference=Time"))
      object_map.setObjectCN(index, time_reference.getCN().getString())
    elif name in observables:
      # case where the current metabolite is an observable
      for m in range(model.getMetabolites().size()):
        meta = model.getMetabolites().get(m)
        if (meta.getSBMLId() == name):
          metab_object = meta.getObject(CCopasiObjectName("Reference=Concentration"))
          object_map.setRole(index, CExperiment.dependent)
          object_map.setObjectCN(index, metab_object.getCN().getString())
    index += 1
   
  experiment_set.addExperiment(experiment)
  experiment = experiment_set.getExperiment(0)

  # definition of the fitted object - i.e. the parameters listed in unknowns
  opt_item_group = fit_problem.getParameter("OptimizationItemList")
  for u in range(len(unknowns)):
    unknown = unknowns[u]
    for r in range(model.getReactions().size()):
      reaction = model.getReaction(r)
      for p in range(reaction.getParameters().size()):
        param = reaction.getParameters().getParameter(p)
        if param.getObjectName() == unknown:
          if reaction.isLocalParameter(p): # case of a local parameter
            fit_item = CFitItem(data_model)
            fit_item.setObjectCN(
              param.getObject(CCopasiObjectName("Reference=Value")).getCN())
            fit_item.setStartValue(param.getValue())
            fit_item.setLowerBound(
              CCopasiObjectName(str(min_unknown_values[u])))
            fit_item.setUpperBound(
              CCopasiObjectName(str(max_unknown_values[u])))
            opt_item_group.addParameter(fit_item)
          else: # case of a global parameter
            parameter = model.getModelValues().getByName(unknown)
            exists = False
            for fit in range(opt_item_group.size()):
              if opt_item_group.getParameter(fit).getCN() == parameter.getCN():
                exists = True # parameter already exists as a CFitItem
                break
            if not exists:
              fit_item = CFitItem(data_model)
              fit_item.setObjectCN(parameter.getObject(CCopasiObjectName(
                "Reference=InitialValue")).getCN())
              fit_item.setStartValue(param.getValue())
              fit_item.setLowerBound(
                CCopasiObjectName(str(min_unknown_values[u])))
              fit_item.setUpperBound(
                CCopasiObjectName(str(max_unknown_values[u])))
              opt_item_group.addParameter(fit_item)
   
  try:
    print "Parameter estimation in progress."
    fit_task.processWithOutputFlags(True, CCopasiTask.ONLY_TIME_SERIES)
  except:
    sys.stderr.write(" Error. Parameter fitting failed.\n")
    return 1

  # produce results i.e. the vector of optimal values for the unknowns
  results = []
  for p in range(opt_item_group.size()):
    opt_item = opt_item_group.getParameter(p)
    results.append(opt_item.getLocalValue())
    print("Value for " + unknowns[p] + ": " + str(opt_item.getLocalValue()))

  # plotting model results vs artificial data
  # first we run a simulation with the computed values of the parameters
  trajectory_task = data_model.getTask("Time-Course")

  # run a deterministic time course
  trajectory_task.setMethodType(CCopasiMethod.deterministic)
  trajectory_task.getProblem().setModel(data_model.getModel())
  problem = trajectory_task.getProblem()

  # parameter assignment depends on the lcoation of the unknowns
  for u in range(len(unknowns)):
    unknown = unknowns[u]
    for r in range(model.getReactions().size()):
      reaction = model.getReaction(r)
      for p in range(reaction.getParameters().size()):
        param = reaction.getParameters().getParameter(p)
        if param.getObjectName() == unknown:
          if reaction.isLocalParameter(p): # local case
            reaction.setParameterValue(unknown, results[u])
          else: # global case
            model.getModelValues().getByName(unknown).setInitialValue(
              results[u])

  data_model.exportSBML(fitted_model, True)

  # input parameters are used for the simulation
  sim_time = np.linspace(start, end, num=101)
  problem.setStepNumber(100)
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
  names = model_result.import_from_copasi_time_series(
    trajectory_task.getTimeSeries())
  data_time = np.array(data.get_time_steps())

  plt.xkcd()

  # plotting model and data results
  for s in range(len(metabolites)):
    if not str.lower(metabolites[s]).__contains__("time"):
      plt.figure(s)
      results = model_result.get_quantities_per_species(names[s])
      plt.plot(sim_time, results, label=str(names[s]))
      # plot data only if it is available
      if metabolites[s] in observables:
        dat = data.get_quantities_per_species(metabolites[s])
        data_label = str(metabolites[s]) + "_experimental"
        plt.plot(data_time, dat, '+', label=data_label)
      plt.legend()

  # a posteriori identifiability analysis - included in the parameter
  # estimation script, as the required information is generated at this point
  fisher = fit_problem.getFisher()
  f_mat = []
  for row in range(fisher.numRows()):
    r = []
    for col in range(fisher.numCols()):
      r.append(fisher.get(row, col))
    f_mat.append(r)

  f_mat = np.mat(f_mat)
  print("====================================================================")
  print("Fisher Information Matrix")
  print(f_mat)
  cov_mat = f_mat.I
  print("====================================================================")
  print("Covariance matrix")
  print(cov_mat)
  cor_mat = np.zeros(cov_mat.shape)
  for r in range(cor_mat.shape[0]):
    for c in range(cor_mat.shape[1]):
      cor_mat[c, r] = cov_mat[c, r] / np.sqrt(cov_mat[r, r] * cov_mat[c, c])
  print("====================================================================")
  print("Correlation matrix")
  print(cor_mat)

  scale = colors.Normalize(vmin=-1, vmax=1)
  cor_plot = plt.matshow(cor_mat, fignum="Correlation matrix", norm=scale)
  plt.colorbar(cor_plot)

  obj_value = fit_problem.getSolutionValue()
  print("====================================================================")
  print("Objective function value: " + str(obj_value))

  # confidence intervals
  f_alpha = f.ppf(1-alpha, len(unknowns), steps)
  c_alpha = len(unknowns) * obj_value * f_alpha / ( steps - len(unknowns) )
  delta_dep = np.sqrt( c_alpha / f_mat.diagonal() )
  print("====================================================================")
  print("Delta dependent confidence intervals")
  print(delta_dep)
  delta_ind = np.sqrt( c_alpha * cov_mat.diagonal() )
  print("====================================================================")
  print("Delta independent confidence intervals")
  print(delta_ind)
  eigen = svd(f_mat)
  print("====================================================================")
  print("Eigenvectors")
  print(eigen[0])
  print("====================================================================")
  print("Singular values")
  print(np.sqrt(np.diagflat(eigen[1])))

  plt.show()

if(__name__ == '__main__'):
   main() 
