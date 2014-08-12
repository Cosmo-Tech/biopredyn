#!/usr/bin/env python
# coding=utf-8

import libsbml
from COPASI import *
import sys
from random import random
from biopredyn import result as res
from biopredyn import resources
from matplotlib import pyplot as plt
import numpy as np

def main():
   # create a datamodel
   dataModel = CCopasiRootContainer.addDatamodel()
   # first we load a simple model
   try:
     # load the model 
     dataModel.importSBML('FEBS_copasi.xml')
   except:
     sys.stderr.write("Error while importing the model.\n")
     return 1

   # importing data as a res.Result object column-aligned
   rm = resources.ResourceManager()
   data = res.Result()
   metabVector = data.import_from_csv_file(
      'artificial_data.txt', rm, separator=',', alignment='column')

   # can really find the original values
   rand=random()*10
   reaction=dataModel.getModel().getReaction(0)
   # we know that it is an irreversible mass action, so there is one
   # parameter
   # the parameter of a irreversible mass action is called k1
   reaction.setParameterValue("k1", rand)
   reaction.setParameterValue("k2", rand)
   
   reaction=dataModel.getModel().getReaction(1)
   # we know that it is an irreversible mass action, so there is one
   # parameter
   reaction.setParameterValue("k3", rand)

   fitTask=dataModel.addTask(CFitTask.parameterFitting)
   # the method in a fit task is an instance of COptMethod or a subclass of
   # it.
   fitMethod=fitTask.getMethod()
   # the object must be an instance of COptMethod or a subclass thereof
   # (CFitMethod)
   fitProblem=fitTask.getProblem()
   
   experimentSet=fitProblem.getParameter("Experiment Set")
   
   # first experiment (we only have one here)
   experiment=CExperiment(dataModel)
   # tell COPASI where to find the data
   # reading data from string is not possible with the current C++ API
   experiment.setFileName("artificial_data.txt")
   # we have to tell COPASI that the data for the experiment is a comma
   # separated list (the default is TAB separated)
   experiment.setSeparator(",")
   experiment.setFirstRow(1)
   experiment.setLastRow(4001)
   experiment.setHeaderRow(1)
   experiment.setExperimentType(CCopasiTask.timeCourse)
   experiment.setNumColumns(5)
   objectMap=experiment.getObjectMap()

   result=objectMap.setNumCols(5)
   result=objectMap.setRole(0,CExperiment.time)

   model=dataModel.getModel()
   timeReference=model.getObject(CCopasiObjectName("Reference=Time"))
   objectMap.setObjectCN(0, timeReference.getCN().getString())

   # Assign roles and names with respect to the content of the data file
   for i in range(len(metabVector)):
     name = metabVector[i]
     if not str.lower(name).__contains__("time"):
       for j in range(len(model.getMetabolites())):
         if (model.getMetabolites().get(j).getSBMLId() == name):
            print("IT'S A MATCH")
            metab_object = model.getMetabolites().get(j).getObject(CCopasiObjectName("Reference=Concentration"))
            objectMap.setRole(i, CExperiment.dependent)
            objectMap.setObjectCN(i, metab_object.getCN().getString())
   
   experimentSet.addExperiment(experiment)
   # addExperiment makes a copy, so we need to get the added experiment
   # again
   experiment=experimentSet.getExperiment(0)

   # now we have to define three fit items for the three local parameters
   # of the two reactions
   reaction=model.getReaction(0)

   # first parameter
   parameter=reaction.getParameters().getParameter(0)
   # define a CFitItem
   parameterReference=parameter.getObject(CCopasiObjectName("Reference=Value"))
   fitItem1=CFitItem(dataModel)
   fitItem1.setObjectCN(parameterReference.getCN())
   fitItem1.setStartValue(4.0)
   fitItem1.setLowerBound(CCopasiObjectName("0.00001"))
   fitItem1.setUpperBound(CCopasiObjectName("10"))
   # add the fit item to the correct parameter group
   optimizationItemGroup=fitProblem.getParameter("OptimizationItemList")
   optimizationItemGroup.addParameter(fitItem1)
   
   # second parameter
   parameter=reaction.getParameters().getParameter(1)
   print("Parameter k2: " + parameter.getCN().getString())
   
   # define a CFitItem
   parameterReference=parameter.getObject(CCopasiObjectName("Reference=Value"))
   fitItem2=CFitItem(dataModel)
   fitItem2.setObjectCN(parameterReference.getCN())
   fitItem2.setStartValue(4.0)
   fitItem2.setLowerBound(CCopasiObjectName("0.00001"))
   fitItem2.setUpperBound(CCopasiObjectName("10"))
   # add the fit item to the correct parameter group
   optimizationItemGroup=fitProblem.getParameter("OptimizationItemList")
   optimizationItemGroup.addParameter(fitItem2)

   # second reaction
   reaction=model.getReaction(1)
   print("Reaction 1: " + reaction.getCN().getString())

   # third parameter
   parameter=reaction.getParameters().getParameter(0)
   print("Parameter k3: " + parameter.getCN().getString())
   
   # define a CFitItem
   parameterReference=parameter.getObject(CCopasiObjectName("Reference=Value"))
   fitItem3=CFitItem(dataModel)
   fitItem3.setObjectCN(parameterReference.getCN())
   fitItem3.setStartValue(4.0)
   fitItem3.setLowerBound(CCopasiObjectName("0.00001"))
   fitItem3.setUpperBound(CCopasiObjectName("10"))
   # add the fit item to the correct parameter group
   optimizationItemGroup=fitProblem.getParameter("OptimizationItemList")
   optimizationItemGroup.addParameter(fitItem3)
   
   result=True
   try:
     # running the task for this example will probably take some time
     print "This can take some time..."
     result=fitTask.processWithOutputFlags(True, CCopasiTask.ONLY_TIME_SERIES)
   except:
     sys.stderr.write(" Error. Parameter fitting failed.\n")
     return 1
   # the order should be the order in whih we added the items above
   optItem1 = fitProblem.getOptItemList()[0]
   optItem2 = fitProblem.getOptItemList()[1]
   optItem3 = fitProblem.getOptItemList()[2]
   # the actual results are stored in the fit problem
   print("value for " + optItem1.getObject().getCN().getString() + ": " +
        str(fitProblem.getSolutionVariables().get(0)))
   print("value for " + optItem2.getObject().getCN().getString() + ": " +
        str(fitProblem.getSolutionVariables().get(1)))
   print("value for " + optItem3.getObject().getCN().getString() + ": " +
        str(fitProblem.getSolutionVariables().get(2)))

   # plotting model results vs artificial data
   # first we run a simulation with the computed values of the parameters
   trajectoryTask = dataModel.getTask("Time-Course")
   # if there isn't one
   if trajectoryTask == None:
       # create a one
       trajectoryTask = CTrajectoryTask()
       # add the time course task to the task list
       # this method makes sure that the object is now owned 
       # by the list and that it does not get deleted by SWIG
       dataModel.getTaskList().addAndOwn(trajectoryTask)

   # run a deterministic time course
   trajectoryTask.setMethodType(CCopasiMethod.deterministic)

   # pass a pointer of the model to the problem
   trajectoryTask.getProblem().setModel(dataModel.getModel())

   # activate the task so that it will be run when the model is saved
   # and passed to CopasiSE
   trajectoryTask.setScheduled(True)

   # get the problem for the task to set some parameters
   problem = trajectoryTask.getProblem()

   reaction=dataModel.getModel().getReaction(0)
   reaction.setParameterValue("k1", fitProblem.getSolutionVariables().get(0))
   reaction.setParameterValue("k2", fitProblem.getSolutionVariables().get(1))
   reaction=dataModel.getModel().getReaction(1)
   reaction.setParameterValue("k3", fitProblem.getSolutionVariables().get(2))

   # simulate 4000 steps
   problem.setStepNumber(4000)
   # start at time 0
   dataModel.getModel().setInitialTime(0.0)
   # simulate a duration of 400 time units
   problem.setDuration(20)
   # tell the problem to actually generate time series data
   problem.setTimeSeriesRequested(True)

   # set some parameters for the LSODA method through the method
   method = trajectoryTask.getMethod()

   result=True
   try:
       # now we run the actual trajectory
       result=trajectoryTask.processWithOutputFlags(True, CCopasiTask.ONLY_TIME_SERIES)
   except:
       sys.stderr.write(" Error. Running the time course simulation failed.\n")
       # check if there are additional error messages
       if CCopasiMessage.size() > 0:
           # print the messages in chronological order
           sys.stderr.write(CCopasiMessage.getAllMessageText(True) + "\n")
       return 1
   if result==False:
       sys.stderr.write("An error occured while running the time course simulation.\n")
       # check if there are additional error messages
       if CCopasiMessage.size() > 0:
           # print the messages in chronological order
           sys.stderr.write(CCopasiMessage.getAllMessageText(True) + "\n")
       return 1

   model_result = res.Result()
   names = model_result.import_from_copasi_time_series(trajectoryTask.getTimeSeries())
   time = np.array(model_result.get_time_steps())
   plt.figure(1)

   # plotting model results
   for s in range(len(metabVector)):
     if not str.lower(metabVector[s]).__contains__("time"):
       print names[s]
       plt.subplot(2,2,s)
       results = model_result.get_quantities_per_species(names[s])
       dat = data.get_quantities_per_species(metabVector[s])
       plt.plot(time, results)
       plt.plot(time, dat, '+')

   plt.show()

if(__name__ == '__main__'):
   main() 
