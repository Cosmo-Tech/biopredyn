#!/usr/bin/env python
# coding=utf-8

from biopredyn import resources, workflow, result as res
from matplotlib import colors, pyplot as plt
import numpy as np
from scipy.stats import f
from scipy.linalg import svd

# required inputs
simulation_file = "generate_data.xml"
calibration_file = "calibration_data.txt"
validation_file = "validation_data.txt"
observables = ["sp_C"] # names of the observables
unknowns = ["k1", "k2", "k3"] # names of the parameters to be estimated
min_unknown_values = [0.0, 0.0, 0.0] # lower bound of the parameter value ranges
max_unknown_values = [10.0, 10.0, 10.0] # upper bound of the parameter value ranges

rm = resources.ResourceManager()
wf = workflow.WorkFlow(simulation_file, rm)

sim = wf.get_simulation_by_id('simulation_1')
model_result = sim.run_as_parameter_estimation(
  wf.get_models()[0], calibration_file, validation_file,
  observables, unknowns, min_unknown_values, max_unknown_values, rm)

plt.xkcd()

# plotting model and data results
for s in model_result.get_fitted_result().get_result().keys():
  if not str.lower(s).__contains__("time"):
    plt.figure(s)
    results = model_result.get_fitted_result().get_quantities_per_species(s)
    plt.plot(model_result.get_fitted_result().get_time_steps(),
      results, label=s)
    # plot data only if it is available
    if s in observables:
      dat = model_result.get_validation_data().get_quantities_per_species(s)
      data_label = str(s) + "_experimental"
      plt.plot(model_result.get_validation_data().get_time_steps(),
        dat, '+', label=data_label)
    plt.legend()

print("====================================================================")
print("Fisher Information Matrix")
print(model_result.get_fisher_information_matrix())
print("====================================================================")
print("Covariance matrix")
print(model_result.get_covariance_matrix())
print("====================================================================")
print("Correlation matrix")
print(model_result.get_correlation_matrix())

scale = colors.Normalize(vmin=-1, vmax=1)
cor_plot = plt.matshow(model_result.get_correlation_matrix(),
  fignum="Correlation matrix", norm=scale)
plt.colorbar(cor_plot)

print("====================================================================")
print("Objective function value: " + str(model_result.get_objective_value()))

print("====================================================================")
print("Delta dependent confidence intervals (alpha = 0.05)")
print(model_result.get_dependent_confidence_intervals())
print("====================================================================")
print("Delta independent confidence intervals (alpha = 0.05)")
print(model_result.get_independent_confidence_intervals())
print("====================================================================")
print("Eigenvectors")
print(model_result.get_fim_eigenvectors())
print("====================================================================")
print("Singular values")
print(model_result.get_fim_singular_values())

plt.show()
