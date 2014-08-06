#!/usr/bin/env python
# coding=utf-8

## @package biopredyn
## $Author$
## $Date$
## $Copyright: 2014, The CoSMo Company, All Rights Reserved $
## $License: BSD 3-Clause $
## $Revision$

import libsbmlsim
import libnuml
from matplotlib import pyplot as plt
import array

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
  
  ## Returns the value of all fluxes in self.result as a vector of values.
  # @param self The object pointer.
  # @return The vector of fluxes, without growth_rate.
  def get_fluxes(self):
    vector = []
    for f in self.result:
      if str(f) != "growth_rate":
        vector.append(self.result[f])
    return vector
  
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
    for t in self.result:
      if str.lower(t).__contains__("time"):
        return self.result[t]
    sys.exit("Error: no time series found.")
  
  ## Import numerical values from the output of a cobrapy flux balance analysis
  ## and store them in self.result. The resulting growth rate is stored as the
  ## value of the 'growth_rate' key.
  # @param self The object pointer.
  # @param solution Solution of a cobrapy FBA.
  def import_from_cobrapy_fba(self, solution):
    self.result["growth_rate"] = [solution.f]
    for p in solution.x_dict.iteritems():
      self.result[p[0]] = [p[1]]

  ## Import numerical values from a COPASI.CTimeSeries object.
  # @param self The object pointer.
  # @param time_series A COPASI.CTimeSeries object.
  def import_from_copasi_time_series(self, time_series):
    for i in range(time_series.getNumVariables()):
      self.result[time_series.getTitles()[i]] = time_series.getDataForIndex(i)
  
  ## Import numerical values from a CSV file and store them in self.result. The
  ## way data is stored in the file (row or column wise) is specified by the
  ## 'alignment' argument.
  # @param self The object pointer.
  # @param address Address of a CSV file (either .csv or .txt).
  # @param manager A ResourceManager instance.
  # @param separator A string indicating the type of separator to be expected
  # between the data values; possible values are ',', ' ', '\\t', ';', '|' and
  # ':' (default '\\t').
  # @param alignment String value indicating the way data is aligned in the
  # input file; possible values are 'row' and 'column' (default 'row').
  # @param header_size Integer value indicating the size of the file header in
  # number of lines (default 0).
  def import_from_csv_file(self, address, manager, separator='\t',
    alignment='row', header_size=0):
    if not separator in (',', ' ', '\t', ';', '|', ':'):
      sys.exit("Invalid separator: " + separator + "\n" +
               "Possible values are: ',', ' ', '\t', ';', '|' and ':'.")
    if address.endswith('csv') or address.endswith('txt'):
      file = manager.get_resource(address)
      # Skipping potential header
      for h in range(header_size):
        file.readline()
      if alignment == 'row':
        for line in file:
          ls = line.split(separator)
          name = str(ls.pop(0))
          f_ls = [float(i) for i in ls]
          self.result[name] = f_ls
      elif alignment == 'column':
        # Initializing items
        names = file.readline().rstrip('\n').split(separator)
        for n in names:
          self.result[n.rstrip('\n')] = []
        # Filling the values
        for line in file:
          l = line.rstrip('\n')
          values = l.split(separator)
          for v in range(len(values)):
            self.result[names[v]].append(float(values[v]))
      else:
        file.close()
        sys.exit("Invalid alignment: " + alignment + "\n" +
                 "Possible values are: 'row', 'column'.")
    else:
      sys.exit("Invalid file format.")
  
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
  # @param address Address of a NuML file.
  # @param manager A ResourceManager instance.
  # @param component Index of the resultComponent to be considered; default 0.
  def import_from_numl_file(self, address, manager, component=0):
    if address.endswith('xml'):
      file = manager.get_resource(address)
      reader = libnuml.NUMLReader()
      doc = reader.readNUMLFromString(file.read())
      if doc.getNumErrors() > 0:
        print("Error code " + str(doc.getError(0).getErrorId()) + " at line " +
              str(doc.getError(0).getLine()) + " when opening file: " +
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
    else:
      sys.exit("Invalid file format.")
