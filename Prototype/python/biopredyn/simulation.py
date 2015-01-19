#!/usr/bin/env python
# coding=utf-8

## @package biopredyn
## $Author$
## $Date$
## $Copyright: 2014, The CoSMo Company, All Rights Reserved $
## $License: BSD 3-Clause $
## $Revision$

import copy
import libsbml
import libsedml
import libsbmlsim
import algorithm, result, statistics
import numpy as np
from cobra.io.sbml import create_cobra_model_from_sbml_doc
from COPASI import *
import libfbc

## Base representation of the execution of an algorithm, independent from the
## model or data set it has to be run with.
class Simulation:
  ## @var algorithm
  # KiSAO identifier of the algorithm to execute.
  ## @var id
  # A unique identifier for this object.
  ## @var name
  # Name of this object.
  ## @var type
  # Type of simulation.
  
  ## Constructor.
  # @param self The object pointer.
  # @param simulation A SED-ML simulation.
  def __init__(self, simulation):
    self.algorithm = algorithm.Algorithm(simulation.getAlgorithm())
    self.id = simulation.getId()
    self.name = simulation.getName()
    self.type = simulation.getElementName()
  
  ## String representation of this. Displays it as a hierarchy.
  # @param self The object pointer.
  # @return A string representing this as a hierarchy.
  def __str__(self):
    tree = "  |-" + self.type + " id=" + self.id + " name=" + self.name + "\n"
    tree += "    |-algorithm " + self.algorithm.get_kisao_id() + "\n"
    return tree
  
  ## Getter. Returns self.algorithm.
  # @param self The object pointer.
  # @return self.algorithm
  def get_algorithm(self):
    return self.algorithm
  
  ## Getter. Returns self.id.
  # @param self The object pointer.
  # @return self.id
  def get_id(self):
    return self.id
  
  ## Setter for self.id.
  # @param self The object pointer.
  # @param id New value for self.id.
  def set_id(self, id):
    self.id = id
  
  ## Getter. Returns self.name.
  # @param self The object pointer.
  def get_name(self):
    return self.name
  
  ## Setter for self.name.
  # @param self The object pointer.
  # @param name New value for self.name.
  def set_name(self, name):
    self.name = name
  
  ## Getter. Returns self.type.
  # @param self The object pointer.
  # @return self.type
  def get_type(self):
    return self.type

## Simulation-derived class for one step simulations.
class OneStep(Simulation):
  ## @var step
  # Value of the time step to be considered.

  ## Overridden constructor.
  # @param self The object pointer.
  # @param simulation A SED-ML 'one step' element.
  def __init__(self, simulation):
    Simulation.__init__(self, simulation)
    self.step = simulation.getStep()

  ## Getter. Returns self.step.
  # @param self The object pointer.
  # @return self.step
  def get_step(self):
    return self.step

  ## Run the simulation encoded in self on the input model using the input tool.
  # @param self The object pointer.
  # @param model A biopredyn.model.Model object.
  # @param tool Name of the tool to use as simulation engine (string).
  # @param res A biopredyn.result.TimeSeries object.
  # @return A biopredyn.result.TimeSeries object.
  def run(self, model, tool, res):
    # tool selection - by default copasi is chosen
    if tool is None or tool == 'copasi':
      self.run_as_copasi_one_step(model, res)
    else:
      raise NameError("Invalid tool name; only 'copasi' is available as a " +
        "simulation engine.")
    return res
  
  ## Run the simulation encoded in self as a Copasi model.
  # @param self The object pointer.
  # @param model A biopredyn.model.Model object.
  # @param res A biopredyn.result.TimeSeries object.
  # @return A biopredyn.result.TimeSeries object. 
  def run_as_copasi_one_step(self, model, res):
    data_model = CCopasiDataModel()
    data_model.importSBMLFromString(model.get_sbml_doc().toSBML())
    task = data_model.addTask(CTrajectoryTask.timeCourse)
    task.setMethodType(CCopasiMethod.deterministic)
    task.processStep(self.get_step())
    res.import_from_copasi_time_series(task.getTimeSeries(),
      model.get_species_copasi_ids())
    return res
  
  ## Setter for self.step.
  # @param self The object pointer.
  # @param step New value for self.step.
  def set_step(self, step):
    self.step = step

## Simulation-derived class for steady state simulations.
class SteadyState(Simulation):

  ## Run the simulation encoded in self on the input model using the input tool.
  # @param self The object pointer.
  # @param model A biopredyn.model.Model object.
  # @param tool Name of the tool to use as simulation engine (string).
  # @param res A biopredyn.result.Fluxes object.
  # @return A biopredyn.result.Fluxes object.
  def run(self, model, tool, res):
    # tool selection - by default cobrapy is chosen
    if tool is None or tool == 'cobrapy':
      self.run_as_cobrapy_problem(model, res)
    elif tool == 'libfbc':
      self.run_as_libfbc_problem(model, res)
    else:
      raise NameError("Invalid tool name; available names are 'cobrapy' and " +
        " 'libfbc'.")
    return res

  ## Run the simulation encoded in self as a CobraPy model.
  # @param self The object pointer.
  # @param model A biopredyn.model.Model object.
  # @param res A biopredyn.result.Fluxes object.
  # @return A biopredyn.result.Fluxes object.
  def run_as_cobrapy_problem(self, model, res):
    if res is None:
      res = result.Fluxes()
    # Case where the encoded simulation is a FBA
    if self.algorithm.get_kisao_id() == "KISAO:0000437":
      # Run a basic FBA with cobrapy
      cobra_model = create_cobra_model_from_sbml_doc(model.get_sbml_doc())
      # Optional model parameters are set
      obj = self.algorithm.get_parameter_by_name('objective_function')
      sense = self.algorithm.get_parameter_by_name('objective_sense')
      if obj is not None:
        cobra_model.change_objective([obj.get_value()])
      if sense is not None:
        cobra_model.optimize(objective_sense=sense.get_value())
      else:
        cobra_model.optimize()
    else:
      raise NameError("Invalid KiSAO identifier for a steady state " + 
        "simulation; see http://bioportal.bioontology.org/ontologies/KISAO " +
        "for more information about the KiSAO ontology.")
    res.import_from_cobrapy_fba(cobra_model.solution)
    return res

  ## Run the simulation encoded in self as a libFBC problem.
  # @param self The object pointer.
  # @param model A biopredyn.model.Model object.
  # @param res A biopredyn.result.Fluxes object.
  # @return A biopredyn.result.Fluxes object
  def run_as_libfbc_problem(self, model, res):
    if res is None:
      res = result.Fluxes()
    # Case where the encoded simulation is a FBA
    if self.algorithm.get_kisao_id() == "KISAO:0000437":
      fbc_model = libfbc.FBAProblem()
      fbc_model.initFromSBMLString(model.get_sbml_doc().toSBML())
      fbc_model.solveProblem()
    else:
      raise NameError("Invalid KiSAO identifier for a steady state " + 
        "simulation; see http://bioportal.bioontology.org/ontologies/KISAO " +
        "for more information about the KiSAO ontology.")
    res.import_from_libfbc_fba(fbc_model.getSolution())
    return res

## Simulation-derived class for uniform time course simulations.
class UniformTimeCourse(Simulation):
  ## @var initial_time
  # Time point where the simulation begins.
  ## @var number_of_points
  # Number of time points to consider between output_start_time and
  # output_end_time.
  ## @var output_end_time
  # Time point where both the simulation and the result collection end.
  ## @var output_start_time
  # Time point where the result collection starts; not necessarily the same as
  # initial_time.
  
  ## Overridden constructor.
  # @param self The object pointer.
  # @param simulation A SED-ML uniform time course element.
  def __init__(self, simulation):
    Simulation.__init__(self, simulation)
    self.initial_time = simulation.getInitialTime()
    self.number_of_points = simulation.getNumberOfPoints()
    self.output_end_time = simulation.getOutputEndTime()
    self.output_start_time = simulation.getOutputStartTime()
  
  ## Overridden string representation of this. Displays it as a hierarchy.
  # @param self The object pointer.
  # @return A string representing this as a hierarchy.
  def __str__(self):
    tree = "  |-" + self.type + " id=" + self.id + " name=" + self.name
    tree += " initialTime" + str(self.initial_time)
    tree += " numberOfPoints" + str(self.number_of_points)
    tree += " outputEndTime" + str(self.output_end_time)
    tree += " outputStartTime" + str(self.output_start_time) + "\n"
    tree += "    |-algorithm " + self.algorithm.get_kisao_id() + "\n"
    return tree
  
  ## Getter. Returns self.initial_time.
  # @param self The object pointer.
  # @return self.initial_time
  def get_initial_time(self):
    return self.initial_time
  
  ## Getter. Returns self.number_of_points.
  # @param self The object pointer.
  # @return self.number_of_points
  def get_number_of_points(self):
    return self.number_of_points
  
  ## Getter. Returns self.output_end_time.
  # @param self The object pointer.
  # @return self.output_end_time
  def get_output_end_time(self):
    return self.output_end_time
  
  ## Getter. Returns self.output_start_time.
  # @param self The object pointer.
  # @return self.output_start_time
  def get_output_start_time(self):
    return self.output_start_time

  ## Run the simulation encoded in self on the input model using the input tool,
  ## and returns its output as a biopredyn.result.TimeSeries object.
  # @param self The object pointer.
  # @param model A biopredyn.model.Model object.
  # @param tool Name of the tool to use as simulation engine (string).
  # @param res A biopredyn.result.TimeSeries object.
  # @return A biopredyn.result.TimeSeries object.
  def run(self, model, tool, res):
    # tool selection - by default libsbmlsim is chosen
    if tool is None or tool == 'libsbmlsim':
      self.run_as_libsbmlsim_time_course(model, res)
    elif tool == 'copasi':
      self.run_as_copasi_time_course(model, res)
    else:
      raise NameError("Invalid tool name; available names are 'copasi' and 'libsbmlsim'.")
    return res

  ## Run this as a COPASI time course and import its result.
  # @param self The object pointer.
  # @param model A biopredyn.model.Model object.
  # @param res A biopredyn.result.TimeSeries object where simulation results
  # will be written.
  # @param unknowns A list of N identifiers corresponding to the IDs of unknown
  # parameters in model. If not None, the simulation will be run with the
  # values listed in fitted_values for the unknown parameters. Default: None.
  # @param fitted_values A list of N values corresponding to the N unknowns.
  # @return A biopredyn.result.TimeSeries object.
  def run_as_copasi_time_course(
    self, model, res, unknowns=None, fitted_values=None):
    if res is None:
      res = result.TimeSeries()
    steps = self.get_number_of_points()
    start = self.get_initial_time()
    o_start = self.get_output_start_time()
    end = self.get_output_end_time()
    step = (end - o_start) / steps
    duration = end - start
    mod = model.get_sbml_doc()
    # Importing model to COPASI
    data_model = CCopasiDataModel()
    data_model.importSBMLFromString(mod.toSBML())
    cop_model = data_model.getModel()
    # unknown parameter assignment
    if unknowns is not None:
      for u in range(len(unknowns)):
        unknown = unknowns[u]
        for r in range(cop_model.getReactions().size()):
          reaction = cop_model.getReaction(r)
          for p in range(reaction.getParameters().size()):
            param = reaction.getParameters().getParameter(p)
            if param.getObjectName() == unknown:
              if reaction.isLocalParameter(p): # local case
                reaction.setParameterValue(unknown, fitted_values[u])
              else: # global case
                cop_model.getModelValues().getByName(unknown).setInitialValue(
                  fitted_values[u])
    task = data_model.addTask(CTrajectoryTask.timeCourse)
    pbm = task.getProblem()
    # Set the parameters
    pbm.setOutputStartTime(o_start)
    pbm.setStepSize(step)
    pbm.setDuration(duration)
    pbm.setTimeSeriesRequested(True)
    # TODO: acquire KiSAO description of the algorithm
    task.setMethodType(CCopasiMethod.deterministic)
    # Execution - initial values are used
    task.processWithOutputFlags(True, CCopasiTask.ONLY_TIME_SERIES)
    # Time series extraction
    res.import_from_copasi_time_series(task.getTimeSeries(),
      model.get_species_copasi_ids())
    return res

  ## Run this as a libSBMLSim time course and import its result.
  # @param self The object pointer.
  # @param model A biopredyn.model.Model object.
  # @param res A biopredyn.result.TimeSeries object where simulation results
  # will be written.
  # @return A biopredyn.result.TimeSeries object.
  # TODO: add option for setting parameter values before running
  def run_as_libsbmlsim_time_course(self, model, res):
    if res is None:
      res = result.TimeSeries()
    steps = self.get_number_of_points()
    start = self.get_output_start_time()
    end = self.get_output_end_time()
    step = (end - start) / steps
    mod = model.get_sbml_doc()
    # TODO: acquire KiSAO description of the algorithm
    r = libsbmlsim.simulateSBMLFromString(
        mod.toSBML(),
        end,
        step,
        1,
        0,
        libsbmlsim.MTHD_RUNGE_KUTTA,
        0)
    res.import_from_libsbmlsim(r, start)
    return res

  ## Use the parameter of the simulation to estimate the input model parameters
  ## with respect to the input data file. Uses COPASI as simulation engine.
  # @param self The object pointer.
  # @param mod A biopredyn.model.Model object.
  # @param cal_data Path to a column-aligned CSV file containing the
  # calibration data.
  # @param val_data Path to a column-aligned CSV file containing the
  # validation data.
  # @param observables A list of identifier corresponding to the IDs of the
  # observables to consider (both in model and data file).
  # @param unknowns A list of identifier corresponding to the IDs of the
  # parameters to be estimated in the input model.
  # @param min_unknown_values A list of numerical values; lower bound of the
  # parameter value ranges.
  # @param max_unknown_values A list of numerical values; upper bound of the
  # parameter value ranges.
  # @param algorithm A CCopasiMethod::SubType object describing the algorithm
  # to be used.
  # @param rm A biopredyn.resources.ResourceManager object.
  # return statistics A biopredyn.statistics.Statistics object.
  def run_as_parameter_estimation(self, mod, cal_data, val_data, observables,
    unknowns, min_unknown_values, max_unknown_values, algorithm, rm):
    data_model = CCopasiDataModel()
    data_model.importSBMLFromString(mod.get_sbml_doc().toSBML())
    # importing data
    data = result.TimeSeries()
    metabolites = data.import_from_csv_file(cal_data, rm)
    steps = len(data.get_time_steps())
    # task definition
    fit_task = data_model.addTask(CFitTask.parameterFitting)
    fit_problem = fit_task.getProblem()
    # experiment definition
    experiment_set = fit_problem.getParameter("Experiment Set")
    experiment = CExperiment(data_model)
    experiment.setFileName(cal_data)
    experiment.setSeparator(",")
    experiment.setFirstRow(1) # offset due to header
    experiment.setLastRow(steps + 1)
    experiment.setHeaderRow(1)
    experiment.setExperimentType(CCopasiTask.timeCourse)
    experiment.setNumColumns(len(metabolites))
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
            metab_object = meta.getObject(
              CCopasiObjectName("Reference=Concentration"))
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
    fit_task.setMethodType(algorithm)
    fit_task.processWithOutputFlags(True, CCopasiTask.ONLY_TIME_SERIES)
    # extracting values of the fitted parameters
    fitted_param = []
    for p in range(opt_item_group.size()):
      opt_item = opt_item_group.getParameter(p)
      fitted_param.append(opt_item.getLocalValue())
    # extracting Fisher Information Matrix from fit_problem
    fisher = fit_problem.getFisher()
    f_mat = []
    for row in range(fisher.numRows()):
      r = []
      for col in range(fisher.numCols()):
        r.append(fisher.get(row, col))
      f_mat.append(r)
    f_mat = np.mat(f_mat)
    stats = statistics.Statistics(
      val_data, data, copy.deepcopy(self), mod, fit_problem.getSolutionValue(),
      observables, unknowns, fitted_param, f_mat, rm)
    return stats
  
  ## Setter. Assign a new value to self.initial_time.
  # @param self The object pointer.
  # @param initial_time New value for self.initial_time.
  def set_initial_time(self, initial_time):
    self.initial_time = initial_time
  
  ## Setter. Assign a new value to self.number_of_points.
  # @param self The object pointer.
  # @param number_of_points New value of self.number_of_points.
  def set_number_of_points(self, number_of_points):
    self.number_of_points = number_of_points
  
  ## Setter. Assign a new value to self.output_end_time.
  # @param self The object pointer.
  # @param output_end_time New value of self.output_end_time.
  def set_output_end_time(self, output_end_time):
    self.output_end_time = output_end_time
  
  ## Setter. Assign a new value to self.output_start_time.
  # @param self The object pointer.
  # @param output_start_time New value for self.output_start_time.
  def set_output_start_time(self, output_start_time):
    self.output_start_time = output_start_time
