#!/usr/bin/env python
# coding=utf-8

from biopredyn import resources, workflow, result as res
from matplotlib import colors, pyplot as plt
import numpy as np
from scipy.stats import f
from scipy.linalg import svd
from scipy.stats import norm, pearsonr
from scikits.statsmodels.sandbox.stats.runs import runstest_1samp

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

sim = wf.get_simulations()[0]
model_result = sim.run_as_parameter_estimation(
  wf.get_models()[0], calibration_file, validation_file,
  observables, unknowns, min_unknown_values, max_unknown_values, rm)

# funny science
plt.xkcd()

# plotting model and data results
plt.figure("Fitted model: " + wf.get_models()[0].get_id())
for s in model_result.get_fitted_result().get_result().keys():
  if not str.lower(s).__contains__("time"):
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

val_data = res.Result()
metabolites = val_data.import_from_csv_file(
  validation_file, rm, separator=',', alignment='column')

# Analysis of the residuals
for m in metabolites:
  if not str.lower(m).__contains__("time") and m in observables:
    # plotting residuals vs fitted values
    plt.figure("Analysis of the residuals - " + m)
    plt.subplot(311)
    prediction = model_result.get_fitted_result().get_quantities_per_species(m)
    prediction = np.array(prediction)
    residuals = model_result.get_residuals(m)
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
      dist.rvs(size = len(val_time_points)), bins = len(res_h))
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

