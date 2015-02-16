#!/usr/bin/env python
# coding=utf-8

## @package biopredyn
## Copyright: [2012-2015] The CoSMo Company, All Rights Reserved
## License: BSD 3-Clause

from PySide.QtGui import *
import tree

## PySide.QtGui.QTreeWidget-derived class for exploring SED-ML work flows.
class NavigationTree(QTreeWidget):

  ## Constructor.
  # @param self The object pointer.
  # @param parent A biopredyn.ui.project.Project object.
  def __init__(self, parent):
    QTreeWidget.__init__(self, parent)
    labels = ['Element', 'ID']
    self.setHeaderLabels(labels)
    self.setMinimumWidth(200)

  ## Creates a new biopredyn.ui.tree.WorkFlowElement with 'self' as parent.
  # @param self The object pointer.
  # @param workflow A biopredyn.workflow.WorkFlow element.
  def add_workflow(self, workflow):
    wf = tree.WorkFlowElement(self, workflow)
    self.invisibleRootItem().addChild(wf)
    wf.setExpanded(True)

  ## Opens a biopredyn.ui.DialogBox window providing several widgets for editing
  ## the current element of 'self', if editable.
  # @param self The object pointer.
  def edit_element(self):
    elt = self.currentItem()
    if elt.is_editable():
      elt.edit()

  ## Removes the input 'item' from 'self'.
  # @param self The object pointer.
  # @param item A biopredyn.ui.tree.TreeElement object.
  def remove_item(self, item):
    self.invisibleRootItem().removeChild(item)
