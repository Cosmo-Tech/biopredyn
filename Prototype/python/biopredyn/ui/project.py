#!/usr/bin/env python
# coding=utf-8

## @package biopredyn
## Copyright: [2012-2015] The CoSMo Company, All Rights Reserved
## License: BSD 3-Clause

from PySide.QtGui import *
import navigationtree, tabpanel
from .. import resources, workflow

## QSplitter-derived class for handling projects in BioPreDyn user interface.
class Project(QSplitter):
  ## @var resource_manager
  # A biopredyn.resources.ResourceManager object.
  ## @var nav_tree
  # A biopredyn.ui.navigationtree.NavigationTree object.
  ## @var tab_panel
  # A biopredyn.ui.tabpanel.TabPanel object.
  
  ## Constructor.
  # @param self The object pointer.
  # @param parent A biopredyn.ui.mainwindow.MainWindow object.
  def __init__(self, parent):
    QSplitter.__init__(self, parent)
    self.resource_manager = resources.ResourceManager()
    self.nav_tree = navigationtree.NavigationTree(parent)
    self.tab_panel = tabpanel.TabPanel(parent)
    self.addWidget(self.nav_tree)
    self.addWidget(self.tab_panel)
    self.setCollapsible(0, False)
    self.setCollapsible(1, False)
    sizes = [250, 550]
    self.setSizes(sizes)
  
  ## Create a new biopredyn.workflow.WorkFlow object from the input 'source' and
  ## adds it to self.nav_tree.
  # @param self The object pointer.
  # @param source Complete filename of a valid SED-ML workflow.
  def add_workflow(self, source):
    wf = workflow.WorkFlow(self.resource_manager, source=source)
    self.nav_tree.add_workflow(wf)
  
  ## Getter for self.resource_manager.
  # @param self The object pointer.
  # @return self.resource_manager
  def get_resource_manager(self):
    return self.resource_manager
  
  ## Getter for self.nav_tree.
  # @param self The object pointer.
  # @return self.nav_tree
  def get_nav_tree(self):
    return self.nav_tree
  
  ## Getter for self.tab_panel.
  # @param self The object pointer.
  # @return self.tab_panel
  def get_tab_panel(self):
    return self.tab_panel
  
  ## Create a new biopredyn.workflow.WorkFlow object and adds it to
  ## self.nav_tree.
  # @param self The object pointer.
  def new_workflow(self):
    wf = workflow.WorkFlow(self.resource_manager)
    self.nav_tree.add_workflow(wf)
  
  ## Remove the active workflow from self.nav_tree.
  # @param self The object pointer.
  def remove_workflow(self):
    self.nav_tree.remove_item(
      self.nav_tree.currentItem().get_workflow_element())
  
  ## Runs the active workflow i.e. runs its tasks, then process its outputs.
  # @param self The object pointer.
  def run_workflow(self):
    self.nav_tree.currentItem().get_workflow_element().run()
  
  ## Writes the active workflow to the input location 'source' as a SED-ML
  ## file.
  # @param self The object pointer.
  # @param source Where to write the active workflow; optional. If not
  # specified, the 'source' attribute of the active workflow is used. 
  def write_workflow(self, source=None):
    print("TODO") # TODO
