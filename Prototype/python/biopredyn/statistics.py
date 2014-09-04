#!/usr/bin/env python
# coding=utf-8

## @package biopredyn
## $Author$
## $Date$
## $Copyright: 2014, The CoSMo Company, All Rights Reserved $
## $License: BSD 3-Clause $
## $Revision$

import result
import numpy as np
from scipy.linalg import svd
from scipy.stats import f, norm, pearsonr
from scikits.statsmodels.sandbox.stats.runs import runstest_1samp

## Base class for processing / analyzing / displaying the statistics resulting
## from a successful parameter estimation.
class Statistics:
  ## @var validation_data
  # A biopredyn.result.Result object containing validation data as time series.
  ## @var fitted_result
  # A biopredyn.result.Result object containing the time series generated by a
  # simulation run of the fitted model.
  ## @var objective_value
  # A float numerical value representing the value of the objective function
  # after a parameter estimation run.
  ## @var observables
  # List of observable quantities in self.validation_data.
  ## @var unknowns
  # List of string identifiers of the estimated parameters in the fitted model.
  ## @var fitted_values
  # List of fitted values for self.unknowns.
  ## @var fisher_information_matrix
  # A numpy.mat object containing the Fisher information for the parameters
  # listed in self.unknowns.

  ## Constructor.
  # @param self The object pointer.
  # @param val_data Path to a column-aligned CSV file containing the
  # validation data.
  # @param simulation A biopredyn.simulation.UniformTimeCourse object.
  # @param model A biopredyn.model.Model object; to be used with the input
  # simulation in order to produce self.fitted_result.
  # @param obj_value Value of the objective function at the end of a parameter
  # estimation run.
  # @param observables A list of identifier corresponding to the IDs of the
  # observables to consider (both in model and data file).
  # @param unknowns A dictionary of N items where IDs of the
  # parameters to be estimated in the input model.
  # @param fitted_values A list of N values corresponding to the fitted values
  # of the N model parameters of the input 'unknowns' list.
  # @param fim An N*N numpy.mat object produced by a successful parameter
  # estimation.
  # @param rm A biopredyn.resources.ResourceManager object.
  def __init__(self, val_data, simulation, model, obj_value, observables,
    unknowns, fitted_values, fim, rm):
    self.validation_data = result.Result()
    self.validation_data.import_from_csv_file(
      val_data, rm, separator=',', alignment='column')
    # running simulation with modified parameters
    simulation.set_number_of_points(
      len(self.validation_data.get_time_steps()) - 1)
    simulation.set_output_start_time(self.validation_data.get_time_steps()[0])
    simulation.set_output_end_time(self.validation_data.get_time_steps()[-1])
    res = result.Result()
    simulation.run_as_copasi_time_course(
      model, res, unknowns=unknowns, fitted_values=fitted_values)
    self.fitted_result = res
    self.objective_value = obj_value
    self.observables = observables
    self.unknowns = unknowns
    self.fitted_values = fitted_values
    self.fisher_information_matrix = fim

  ## Tests the correlation of self.residuals using a Wald-Wolfowitz statistical
  ## test. Null hypothesis: residuals are uncorrelated.
  # @param self The object pointer.
  # @param species Identifier of the species to be considered in
  # self.validation_data and self.fitted_result.
  # @param alpha Significance level for the Wald-Wolfowitz test
  # (default: 0.05).
  # @return A tuple containing the test's P-value and a bolean value: True if
  # the null hypothesis cannot be rejected (i.e. residuals are uncorrelated),
  # False otherwise (residuals show some correlation).
  def check_residuals_correlation(self, species, alpha=0.05):
    (h_runs, p_runs) = runstest_1samp(self.get_residuals(species))
    if p_runs <= alpha:
      return (p_runs, False)
    else:
      return (p_runs, True)

  ## Tests the randomness of self.residuals using a Pearson's chi-squared
  ## statistical test. Null hypothesis: distribution of the residuals follows
  ## a normal law.
  # @param self The object pointer.
  # @param species Identifier of the species to be considered in
  # self.validation_data and self.fitted_result.
  # @param alpha Significance level for the Pearson's chi squared test
  # (default: 0.05).
  # @param bins Number of bins in the compared histograms (default: 10).
  # @return A tuple containing the test's P-value and a boolean value: True if
  # the null hypothesis cannot be rejected (residuals have a random behavior),
  # False otherwise (residuals do not have a random behavior).
  def check_residuals_randomness(self, species, alpha=0.05, bins=10):
    # create reference histogram from a normal distribution
    residuals = self.get_residuals(species)
    dist = norm(loc = residuals.mean(), scale = residuals.std())
    # create histograms for normal distribution and residuals
    (norm_h, norm_edges) = np.histogram(dist.rvs(
      size = len(self.validation_data.get_time_steps())), bins = bins)
    (res_h, res_edges) = np.histogram(residuals, bins = bins)
    # test
    (h_chi, p_chi) = pearsonr(res_h, norm_h)
    if p_chi <= alpha:
      return (p_chi, False)
    else:
      return (p_chi, True)

  ## Returns the covariance matrix derived from self.fisher_information_matrix.
  # @param self The object pointer.
  # @return A numpy.mat object.
  def get_covariance_matrix(self):
    return self.fisher_information_matrix.I

  ## Returns the correlation matrix derived from
  ## self.fisher_information_matrix.
  # @param self The object pointer.
  # @return cor_mat A numpy.mat object.
  def get_correlation_matrix(self):
    cov_mat = self.get_covariance_matrix()
    cor_mat = np.zeros(cov_mat.shape)
    for r in range(cor_mat.shape[0]):
      for c in range(cor_mat.shape[1]):
        cor_mat[c, r] = cov_mat[c, r] / np.sqrt(cov_mat[r, r] * cov_mat[c, c])
    return cor_mat

  ## Returns the vector of dependent confidence intervals; its length equals
  ## the length of self.unknowns.
  # @param self The object pointer.
  # @param alpha Probability of failure i.e. probability that the real value of
  # the estimated parameter is outside the confidence region. Default: 0.05
  # @return A vector containing the dependent confidence intervals of each
  # estimated parameter.
  def get_dependent_confidence_intervals(self, alpha=0.05):
    m = len(self.unknowns)
    n = len(self.validation_data.get_time_steps())
    f_alpha = f.ppf(1-alpha, m, n)
    c_alpha = n * self.objective_value * f_alpha / (n - m)
    return np.sqrt(c_alpha / self.fisher_information_matrix.diagonal())

  ## Getter. Returns self.fisher_information_matrix.
  # @param self The object pointer.
  # @return self.fisher_information_matrix
  def get_fisher_information_matrix(self):
    return self.fisher_information_matrix

  ## Returns the eigenvectors (as a matrix) of self.fisher_information_matrix.
  # @param self The object pointer.
  # @return A numpy.mat object.
  def get_fim_eigenvectors(self):
    sv_dec = svd(self.fisher_information_matrix)
    return sv_dec[0]

  ## Returns the singular values (as a vector) of
  ## self.fisher_information_matrix.
  # @param self The object pointer.
  # @return A numpy.mat object.
  def get_fim_singular_values(self):
    sv_dec = svd(self.fisher_information_matrix)
    return np.sqrt(np.diagflat(sv_dec[1]))

  ## Getter. Returns self.fitted_result.
  # @param self The object pointer.
  # @return self.fitted_result
  def get_fitted_result(self):
    return self.fitted_result

  ## Getter. Returns self.fitted_values.
  # @param self The object pointer.
  # @return self.fitted_values
  def get_fitted_values(self):
    return self.fitted_values

  ## Returns the vector of independent confidence intervals; its length equals
  ## the length of self.unknowns.
  # @param self The object pointer.
  # @param alpha Probability of failure i.e. probability that the real value of
  # the estimated parameter is outside the confidence region. Default: 0.05
  # @return A vector containing the independent confidence intervals of each
  # estimated parameter.
  def get_independent_confidence_intervals(self, alpha=0.05):
    m = len(self.unknowns)
    n = len(self.validation_data.get_time_steps())
    f_alpha = f.ppf(1-alpha, m, n)
    c_alpha = n * self.objective_value * f_alpha / (n - m)
    return np.sqrt(c_alpha / self.get_covariance_matrix().diagonal())

  ## Getter. Returns self.objective_value.
  # @param self The object pointer.
  # @return self.objective_value
  def get_objective_value(self):
    return self.objective_value

  ## Getter. Returns self.observables.
  # @param self The object pointer.
  # @return self.observables
  def get_observables(self):
    return self.observables

  ## Returns the residuals of the input species; if the input species is not in
  ## self.observables, an exception is raised.
  # @param self The object pointer.
  # @param species Identifier of the species to be considered.
  # @return residuals The residuals for the input species.
  def get_residuals(self, species):
    try:
      prediction = self.fitted_result.get_quantities_per_species(species)
      prediction = np.array(prediction)
      experiment = np.array(
        self.validation_data.get_quantities_per_species(species))
      residuals = experiment - prediction
      return residuals
    except KeyError as k:
      print("Error: " + species + " is not an observable.")

  ## Returns the coefficient of variation of the residuals for the input
  ## species. The coefficient of variation is defined as the ratio between
  ## the experiment variance and mean.
  def get_residuals_coeff_of_variation(self, species):
    residuals = self.get_residuals(species)
    return residuals.var() / residuals.mean()

  ## Getter. Returns self.unknowns.
  # @param self The object pointer.
  # @return self.unknowns
  def get_unknowns(self):
    return self.unknowns

  ## Getter. Returns self.validation_data.
  # @param self The object pointer.
  # @return self.validation_data
  def get_validation_data(self):
    return self.validation_data

  ## Setter for self.fisher_information_matrix.
  # @param self The object pointer.
  # @param fim New value for self.fisher_information_matrix.
  def set_fisher_information_matrix(self, fim):
    self.fisher_information_matrix = fim

  ## Setter for self.fitted_result.
  # @param self The object pointer.
  # @param fitted_res New value for self.fitted_result.
  def set_fitted_result(self, fitted_res):
    self.fitted_result = fitted_res

  ## Setter for self.fitted_values.
  # @param self The object pointer.
  # @param fitted_values New value for self.fitted_values.
  def set_fitted_values(self, fitted_values):
    self.fitted_values = fitted_values

  ## Setter for self.objective_value.
  # @param self The object pointer.
  # @param obj_value New value for self.objective_value.
  def set_objective_value(self, obj_value):
    self.objective_value = obj_value

  ## Setter for self.observables.
  # @param self The object pointer.
  # @param observables New value for self.observables.
  def set_observables(self, observables):
    self.observables = observables

  ## Setter for self.unknowns.
  # @param self The object pointer.
  # @param unknowns New value for self.unknowns.
  def set_unknowns(self, unknowns):
    self.unknowns = unknowns

  ## Setter for self.validation_data.
  # @param self The object pointer.
  # @param val_data New value for self.validation_data.
  def set_validation_data(self, val_data):
    self.validation_data = val_data
