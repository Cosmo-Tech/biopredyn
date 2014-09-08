#!/usr/bin/env python
# coding=utf-8

from biopredyn import resources, workflow, result as res
from matplotlib import pyplot as plt
import numpy as np

# required inputs
simulation_file = "generate_data.xml"
calibration_file = "calibration_data.txt"
validation_file = "validation_data.txt"
observables = ["sp_C"] # names of the observables
unknowns = ["k1", "k2", "k3"] # names of the parameters to be estimated
min_unknown_values = [0.0, 0.0, 0.0] # lower bound of the parameter value ranges
max_unknown_values = [10.0, 10.0, 10.0] # upper bound of the parameter value ranges
nb_models = 3 # number of models to compare

rm = resources.ResourceManager()
wf = workflow.WorkFlow(simulation_file, rm)

# funny science
plt.xkcd()

val_data = res.Result()
metabolites = val_data.import_from_csv_file(
  validation_file, rm, separator=',', alignment='column')
sim = wf.get_simulations()[0]

# run a parameter estimation for each model
model_results = []
for i in range(nb_models):
  model_results.append(sim.run_as_parameter_estimation(
    wf.get_models()[0], calibration_file, validation_file,
    observables, unknowns, min_unknown_values, max_unknown_values, rm))

# compare each solution
for i in range(len(model_results)):
  m = model_results[i]
  print("====================================================================")
  print("Model " + str(i))
  for p in range(len(m.get_unknowns())):
    print(m.get_unknowns()[p] + ": " + str(m.get_fitted_values()[p]))
  for meta in metabolites:
    if not str.lower(meta).__contains__("time") and meta in observables:
      print("Metabolite " + meta + ":")
      print("AIC: " + str(m.get_aic(meta)))
      print("BIC: " + str(m.get_bic(meta)))
  # plotting model and data results
  plt.figure("Fitted model: " + wf.get_models()[0].get_id() +
    " - Parameter set " + str(i))
  for s in m.get_fitted_result().get_result().keys():
    if not str.lower(s).__contains__("time"):
      results = m.get_fitted_result().get_quantities_per_species(s)
      plt.plot(m.get_fitted_result().get_time_steps(), results, label=s)
      # plot data only if it is available
      if s in observables:
        dat = m.get_validation_data().get_quantities_per_species(s)
        data_label = str(s) + "_experimental"
        plt.plot(m.get_validation_data().get_time_steps(),
          dat, '+', label=data_label)
      plt.legend()

plt.show()
