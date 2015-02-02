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
  
  ## Appends the input biopredyn.workflow.WorkFlow object to self.workflows.
  # @param self The object pointer.
  # @param workflow A biopredyn.workflow.WorkFlow object.
  def add_workflow(self, workflow):
    self.workflows.append(workflow)
  
  ## Getter for self.resource_manager.
  # @param self The object pointer.
  # @return self.resource_manager
  def get_resource_manager(self):
    return self.resource_manager
  
  ## Remove the input biopredyn.workflow.WorkFlow object from self.workflows.
  # @param self The object pointer.
  # @param workflow A biopredyn.workflow.WorkFlow object.
  def remove_workflow(self, workflow):
    try:
      self.workflows.remove(workflow)
    except KeyError:
      print("Input biopredyn.workflow.WorkFlow object does not exist in " +
        "current Project.")
