#!/usr/bin/env python
# coding=utf-8

from COPASI import *
import sys
from random import random

dataModel = CCopasiDataModel()
dataModel.importSBML('FEBS_copasi.xml')

trajectoryTask = dataModel.addTask(CTrajectoryTask.timeCourse)
trajectoryTask.setMethodType(CCopasiMethod.deterministic)
trajectoryTask.getProblem().setModel(dataModel.getModel())

# get the problem for the task to set some parameters
problem = trajectoryTask.getProblem()

# simulate 4000 steps
problem.setStepNumber(4000)
# start at time 0
dataModel.getModel().setInitialTime(0.0)
# simulate a duration of 20 time units
problem.setDuration(20)
# tell the problem to actually generate time series data
problem.setTimeSeriesRequested(True)

trajectoryTask.setScheduled(True)

result=True
try:
    # now we run the actual trajectory
    result=trajectoryTask.processWithOutputFlags(True, CCopasiTask.ONLY_TIME_SERIES)
except:
    print >> sys.stderr,  "Error. Running the time course simulation failed." 
    # check if there are additional error messages
    if CCopasiMessage.size() > 0:
        # print the messages in chronological order
        print >> sys.stderr, CCopasiMessage.getAllMessageText(True)
if result==False:
    print >> sys.stderr,  "An error occured while running the time course simulation." 
    # check if there are additional error messages
    if CCopasiMessage.size() > 0:
        # print the messages in chronological order
        print >> sys.stderr, CCopasiMessage.getAllMessageText(True)

# This is necessary since COPASI can only read experimental data from
# file.
timeSeries = trajectoryTask.getTimeSeries()
iMax = timeSeries.getNumVariables()
lastIndex = timeSeries.getRecordedSteps()
print(lastIndex)
# open the file
# we need to remember in which order the variables are written to file
# since we need to specify this later in the parameter fitting task
indexSet=[]
metabVector=[]

# write the header
# the first variable in a time series is a always time, for the rest
# of the variables, we use the SBML id in the header
rand=0.0
os=open("artificial_data.txt","w")
os.write("# time ")
keyFactory=CCopasiRootContainer.getKeyFactory()
assert keyFactory != None
for i in range(1,iMax):
 key=timeSeries.getKey(i)
 object=keyFactory.get(key)
 assert object != None
 # only write header data or metabolites
 if object.__class__==CMetab:
   os.write(",")
   os.write(timeSeries.getSBMLId(i,dataModel))
   indexSet.append(i)
   metabVector.append(object)
os.write("\n")
data=0.0
for i in range(0,lastIndex):
 s=""
 for j in range(0,iMax):
   # we only want to  write the data for metabolites
   # the compartment does not interest us here
   if j==0 or (j in indexSet):
     # write the data with some noise (+-5% max)
     rand=random()
     data=timeSeries.getConcentrationData(i, j)
     # don't add noise to the time
     if j!=0:
       data+=data*(rand*0.1-0.05)
     s=s+str(data)
     s=s+","
 # remove the last two characters again
 os.write(s[0:-2])
 os.write("\n")
os.close()
