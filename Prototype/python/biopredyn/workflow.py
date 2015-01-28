#!/usr/bin/env python
# coding=utf-8

## @package biopredyn
## Copyright: [2012-2015] The CoSMo Company, All Rights Reserved
## License: BSD 3-Clause

import numpy as np
import sys, os
import libsbml
import libsedml
import model, output, result, task, simulation, datagenerator
from matplotlib import pyplot as plt

## Class for SED-ML generic work flows.
class WorkFlow:
  ## @var source
  # Address of the SED-ML file associated with the object.
  ## @var data_generators
  # A list of DataGenerator elements.
  ## @var models
  # A list of Model elements.
  ## @var outputs
  # A list of Output elements.
  ## @var resource_manager
  # Resource manager for the current work flow.
  ## @var sedml
  # A SED-ML document.
  ## @var tasks
  # A list of Task elements.
  ## @var simulations
  # A list of Simulation elements.
  
  ## Constructor.
  # @param self The object pointer.
  # @param res_man A biopredyn.resources.ResourceManager object.
  # @param source Address of the SED-ML file to be read; optional (default:
  # None).
  def __init__(self, res_man, source=None):
    self.resource_manager = res_man
    self.models = []
    self.simulations = []
    self.tasks = []
    self.data_generators = []
    self.outputs = []
    if source is not None:
      self.source = source
      fl = self.resource_manager.get_resource(self.source)
      reader = libsedml.SedReader()
      self.sedml = reader.readSedMLFromString(fl.read())
      self.check()
      # Parsing self.sedml for model elements
      for m in self.sedml.getListOfModels():
        self.add_model(
          model.Model(self.resource_manager, model=m, workflow=self))
      # Parsing self.sedml for simulation elements
      for s in self.sedml.getListOfSimulations():
        s_name = s.getElementName()
        if s_name == "uniformTimeCourse":
          self.add_simulation(simulation.UniformTimeCourse(simulation=s))
        elif s_name == "oneStep":
          self.add_simulation(simulation.OneStep(simulation=s))
        elif s_name == "steadyState":
          self.add_simulation(simulation.SteadyState(simulation=s))
        else:
          self.add_simulation(simulation.Simulation(simulation=s))
      # Parsing self.sedml for task elements
      for t in self.sedml.getListOfTasks():
        t_name = t.getElementName()
        if t_name == "task":
          self.add_task(task.Task(self, task=t))
        elif t_name == "repeatedTask":
          self.add_task(task.RepeatedTask(self, task=t))
        else:
          self.add_task(task.AbstractTask(task=t))
      # Parsing self.sedml for data generator elements
      for d in self.sedml.getListOfDataGenerators():
        self.add_data_generator(datagenerator.DataGenerator(d, self))
      # Parsing self.sedml for output elements
      for o in self.sedml.getListOfOutputs():
        o_name = o.getElementName()
        if o_name == "plot2D":
          self.add_output(output.Plot2D(o, self))
        elif o_name == "plot3D":
          self.add_output(output.Plot3D(o, self))
        elif o_name == "report":
          self.add_output(output.Report(o, self))
        else:
          self.add_output(output.Output(o))
  
  ## String representation of this. Displays it as a hierarchy.
  # @param self The object pointer.
  # @return A string representing this as a hierarchy.
  def __str__(self):
    tree = "Work flow: " + self.source + "\n"
    if len(self.simulations) > 0:
      tree += "|-listOfSimulations\n"
      for s in self.simulations:
        tree += str(s)
    if len(self.models) > 0:
      tree += "|-listOfModels\n"
      for m in self.models:
        tree += str(m)
    if len(self.tasks) > 0:
      tree += "|-listOfTasks\n"
      for t in self.tasks:
        tree += str(t)
    if len(self.data_generators) > 0:
      tree += "|-listOfDataGenerators\n"
      for d in self.data_generators:
        tree += str(d)
    if len(self.outputs) > 0:
      tree += "|-listOfOutputs\n"
      for o in self.outputs:
        tree += str(o)
    return tree

  ## Appends the input biopredyn.datagenerator.DataGenerator object to
  # self.datagenerators.
  # @param self The object pointer.
  # @param dg A biopredyn.datagenerator.DataGenerator instance.
  def add_data_generator(self, dg):
    self.data_generators.append(dg)

  ## Appends the input biopredyn.model.Model object to
  # self.models.
  # @param self The object pointer.
  # @param md A biopredyn.model.Model instance.
  def add_model(self, md):
    self.models.append(md)

  ## Appends the input biopredyn.output.Output object to
  # self.outputs.
  # @param self The object pointer.
  # @param op A biopredyn.output.Output instance.
  def add_output(self, op):
    self.outputs.append(op)

  ## Appends the input biopredyn.simulation.Simulation object to
  # self.simulations.
  # @param self The object pointer.
  # @param sm A biopredyn.simulation.Simulation instance.
  def add_simulation(self, sm):
    self.simulations.append(sm)

  ## Appends the input biopredyn.task.Task object to
  # self.tasks.
  # @param self The object pointer.
  # @param tk A biopredyn.task.Task instance.
  def add_task(self, tk):
    self.tasks.append(tk)
  
  ## SED-ML compliance check function.
  # Check whether self.sedml is compliant with the SED-ML standard; if
  # not, boolean value false is returned and the first error code met by the
  # reader is printed; if yes, the method returns a pointer to the SED-ML model
  # instead.
  # @param self The object pointer.
  # @return self.sedml
  def check(self):
    if self.sedml.getNumErrors() > 0:
      print("Error code " + str(self.sedml.getError(0).getErrorId()) +
            " at line " + str(self.sedml.getError(0).getLine()) + 
            " when opening file " + str(self.source) + ": " +
            str(self.sedml.getError(0).getShortMessage()))
      sys.exit(2)
    else:
      print("Document " + self.source + " is SED-ML compliant.")
      # check compatibility with SED-ML level 1
      print( str(self.sedml.checkCompatibility(self.sedml)) +
        " compatibility errors with SED-ML." )
      return self.sedml
  
  ## Getter. Returns a data generator referenced by the input id listed in
  # self.models.
  # @param self The object pointer.
  # @param id The id of the data generator to be returned.
  # @return model A DataGenerator object.
  def get_data_generator_by_id(self, id):
    for d in self.data_generators:
      if d.get_id() == id:
        return d
    print("DataGenerator not found: " + id)
    return 0
  
  ## Getter. Returns a model referenced by the input id listed in self.models.
  # @param self The object pointer.
  # @param id The id of the model to be returned.
  # @return model A Model object.
  def get_model_by_id(self, id):
    for m in self.models:
      if m.get_id() == id:
        return m
    print("Model not found: " + id)
    return 0
  
  ## Getter. Returns self.models.
  # @param self The object pointer.
  def get_models(self):
    return self.models
  
  ## Getter. Returns an output referenced by the input id listed in
  ## self.outputs.
  # @param self The object pointer.
  # @param id The id of the biopredyn.output.Output object to be returned.
  # @return output A biopredyn.output.Output object.
  def get_output_by_id(self, id):
    for o in self.outputs:
      if o.get_id() == id:
        return o
    print("Model not found: " + id)
    return 0
  
  ## Getter. Returns self.outputs.
  # @param self The object pointer.
  def get_outputs(self):
    return self.outputs
  
  ## Getter for self.resource_manager.
  # @param self The object pointer.
  # @return self.resource_manager
  def get_resource_manager(self):
    return self.resource_manager
  
  ## Getter. Returns self.sedml.
  # @param self The object pointer.
  def get_sedml(self):
    return self.sedml
  
  ## Getter. Returns a simulation referenced by the input id listed in
  # self.simulations.
  # @param self The object pointer.
  # @param id The id of the simulation to be returned.
  # @return simulation A simulation object.
  def get_simulation_by_id(self, id):
    for s in self.simulations:
      if s.get_id() == id:
        return s
    print("Simulation not found: " + id)
    return 0
  
  ## Getter. Returns self.simulations.
  # @param self The object pointer.
  # @return self.simulations
  def get_simulations(self):
    return self.simulations
  
  ## Getter. Returns self.source.
  # @param self The object pointer.
  def get_source(self):
    return self.source
  
  ## Getter. Returns a task referenced by the input id listed in self.tasks.
  # @param self The object pointer.
  # @param id The id of the task to be returned.
  # @return task A task object.
  def get_task_by_id(self, id):
    for t in self.tasks:
      if t.get_id() == id:
        return t
    print("Task not found: " + id)
    return 0
  
  ## Getter. Returns self.tasks.
  # @param self The object pointer.
  # @return self.tasks
  def get_tasks(self):
    return self.tasks
  
  ## Parse self.outputs and produce the corresponding outputs.
  # @param self The object pointer.
  # @param test Boolean value stating whether this function was called from a
  # test (in which case the plot must be closed). Default False.
  # @param filename Where to write the potential report file (default None).
  def process_outputs(self, test=False, filename=None):
    if test:
      plt.ion()
    if filename == None:
      filename = os.path.join(os.path.dirname(__file__), 'output.csv')
    for o in self.outputs:
      if o.__class__.__name__ == "Plot2D" or o.__class__.__name__ == "Plot3D":
        o.process()
      elif o.__class__.__name__ == "Report":
        o.process(filename)
      else:
        sys.exit("Error: invalid output type. Possible output types are: " +
              "Plot2D, Plot3D, Report")
    plt.show()
    if test:
      plt.close()
  
  ## Executes the pipeline encoded in self.sedml.
  # Each task in self.tasks is executed.
  # libSBMLSim is used as simulation engine.
  # @param self The object pointer.
  def run_tasks(self):
    # Parse the list of tasks in the input file; by default model changes apply
    for t in self.tasks:
      t.run(True)
