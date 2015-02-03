#!/usr/bin/env python
# coding=utf-8

## @package biopredyn
## Copyright: [2012-2015] The CoSMo Company, All Rights Reserved
## License: BSD 3-Clause

from .. import resources, workflow

## Class for handling projects in BioPreDyn user interface.
# A Project object holds a list of WorkFlow objects and a ResourceManager.
class Project:
  ## @var resource_manager
  # A biopredyn.resources.ResourceManager object.
  ## @var workflows
  # A list of biopredyn.workflow.WorkFlow objects.
  
  ## Constructor.
  # @param self The object pointer.
  def __init__(self):
    self.workflows = []
    self.resource_manager = resources.ResourceManager()
  
  ## Create a new biopredyn.workflow.WorkFlow object from the input 'source' and
  ## adds it to self.workflows.
  # @param self The object pointer.
  # @param source Complete filename of a valid SED-ML workflow.
  def add_workflow(self, source):
    wf = workflow.WorkFlow(self.resource_manager, source=source)
    # TODO self.workflows.append(workflow)
  
  ## Getter for self.resource_manager.
  # @param self The object pointer.
  # @return self.resource_manager
  def get_resource_manager(self):
    return self.resource_manager
  
  ## Create a new biopredyn.workflow.WorkFlow object and adds it to
  ## self.workflows.
  # @param self The object pointer.
  def new_workflow(self):
    wf = workflow.WorkFlow(self.resource_manager)
    # TODO self.workflows.append(workflow)
  
  ## Remove the active workflow from self.workflows.
  # @param self The object pointer.
  def remove_workflow(self):
    print("TODO") # TODO 
  
  ## Runs the active workflow i.e. runs its tasks, then process its outputs.
  # @param self The object pointer.
  def run_workflow(self):
    # workflow.run_tasks()
    # workflow.process_outputs()
    print("TODO") # TODO
  
  ## Writes the active workflow to the input location 'source' as a SED-ML
  ## file.
  # @param self The object pointer.
  # @param source Where to write the active workflow; optional. If not
  # specified, the 'source' attribute of the active workflow is used. 
  def write_workflow(self, source=None):
    print("TODO") # TODO
