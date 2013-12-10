## @package biopredyn
## @author: $Author$
## @date: $Date$
## @copyright: $Copyright: [2013] BioPreDyn $
## @version: $Revision$

import numpy as np

import libsedml
import data, model, output, result, task, simulation, datagenerator

## Class for SED-ML generic work flows.
class WorkFlow:
  ## @var source
  # Address of the SED-ML file associated with the object.
  ## @var data_generators
  # A list of DataGenerator elements.
  ## @var models
  # A list of Model elements.
  ## @var outputs
  # A list of Output elements
  ## @var sedml
  # A SED-ML document.
  ## @var tasks
  # A list of Task elements.
  ## @var simulations
  # A list of Simulation elements.
  
  ## Constructor.
  # @param self The object pointer.
  # @param file Address of the SED-ML file to be read.
  def __init__(self, file):
    self.source = file
    reader = libsedml.SedReader()
    self.sedml = reader.readSedML(file)
    self.check()
    # Parsing self.sedml for model elements
    self.models = []
    for m in self.sedml.getListOfModels():
      self.models.append(model.SBMLModel(model=m))
    # Parsing self.sedml for simulation elements
    self.simulations = []
    for s in self.sedml.getListOfSimulations():
      s_name = s.getElementName()
      if s_name == "uniformTimeCourse":
        self.simulations.append(simulation.UniformTimeCourse(s))
      else:
        self.simulations.append(simulation.Simulation(s))
    # Parsing self.sedml for task elements
    self.tasks = []
    for t in self.sedml.getListOfTasks():
      # TODO: check whether the tools are set
      self.tasks.append(task.Task(t, self))
    # Parsing self.sedml for data generator elements
    self.data_generators = []
    for d in self.sedml.getListOfDataGenerators():
      self.data_generators.append(datagenerator.DataGenerator(d, self))
    # Parsing self.sedml for output elements
    self.outputs = []
    for o in self.sedml.getListOfOutputs():
      o_name = o.getElementName()
      if o_name == "plot2D":
        self.outputs.append(output.Plot2D(o, self))
      elif o_name == "plot3D":
        self.outputs.append(output.Plot3D(o, self))
      elif o_name == "report":
        self.outputs.append(output.Report(o, self))
      else:
        self.outputs.append(output.Output(o))
  
  ## String representation of this. Displays it as a hierarchy.
  # @param self The object pointer.
  # @return A string representing this as a hierarchy.
  def __str__(self):
    tree = "Work flow: " + self.source + "\n"
    tree += "|-listOfSimulations\n"
    for s in self.simulations:
      tree += str(s)
    tree += "|-listOfModels\n"
    for m in self.models:
      tree += str(m)
    tree += "|-listOfTasks\n"
    for t in self.tasks:
      tree += str(t)
    tree += "|-listOfDataGenerators\n"
    for d in self.data_generators:
      tree += str(d)
    tree += "|-listOfOutputs\n"
    for o in self.outputs:
      tree += str(o)
    return tree
  
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
            " when opening file: " +
            str(self.sedml.getError(0).getShortMessage()))
      sys.exit(2)
    else:
      print("Document " + self.source + " is SED-ML compliant.")
      # check compatibility with SED-ML level 1
      print( str(self.sedml.checkCompatibility(self.sedml)) +
             " compatibility errors with SED-ML L1." )
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
  
  ## Getter. Returns self.outputs.
  # @param self The object pointer.
  def get_outputs(self):
    return self.outputs
  
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
  # @param interactive Boolean value stating whether the plots have to be
  #   drawn in interactive mode or not.
  def process_outputs(self, interactive):
    for o in self.outputs:
      o.process(interactive)
  
  ## Executes the pipeline encoded in self.sedml.
  # Each task in self.tasks is executed.
  # libSBMLSim is used as simulation engine.
  # @param self The object pointer.
  def run_tasks(self):
    # Parse the list of tasks in the input file
    for t in self.tasks:
      t.run()