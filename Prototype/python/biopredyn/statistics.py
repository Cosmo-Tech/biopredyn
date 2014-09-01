#!/usr/bin/env python
# coding=utf-8

## @package biopredyn
## $Author$
## $Date$
## $Copyright: 2014, The CoSMo Company, All Rights Reserved $
## $License: BSD 3-Clause $
## $Revision$

## Base class for processing / analyzing / displaying the statistics resulting
## from a successful parameter estimation.
class Statistics:
  ## @var validation_data
  # Address of a column-aligned CSV or NuML file.
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
  def __init__(
    self, val_data, fitted_res, observables, unknowns, fitted_values, fim):
    print('TODO') # TODO
