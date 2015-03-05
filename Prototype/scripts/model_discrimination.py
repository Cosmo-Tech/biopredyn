#!/usr/bin/env python
# coding=utf-8

from biopredyn import resources, workflow, result as res
from matplotlib import pyplot as plt
import numpy as np
from COPASI import CCopasiMethod

# required inputs - first model
simulation_file = "generate_data.xml"
calibration_file = "calibration_data.txt"
validation_file = "validation_data.txt"
observables = ["sp_C"] # names of the observables
unknowns = ["k1", "k2", "k3"] # names of the parameters to be estimated
min_unknown_values = [0.0, 0.0, 0.0] # lower bound of the parameter value ranges
max_unknown_values = [10.0, 10.0, 10.0] # upper bound of the parameter value ranges

# required inputs - second model
simulation_file_4 = "simulation_4.xml"
unknowns_4 = ["k1", "k2", "k3", "k4"] # names of the parameters to be estimated
min_unknown_values_4 = [0.0, 0.0, 0.0, 0.0] # lower bound of the parameter value ranges
max_unknown_values_4 = [10.0, 10.0, 10.0, 10.0] # upper bound of the parameter value ranges

algo = CCopasiMethod.LevenbergMarquardt # algorithm to be used by COPASI
rm = resources.ResourceManager()

# first model
wf = workflow.WorkFlow(rm, source=simulation_file)
sim = wf.get_simulations()[0]

res = sim.run_as_parameter_estimation(
  wf.get_models()[0], calibration_file, validation_file,
  observables, unknowns, min_unknown_values, max_unknown_values, algo, rm)

print("====================================================================")
print("Model 3-parameters")
for p in range(len(res.get_unknowns())):
  print(res.get_unknowns()[p] + ": " + str(res.get_fitted_values()[p]))
print("AIC: " + str(res.get_aic()))
print("BIC: " + str(res.get_bic()))
# plotting model and data results
plt.figure("Fitted model: " + wf.get_models()[0].get_id() +
  " - 3 parameters")
for s in res.get_fitted_result().get_result().keys():
  if not str.lower(s).__contains__("time"):
    results = res.get_fitted_result().get_quantities_per_species(s)
    plt.plot(res.get_fitted_result().get_time_steps(), results, label=s)
    # plot data only if it is available
    if s in observables:
      dat = res.get_validation_data().get_species_as_mean_std(s)
      data_label = str(s) + "_experimental"
      plt.errorbar(res.get_validation_data().get_time_steps(),
        dat[:,0], yerr=dat[:,1], ls='None', marker='_', label=data_label)
    plt.legend()

# second model
wf_4 = workflow.WorkFlow(rm, source=simulation_file_4)
sim_4 = wf.get_simulations()[0]

res_4 = sim.run_as_parameter_estimation(
  wf_4.get_models()[0], calibration_file, validation_file, observables,
  unknowns_4, min_unknown_values_4, max_unknown_values_4, algo, rm)

print("====================================================================")
print("Model 4-parameters")
for p in range(len(res_4.get_unknowns())):
  print(res_4.get_unknowns()[p] + ": " + str(res_4.get_fitted_values()[p]))
print("AIC: " + str(res_4.get_aic()))
print("BIC: " + str(res_4.get_bic()))
# plotting model and data results
plt.figure("Fitted model: " + wf_4.get_models()[0].get_id() +
  " - 4 parameters")
for s in res_4.get_fitted_result().get_result().keys():
  if not str.lower(s).__contains__("time"):
    results = res_4.get_fitted_result().get_quantities_per_species(s)
    plt.plot(res_4.get_fitted_result().get_time_steps(), results, label=s)
    # plot data only if it is available
    if s in observables:
      dat = res_4.get_validation_data().get_species_as_mean_std(s)
      data_label = str(s) + "_experimental"
      plt.errorbar(res_4.get_validation_data().get_time_steps(),
        dat[:,0], yerr=dat[:,1], ls='None', marker='_', label=data_label)
    plt.legend()

plt.show()
