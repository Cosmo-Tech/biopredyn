#!/usr/bin/env python
# coding=utf-8

from COPASI import *
import sys
from random import gauss

# input values required for data generation
model_file = 'FEBS_antimony_solved.xml' # Using the 'right' parameters
data_file = 'artificial_data.txt'
start = 0.0
end = 20.0
steps = 100
noise_type = 'heteroscedastic' # can be 'homoscedastic' or 'heteroscedastic'
std_dev = 0.1 # experimental data standard deviation
observables = ['sp_E', 'sp_C', 'sp_P', 'sp_S'] # vector of SBML IDs - observable quantities

# derived values are computed
duration = end - start

data_model = CCopasiDataModel()
data_model.importSBML(model_file)

trajectory_task = data_model.addTask(CTrajectoryTask.timeCourse)
trajectory_task.setMethodType(CCopasiMethod.deterministic)
trajectory_task.getProblem().setModel(data_model.getModel())

# get the problem for the task to set some parameters
problem = trajectory_task.getProblem()

# simulation conditions
problem.setStepNumber(steps)
data_model.getModel().setInitialTime(start)
problem.setDuration(duration)

result = True
try:
  # now we run the actual trajectory
  result = trajectory_task.processWithOutputFlags(
    True, CCopasiTask.ONLY_TIME_SERIES)
except:
  print >> sys.stderr, "Error. Running the time course simulation failed."
  # check if there are additional error messages
  if CCopasiMessage.size() > 0:
    # print the messages in chronological order
    print >> sys.stderr, CCopasiMessage.getAllMessageText(True)
if result == False:
  print >> sys.stderr, "An error occured while running the time course simulation."
  # check if there are additional error messages
  if CCopasiMessage.size() > 0:
    # print the messages in chronological order
    print >> sys.stderr, CCopasiMessage.getAllMessageText(True)

time_series = trajectory_task.getTimeSeries()
num_variables = time_series.getNumVariables()
last_index = time_series.getRecordedSteps()

# open and write the file - time goes first
os = open(data_file, "w")
os.write("# time ")

for i in range(1, num_variables):
  name = time_series.getSBMLId(i, data_model)
  # time is already
  if name in observables:
    os.write(",")
    os.write(name)
os.write("\n")
for i in range(0, last_index):
  s = ""
  for j in range(0, num_variables):
    name = time_series.getSBMLId(j, data_model)
    # time should not be added noise
    if j == 0:
      data = time_series.getConcentrationData(i, j)
      s = s + str(data)
      s = s + ","
    # only observable quantities are written in output file
    elif name in observables:
      data = time_series.getConcentrationData(i, j)
      # apply noise
      if noise_type == 'heteroscedastic':
        # heteroscedastic case
        sigma = data * std_dev
      elif noise_type == 'homoscedastic':
        # homoscedastic case
        sigma = std_dev
      else:
        sys.exit("Invalid noise type; expected noise types are " +
          "'homoscedastic' or 'heteroscedastic'.")
      data = gauss(data, sigma)
      s = s + str(data)
      s = s + ","
  # remove the last comma
  os.write(s[0:-1])
  os.write("\n")
os.close()
