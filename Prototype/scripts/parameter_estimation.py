#!/usr/bin/env python
# coding=utf-8

from biopredyn import resources, workflow, result as res
from matplotlib import colors, pyplot as plt
import numpy as np
from scipy.stats import f
from scipy.linalg import svd
from scipy.stats import norm
from COPASI import CCopasiMethod

# required inputs
simulation_file = "generate_data.xml"
calibration_file = "calibration_data.txt"
validation_file = "validation_data.txt"
observables = ["sp_C"] # names of the observables
unknowns = ["k1", "k2", "k3"] # names of the parameters to be estimated
min_unknown_values = [0.0, 0.0, 0.0] # lower bound of the parameter value ranges
max_unknown_values = [10.0, 10.0, 10.0] # upper bound of the parameter value ranges
algo = CCopasiMethod.LevenbergMarquardt

rm = resources.ResourceManager()
wf = workflow.WorkFlow(simulation_file, rm)

sim = wf.get_simulations()[0]
model_result = sim.run_as_parameter_estimation(
  wf.get_models()[0], calibration_file, validation_file,
  observables, unknowns, min_unknown_values, max_unknown_values, algo, rm)

# funny science
#plt.xkcd()

# plotting model and data results
plt.figure("Fitted model: " + wf.get_models()[0].get_id())
for s in model_result.get_fitted_result().get_result().keys():
  if not str.lower(s).__contains__("time"):
    results = model_result.get_fitted_result().get_quantities_per_species(s)
    plt.plot(model_result.get_fitted_result().get_time_steps(),
      results, label=s)
    # plot data only if it is available
    if s in observables:
      dat = model_result.get_validation_data().get_species_as_mean_std(s)
      data_label = str(s) + "_experimental"
      plt.errorbar(model_result.get_validation_data().get_time_steps(),
        dat[:,0], yerr=dat[:,1], ls='None', marker='+', label=data_label)
    plt.legend(loc='center right')

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
plt.xticks(np.arange(len(unknowns)), unknowns)
plt.yticks(np.arange(len(unknowns)), unknowns)
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

val_data = res.TimeSeries()
val_data.import_from_csv_file(validation_file, rm)
residuals = model_result.get_residuals()
   
# statistical measures on residuals
res_min = residuals.min()
res_max = residuals.max()
res_mean = residuals.mean()
res_var = residuals.var()
res_std = residuals.std()
print("===============================================================")
print("Minimum of the residuals: " + str(res_min))
print("Maximum of the residuals: " + str(res_max))
print("Mean of the residuals: " + str(res_mean))
print("Variance of the residuals: " + str(res_var))
print("Coefficient of variation: " +
  str(model_result.get_residuals_coeff_of_variation()))

# plotting residuals versus time-ordered data
plt.figure("Analysis of the residuals")
plt.subplot(211)
val_time_points = np.array(val_data.get_time_steps())
plt.plot(val_time_points, residuals, 'r+')
plt.legend()
# add y=0 line for reference and axis labels
plt.axhline(0, color='grey')
plt.xlabel('Observation order')
plt.ylabel('Residual')

# plotting residuals as a histogram
plt.subplot(212)
(res_h, res_edges, res_p) = plt.hist(residuals)
plt.xlabel('Residual')
plt.ylabel('Frequency')
# plot associated pdf
dist = norm(loc = res_mean, scale = res_std)
x = np.linspace(res_min, res_max, 100)
plt.plot(x, dist.pdf(x), 'k-', lw=2)

# Pearson's chi-squared test
chi_test = model_result.check_residuals_randomness()
print("Pearson's chi-squared test - H0: residuals follow a N(0,1)")
print("P value = " + str(chi_test[0]))
if chi_test[1]:
  print("Not possible to reject null hypothesis.")
else:
  print("Reject null hypothesis: residuals do not have a random behavior.")

# Runs test
runs_test = model_result.check_residuals_correlation()
print("Wald-Wolfowitz test - H0: residuals are uncorrelated")
print("P value = " + str(runs_test[0]))
if runs_test[1]:
  print("Not possible to reject null hypothesis.")
else:
  print("Reject null hypothesis: residuals show some correlation.")

plt.show()
