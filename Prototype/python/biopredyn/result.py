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
import numpy as np

## Base class for simulation results
class Result:
  ## @var result
  # Dictionary containing the numerical output of a simulation run. Keys are
  # names and values are numerical results (dimensionality of the results
  # depend on the type of simulation).
  
  ## Constructor.
  # @param self The object pointer.
  def __init__(self):
    self.result = dict()

  ## Getter. Returns self.result.
  # @param self The object pointer.
  # @return self.result
  def get_result(self):
    return self.result

## Result derived class for time series formatted simulation results.
# In a TimeSeries class, values of self.result are arrays of experiments,
# except values of the 'time' key, which are numerical values. An experiment is
# a vector of numerical values.
class TimeSeries(Result):

  ## Constructor.
  # @param self The object pointer.
  def __init__(self):
    Result.__init__(self)
  
  ## Returns the list of experiment for the input species over time.
  # @param self The object pointer.
  # @param species The species which quantity values are wanted. 
  # @return A list of quantity values for the input species over time.
  def get_quantities_per_species(self, species):
    return self.result[species]
  
  ## Returns the list of all time steps in self.result.
  # @param self The object pointer.
  # @return The list of time steps.
  def get_time_steps(self):
    for t in self.result:
      if str.lower(t).__contains__("time"):
        return self.result[t]
    sys.exit("Error: no time series found.")

  ## Import numerical values from a COPASI.CTimeSeries object.
  # @param self The object pointer.
  # @param time_series A COPASI.CTimeSeries object.
  # @param species A list of strings: the title of the species which data
  # should be extracted from the input time_series; if None, all time series
  # are extracted (default: None).
  # @return A vector containing the names of the time series listed in the
  # input file.
  def import_from_copasi_time_series(self, time_series, species=None):
    names = []
    for i in range(time_series.getNumVariables()):
      name = time_series.getTitle(i)
      if str.lower(name).__contains__('time'):
        self.result[name] = np.array(time_series.getDataForIndex(i))
      elif ((species is not None and name in species)
        or species is None):
        names.append(name)
        res = time_series.getDataForIndex(i)
        value = []
        for r in res:
          value.append(np.array([r]))
        self.result[name] = np.array(value)
    return names
  
  ## Import numerical values from a CSV file and store them in self.result.
  # Data is expected to be stored column-wise:
  #
  # time, species_1, ..., species_N
  #
  # 0.0, 0.256, ..., 0.321
  #
  # 0.0, 0.276, ..., 0.332
  #
  # ..., ..., ..., ...
  #
  # The first column of the input file HAS to list time steps.
  # @param self The object pointer.
  # @param address Address of a CSV file (either .csv or .txt).
  # @param manager A ResourceManager instance.
  # @param separator A string indicating the type of separator to be expected
  # between the data values; possible values are ',', ' ', '\\t', ';', '|' and
  # ':' (default ',').
  # @param alignment String value indicating the way data is aligned in the
  # input file; possible values are 'row' and 'column' (default 'row').
  # @param header Integer value indicating the size of the file header in
  # number of lines i.e. the number of line to be skipped when parsing the file
  # (default 0).
  # @return A vector containing the names of the time series listed in the
  # input file.
  def import_from_csv_file(self, address, manager, separator=',', header=0):
    if not separator in (',', ' ', '\t', ';', '|', ':'):
      sys.exit("Invalid separator: " + separator + "\n" +
               "Possible values are: ',', ' ', '\t', ';', '|' and ':'.")
    if address.endswith('csv') or address.endswith('txt'):
      file = manager.get_resource(address)
      names = []
      # Skipping potential header
      for h in range(header):
        file.readline()
      # Initializing items
      names = file.readline().rstrip('\n').rstrip('\r').split(separator)
      for n in names:
        self.result[n.rstrip('\n').rstrip('\r')] = []
      # Filling the values
      for line in file:
        l = line.rstrip('\n').rstrip('\r')
        values = l.split(separator)
        # test whether new vectors of experiment should be created
        if (len(self.result['time'] == 0)
          or values[0] != self.result['time'][-1]):
          self.result['time'].append(values[0])
          for v in range(1, len(values)):
            self.result[names[v]].append([])
        # populate vectors of experiment
        for p in range(1, len(values)):
          self.result[names[p]][-1].append(float(values[p]))
      # Convert all values to np.array
      for key in self.result.keys():
        self.result[key] = np.array(self.result[key])
      return names
    else:
      sys.exit("Invalid file format.")
  
  ## Import numerical values from the output of a libSBMLSim simulation and
  ## store them in self.result.
  # @param self The object pointer.
  # @param result Result of a libSBMLSim simulation.
  # @param output_start Which time point to consider as the first output.
  # @return A vector containing the names of the time series listed in the
  # input file.
  def import_from_libsbmlsim(self, result, output_start):
    rows = result.getNumOfRows()
    # Time extraction
    time = []
    for r in range(rows):
      t = result.getTimeValueAtIndex(r)
      if t >= output_start:
        time.append(result.getTimeValueAtIndex(r))
    self.result["time"] = np.array(time)
    # Species and miscellaneous values
    names = []
    for s in range(result.getNumOfSpecies()):
      species = []
      name = result.getSpeciesNameAtIndex(s)
      names.append(name)
      for t in range(rows):
        current = result.getTimeValueAtIndex(r)
        if current >= output_start:
          species.append(np.array([result.getSpeciesValueAtIndex(name, t)]))
      self.result[name] = np.array(species)
    return names
  
  ## Import time series from a NuML file and store them in self.result. This
  ## function expects the following layout for the considered resultComponent
  ## element:
  ##
  ## - resultComponent id="time_series"
  ##   + dimensionDescription
  ##   - dimension
  ##     - compositeValue indexValue=0.0
  ##       - compositeValue indexValue="species_1"
  ##         - tuple
  ##           - atomicValue value=0.256
  ##           + atomicValue
  ##           [...]
  ##           + atomicValue
  ##       + compositeValue
  ##       [...]
  ##       + compositeValue
  ##     + compositeValue indexValue=0.2
  ##     [...]
  ##     + compositeValue indexValue=M
  ##
  ## This file should contain only one resultComponent node which id is
  ## 'time_series'.
  # @param self The object pointer.
  # @param address Address of a NuML file.
  # @param manager A ResourceManager instance.
  # @return A vector containing the names of the time series listed in the
  # input file.
  def import_from_numl_file(self, address, manager):
    names = []
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
        # extract metadata
        dim = doc.getResultComponents().get('time_series').getDimension()
        self.result['time'] = []
        # Acquiring keys and initializing values
        for k in dim.get(0):
          self.result[k.getIndexValue()] = []
          names.append(k.getIndexValue())
        # Populating values
        for i in dim: # time level
          self.result['time'].append(float(i.getIndexValue()))
          for v in i: # species level
            exp = []
            for e in v: # experiment level
              exp.append(e.getAtomicValue().getDoubleValue())
            self.result[v.getIndexValue()].append(np.array(exp))
        # Convert all values to np.array
        for key in self.result.keys():
          self.result[key] = np.array(self.result[key])
    else:
      sys.exit("Invalid file format.")
    return names

class Fluxes(Result):

  ## Constructor.
  # @param self The object pointer.
  def __init__(self):
    Result.__init__(self)
  
  ## Returns the value of all fluxes in self.result as a vector of values.
  # @param self The object pointer.
  # @return The vector of fluxes, without growth_rate.
  def get_fluxes(self):
    vector = []
    for f in self.result:
      if str(f) != "growth_rate":
        vector.append(self.result[f])
    return np.array(vector)
  
  ## Import numerical values from the output of a cobrapy flux balance analysis
  ## and store them in self.result. The resulting growth rate is stored as the
  ## value of the 'growth_rate' key.
  # @param self The object pointer.
  # @param solution Solution of a cobrapy FBA.
  # @return A vector containing the names of the time series listed in the
  # input file.
  def import_from_cobrapy_fba(self, solution):
    names = ["growth_rate"]
    self.result["growth_rate"] = [solution.f]
    for p in solution.x_dict.iteritems():
      names.append(p[0])
      self.result[p[0]] = [p[1]]
    return names
