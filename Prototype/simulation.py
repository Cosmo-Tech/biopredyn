## @package biopredyn
## @author: $Author$
## @date: $Date$
## @copyright: $Copyright: [2013] BioPreDyn $
## @version: $Revision$

import libsedml

## Description of the execution of an algorithm, independent from the model or
## data set it has to be run with.
class Simulation:
  ## @var algorithm
  # KiSAO identifier of the algorithm to execute.
  ## @var type
  # Type of simulation.
  
  ## Constructor.
  # @param self The object pointer.
  # @param simulation A SED-ML simulation.
  def __init__(self, simulation):
    self.algorithm = simulation.getAlgorithm().getKisaoID()
    self.type = simulation.getElementName()
  
  ## Getter. Returns self.algorithm.
  # @param self The object pointer.
  # @return self.algorithm
  def get_algorithm(self):
    return self.algorithm
  
  ## Getter. Returns self.type.
  # @param self The object pointer.
  # @return self.type
  def get_type(self):
    return self.type

## Derived class for uniform time course simulations.
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
    self.algorithm = simulation.getAlgorithm().getKisaoID()
    self.type = simulation.getElementName()
    self.initial_time = simulation.getInitialTime()
    self.number_of_points = simulation.getNumberOfPoints()
    self.output_end_time = simulation.getOutputEndTime()
    self.output_start_time = simulation.getOutputStartTime()
  
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