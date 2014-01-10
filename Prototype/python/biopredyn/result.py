# coding=utf-8

## @package biopredyn
## @author: $Author$
## @date: $Date$
## @copyright: $Copyright: [2013] BioPreDyn $
## @version: $Revision$

import libsbmlsim
import libnuml
from matplotlib import pyplot as plt

## Base class for simulation results
class Result:
  ## @var result 
  # Pointer to the output of a simulation run. Results are always stored as
  # a dictionary where keys are names and values are arrays, for instance:
  #
  # keys ---> |  Time  | Species_1 | Species_2 | Error_1 | Error_2 |
  #           |--------|-----------|-----------|---------|---------|
  #           | 0.01   | 1.256e-6  | 5.21e-5   | 2.5e-8  | 1.23e-5 |
  #           | 0.16   | 1.004e-6  | 5.51e-5   | 6.7e-8  | 1.00e-5 |
  # values -> | 0.23   | 8.564e-7  | 5.13e-5   | 5.9e-7  | 8.96e-6 |
  #           | 0.47   | 5.735e-7  | 5.03e-5   | 2.4e-8  | 1.02e-5 |
  #           | 0.59   | 3.246e-7  | 5.45e-5   | 3.1e-8  | 1.17e-5 |
  
  ## Constructor.
  # @param self The object pointer.
  def __init__(self):
    self.result = dict()
  
  ## Returns the number of time series in self.result; potential "time" series
  ## are not counted as time series.
  # @param self The object pointer.
  # @return The numbr of time series in self.result.
  def get_number_of_series(self):
    number = 0;
    for i in self.result:
      if str.lower(i) != "time":
        number = number + 1
    return number
  
  ## Returns a list containing all the quantity values for the input species
  ## over time.
  # @param self The object pointer.
  # @param species The species which quantity values are wanted. 
  # @return A list of quantity values for the input species over time.
  def get_quantities_per_species(self, species):
    return self.result[species]

  ## Getter. Returns self.result.
  # @param self The object pointer.
  # @return self.result
  def get_result(self):
    return self.result
  
  ## Returns the list of all time steps in self.result.
  # @param self The object pointer.
  # @return The list of time steps.
  def get_time_steps(self):
    return self.result["time"]
  
  ## Import numerical values from the output of a libSBMLSim simulation and
  ## store them in self.result.
  # @param self The object pointer.
  # @param result Result of a libSBMLSim simulation.
  def import_from_libsbmlsim(self, result):
    rows = result.getNumOfRows()
    # Time extraction
    time = []
    for r in range(rows):
      time.append(result.getTimeValueAtIndex(r))
    self.result["time"] = time
    # Species and miscellaneous values
    for s in range(result.getNumOfSpecies()):
      species = []
      name = result.getSpeciesNameAtIndex(s)
      for t in range(rows):
        species.append(result.getSpeciesValueAtIndex(name, t))
      self.result[name] = species
  
  ## Import numerical values from a NuML file and store them in self.result.
  ## This function expects the following layout for the considered
  ## resultComponent element:
  ##
  ## - resultComponent
  ##   + dimensionDescription
  ##   - dimension
  ##     - compositeValue indexValue=0
  ##       - compositeValue indexValue="time"
  ##         + atomicValue
  ##       - compositeValue indexValue="species_1"
  ##         + atomicValue
  ##       - compositeValue indexValue="species_2"
  ##         + atomicValue
  ##       [...]
  ##       - compositeValue indexValue="species_N"
  ##         + atomicValue
  ##     + compositeValue indexValue=1
  ##     [...]
  ##     + compositeValue indexValue=M
  ##
  ## This file should contain only one resultComponent
  # @param self The object pointer.
  # @param file Address of a NuML file.
  # @param component Index of the resultComponent to be considered; default 0.
  def import_from_numl_file(self, file, component=0):
    reader = libnuml.NUMLReader()
    doc = reader.readNUMLFromFile(file)
    if doc.getNumErrors() > 0:
      print("Error code " + str(doc.getError(0).getErrorId()) +
            " when opening file: " +
            str(doc.getError(0).getShortMessage()))
      sys.exit(2)
    else:
      # Process the file normally
      dim = doc.getResultComponents().get(component).getDimension()
      # Acquiring keys and initializing values
      for k in dim.get(0):
        self.result[k.getIndexValue()] = []
      # Populating values
      for i in dim:
        for v in i:
          self.result[v.getIndexValue()].append(
            v.getAtomicValue().getDoubleValue())
