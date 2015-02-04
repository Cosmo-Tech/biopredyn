#!/usr/bin/env python
# coding=utf-8

## @package biopredyn
## Copyright: [2012-2015] The CoSMo Company, All Rights Reserved
## License: BSD 3-Clause

import os
from PySide.QtGui import *

## Base class for SED-ML elements in parent
## biopredyn.ui.navigationtree.NavigationTree object. Derived from
## PySide.QtGui.QTreeWidgetItem.
class TreeElement(QTreeWidgetItem):

  ## Constructor.
  # @param self The object pointer.
  # @param parent A PySide.QtGui.QWidget object.
  def __init__(self, parent):
    QTreeWidgetItem.__init__(self, parent)

  ## Recursively browses the parents of 'self' until a
  ## biopredyn.ui.tree.WorkFlowElement is reached, then returns it.
  # @param self The object pointer.
  # @return The top-level biopredyn.ui.tree.WorkFlowElement parent of'self'.
  def get_workflow_element(self):
    return self.parent().get_workflow_element()

## TreeElement-derived class representing biopredyn.workflow.WorkFlow objects in
## parent biopredyn.ui.navigationtree.NavigationTree object.
class WorkFlowElement(TreeElement):
  ## @var workflow
  # Reference to the biopredyn.workflow.WorkFlow represented by self.
  ## @var sim_list
  # A biopredyn.ui.tree.TreeElement object for listing simulations.
  ## @var model_list
  # A biopredyn.ui.tree.TreeElement object for listing models.
  ## @var task_list
  # A biopredyn.ui.tree.TreeElement object for listing tasks.
  ## @var datagen_list
  # A biopredyn.ui.tree.TreeElement object for listing data generators.
  ## @var out_list
  # A biopredyn.ui.tree.TreeElement object for listing outputs.

  ## Overriden constructor.
  # @param self The object pointer.
  # @param parent A biopredyn.ui.navigationtree.NavigationTree object.
  # @param workflow A biopredyn.workflow.WorkFlow object.
  def __init__(self, parent, workflow):
    TreeElement.__init__(self, parent)
    self.workflow = workflow
    self.setText(0, os.path.split(self.workflow.get_source())[1])
    # Build child tree lists
    self.sim_list = TreeElement(self)
    self.sim_list.setText(0, 'listOfSimulations')
    self.addChild(self.sim_list)
    self.model_list = TreeElement(self)
    self.model_list.setText(0, 'listOfModels')
    self.addChild(self.model_list)
    self.task_list = TreeElement(self)
    self.task_list.setText(0, 'listOfTasks')
    self.addChild(self.task_list)
    self.datagen_list = TreeElement(self)
    self.datagen_list.setText(0, 'listOfDataGenerators')
    self.addChild(self.datagen_list)
    self.out_list = TreeElement(self)
    self.out_list.setText(0, 'listOfOutputs')
    self.addChild(self.out_list)

  ## Overriden. Returns 'self'.
  # @param self The object pointer.
  # @return self
  def get_workflow_element(self):
    return self

  ## Runs the tasks of self.workflow, and processes its outputs.
  # @param self The object pointer.
  def run(self):
    self.workflow.run_tasks()
    self.workflow.process_outputs()
