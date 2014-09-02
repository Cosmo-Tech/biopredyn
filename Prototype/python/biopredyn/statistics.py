#!/usr/bin/env python
# coding=utf-8

## @package biopredyn
## $Author$
## $Date$
## $Copyright: 2014, The CoSMo Company, All Rights Reserved $
## $License: BSD 3-Clause $
## $Revision$

import result

## Base class for processing / analyzing / displaying the statistics resulting
## from a successful parameter estimation.
class Statistics:
  ## @var validation_data
  # A biopredyn.result.Result object.
  ## @var fitted_result
  # A biopredyn.result.Result object.
  ## @var observables
  # List of observable quantities in self.validation_data.
  ## @var unknowns
  # List of unknown parameters
  ## @var fitted_values
  # List of fitted values for self.unknowns.
  ## @var fisher_information_matrix
  # A numpy.mat object.

  ## Constructor.
  # @param self The object pointer.
  # @param val_data Path to a column-aligned CSV file containing the
  # validation data.
  # fitted_res A biopredyn.result.Result object produced by a fitted model
  # simulation run.
  # @param observables A list of identifier corresponding to the IDs of the
  # observables to consider (both in model and data file).
  # @param unknowns A dictionary of N items where IDs of the
  # parameters to be estimated in the input model.
  # @param fitted_values A list of N values corresponding to the fitted values
  # of the N model parameters of the input 'unknowns' list.
  # @param fim An N*N numpy.mat object produced by a successful parameter
  # estimation.
  # @param rm A biopredyn.resources.ResourceManager object.
  def __init__(
    self, val_data, fitted_res, observables, unknowns, fitted_values, fim, rm):
    self.validation_data = result.Result()
    self.validation_data.import_from_csv_file(
      val_data, rm, separator=',', alignment='column')
    self.fitted_result = fitted_res
    self.observables = observables
    self.unknowns = unknowns
    self.fitted_values = fitted_values
    self.fisher_information_matrix = fim

  ## Getter. Returns self.fisher_information_matrix.
  # @param self The object pointer.
  # @return self.fisher_information_matrix
  def get_fisher_information_matrix(self):
    return self.fisher_information_matrix

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

  ## Getter. Returns self.observables.
  # @param self The object pointer.
  # @return self.observables
  def get_observables(self):
    return self.observables

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
