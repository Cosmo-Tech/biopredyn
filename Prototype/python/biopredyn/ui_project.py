#!/usr/bin/env python

## @package biopredyn
## $Author$
## $Date$
## $Copyright: 2014, The CoSMo Company, All Rights Reserved $
## $License: BSD 3-Clause $
## $Revision$

import resources, workflow

## Class for handling projects in BioPreDyn user interface.
# A Project object holds a list of WorkFlow objects and a ResourceManager.
class Project:
  ## @var resource_manager
  # A ResourceManager object.
  ## @var workflows
  # A list of WorkFlow objects.
  
  ## Constructor.
  # @param self The object pointer.
  def __init__(self):
    self.workflows = []
    self.resource_manager = resources.ResourceManager()
  
  ## Append the input WorkFlow object to self.workflows.
  # @param self The object pointer.
  # @param workflow A WorkFlow object.
  def add_workflow(self, workflow):
    self.workflows.append(workflow)
  
  ## Getter for self.resource_manager.
  # @param self The object pointer.
  # @return self.resource_manager
  def get_resource_manager(self):
    return self.resource_manager
  
  ## Remove the input WorkFlow object from self.workflows.
  # @param self The object pointer.
  # @param workflow A WorkFlow object.
  def remove_workflow(self, workflow):
    try:
      self.workflows.remove(workflow)
    except KeyError:
      print("Input WorkFlow object does not exist in current Project.")