#!/usr/bin/env python
# coding=utf-8

import libsbml
import libsbmlsim
import numpy as np
import matplotlib.pyplot as plt
from biopredyn import result

# Open SBML file
reader = libsbml.SBMLReader()
doc = reader.readSBMLFromFile('FEBS_copasi.xml')

# Simulation conditions
start = 0.0
end = 20.0
steps = 4000.0
step = (end - start) / steps

# Simulate model with stiff solver
r_stiff = libsbmlsim.simulateSBMLFromString(
    doc.toSBML(),
    end,
    step,
    1,
    0,
    libsbmlsim.MTHD_RUNGE_KUTTA,
    0)
stiff_result = result.Result()
stiff_result.import_from_libsbmlsim(r_stiff)

# Simulate model with non-stiff solver
r_non_stiff = libsbmlsim.simulateSBMLFromString(
    doc.toSBML(),
    end,
    step,
    1,
    0,
    libsbmlsim.MTHD_ADAMS_MOULTON_2,
    0)
non_stiff_result = result.Result()
names = non_stiff_result.import_from_libsbmlsim(r_non_stiff)

# Plot results - for each species, time series produced
# by both solvers are plotted
time = np.array(stiff_result.get_time_steps()) # Same for all plots
plt.figure(1)
for s in range(len(names)):
  if not str.lower(names[s]).__contains__("time"):
    plt.subplot(2,2,s)
    stiff = stiff_result.get_quantities_per_species(names[s])
    non_stiff = non_stiff_result.get_quantities_per_species(names[s])
    plt.plot(time, stiff, time, non_stiff)

# Plot difference between stiff and non-stiff solutions
plt.figure(2)
for s in range(len(names)):
  if not str.lower(names[s]).__contains__("time"):
    stiff = np.array(stiff_result.get_quantities_per_species(names[s]))
    non_stiff = np.array(non_stiff_result.get_quantities_per_species(names[s]))
    diff = abs(stiff - non_stiff)
    plt.plot(time, diff)

plt.show()
