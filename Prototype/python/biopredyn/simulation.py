#!/usr/bin/env python
# coding=utf-8

## @package biopredyn
## $Author$
## $Date$
## $Copyright: 2014, The CoSMo Company, All Rights Reserved $
## $License: BSD 3-Clause $
## $Revision$

import libsbml
import libsedml
import libsbmlsim
import algorithm, result
from cobra.io.sbml import create_cobra_model_from_sbml_doc
#TODO: from COPASI import CCopasiDataModel, CCopasiTask, CTrajectoryTask, CCopasiMethod

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
  def run(self, model, tool):
    # TODO
    return 0
  
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
  def run(self, model, tool):
    # Case where the encoded simulation is a FBA - TODO other SteadyState cases
    if self.algorithm.get_kisao_id() == "KISAO:0000437":
      # Run a basic FBA with cobrapy
      cobra_model = create_cobra_model_from_sbml_doc(model.get_sbml_doc())
      # Optional model parameters are set - TODO KiSAO: suggest new parameters
      obj = self.algorithm.get_parameter_by_name('objective_function')
      sense = self.algorithm.get_parameter_by_name('objective_sense')
      if obj is not None:
        cobra_model.change_objective([obj.get_value()])
      if sense is not None:
        cobra_model.optimize(objective_sense=sense.get_value())
      else:
        cobra_model.optimize()
    res = result.Result()
    res.import_from_cobrapy_fba(cobra_model.solution)
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
  ## and returns its output as a biopredyn.result.Result object.
  # @param self The object pointer.
  # @param model A biopredyn.model.Model object.
  # @param tool Name of the tool to use as simulation engine (string).
  # @return A biopredyn.result.Result object.
  def run(self, model, tool):
    res = result.Result()
    # Tool selection - by default libsbmlsim is chosen
    if tool is None or tool == 'libsbmlsim':
      self.run_as_libsbmlsim_time_course(model, res)
    elif tool == 'copasi':
      self.run_as_copasi_time_course(model, res)
    else:
      raise NameError("Invalid tool name; available names are 'copasi' and 'libsbmlsim'.")
    return res

  ## Run this as a COPASI time course and import its result.
  # @param self The object pointer.
  def run_as_copasi_time_course(self, model, result):
    steps = self.get_number_of_points()
    start = self.get_initial_time()
    o_start = self.get_output_start_time()
    end = self.get_output_end_time()
    step = (end - o_start) / steps
    duration = end - start
    # Importing model to COPASI
    data_model = CCopasiDataModel()
    data_model.importSBMLFromString(model.get_sbml_doc().toSBML())
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
    result.import_from_copasi_time_series(task.getTimeSeries())
    return result

  ## Run this as a libSBMLSim time course and import its result.
  # @param self The object pointer.
  def run_as_libsbmlsim_time_course(self, model, result):
    steps = self.get_number_of_points()
    start = self.get_output_start_time()
    end = self.get_output_end_time()
    step = (end - start) / steps
    # TODO: acquire KiSAO description of the algorithm
    r = libsbmlsim.simulateSBMLFromString(
        model.get_sbml_doc().toSBML(),
        end,
        step,
        1,
        0,
        libsbmlsim.MTHD_RUNGE_KUTTA,
        0)
    result.import_from_libsbmlsim(r)
    return result
  
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
