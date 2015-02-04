#!/usr/bin/env python
# coding=utf-8

## @package biopredyn
## Copyright: [2012-2015] The CoSMo Company, All Rights Reserved
## License: BSD 3-Clause

from PySide.QtGui import *
from PySide.QtCore import *
import os
import project

## Class describing the main window for the BioPreDyn user interface.
# Derived from PySide.QtGui.QMainWindow.
class MainWindow(QMainWindow):
  # @var menu_bar
  # @var project
  # @var filename
  # @var save_filename
  # @var hbox

  ## Constructor.
  # @param self The object pointer.
  def __init__(self):
    QMainWindow.__init__(self, None)
    self.filename = None
    self.save_filename = None
    self.setWindowTitle("BioPreDyn UI")
    self.setWindowIcon(QIcon("icons/bpd.xpm"))
    self.setMinimumSize(800, 600)
    self.project = project.Project(self)
    # Menu bar
    self.menu_bar = QMenuBar(self)
    # 'File' menu
    file_menu = QMenu("File", parent=self.menu_bar)
    new_wf_action = QAction("New", self) # connect to new_workflow
    new_wf_action.setShortcut(QKeySequence.New)
    new_wf_action.setStatusTip("Create a new empty work flow.")
    new_wf_action.triggered.connect(self.new_workflow)
    file_menu.addAction(new_wf_action)
    open_wf_action = QAction("Open", self) # connect to open_workflow
    open_wf_action.setShortcut(QKeySequence.Open)
    open_wf_action.setStatusTip("Open a SED-ML work flow.")
    open_wf_action.triggered.connect(self.open_workflow)
    file_menu.addAction(open_wf_action)
    saveas_wf_action = QAction("Save as", self) # connect to save_workflow_as
    saveas_wf_action.setShortcut(QKeySequence.SaveAs)
    saveas_wf_action.setStatusTip("Save current work flow as.")
    saveas_wf_action.triggered.connect(self.save_workflow_as)
    file_menu.addAction(saveas_wf_action)
    save_wf_action = QAction("Save", self) # connect to save_workflow
    save_wf_action.setShortcut(QKeySequence.Save)
    save_wf_action.setStatusTip("Save current work flow.")
    save_wf_action.triggered.connect(self.save_workflow)
    file_menu.addAction(save_wf_action)
    close_wf_action = QAction("Close", self) # connect to close_workflow
    close_wf_action.setShortcut(QKeySequence.Close)
    close_wf_action.setStatusTip("Close current work flow.")
    close_wf_action.triggered.connect(self.close_workflow)
    file_menu.addAction(close_wf_action)
    file_menu.addSeparator()
    run_wf_action = QAction("Run", self) # connect to run_workflow
    run_wf_action.setShortcut("Ctrl+R")
    run_wf_action.setStatusTip("Run all the tasks of the current work flow, " +
      "and process all its outputs.")
    run_wf_action.triggered.connect(self.run_workflow)
    file_menu.addAction(run_wf_action)
    file_menu.addSeparator()
    quit_action = QAction("Quit", self) # connect to close
    quit_action.setShortcut(QKeySequence.Quit)
    quit_action.setStatusTip("Quit the BioPreDyn UI.")
    quit_action.triggered.connect(self.close)
    file_menu.addAction(quit_action)
    self.menu_bar.addMenu(file_menu)
    self.setMenuBar(self.menu_bar)
    # Central widget
    self.setCentralWidget(self.project)
    # Status bar
    self.status_bar = QStatusBar(parent=self)
    self.setStatusBar(self.status_bar)

  ## Closes the active workflow.
  # @param self The object pointer.
  def close_workflow(self):
    self.project.remove_workflow()

  ## Creates a new workflow.
  # @param self The object pointer.
  def new_workflow(self):
    self.project.new_workflow()

  ## Opens a workflow from a user-defined source file.
  # Opens a dialog window asking for the location of a SED-ML file; if a valid
  # SED-ML file location is provided by the user, it is opened.
  # @param self The object pointer.
  def open_workflow(self):
    dir = (os.path.dirname(self.filename)
      if self.filename is not None else ".")
    fname = QFileDialog.getOpenFileName(
      self, "Open SED-ML file", dir, "XML file (*.xml)")
    self.filename = fname[0]
    self.project.add_workflow(self.filename)

  ## Runs the active workflow.
  # @param self The object pointer.
  def run_workflow(self):
    self.project.run_workflow()

  ## Saves the active workflow to the location defined by its 'source'
  ## attribute.
  # @param self The object pointer.
  def save_workflow(self):
    self.project.write_workflow()

  ## Saves the active workflow to a user-defined location.
  # Opens a dialog window asking for the location of a SED-ML file; if a valid
  # SED-ML file location is provided by the user, it is opened.
  # @param self The object pointer.
  def save_workflow_as(self):
    dir = (os.path.dirname(self.save_filename)
      if self.save_filename is not None else ".")
    fname = QFileDialog.getSaveFileName(
      self, "Save SED-ML file", dir, "XML file (*.xml)")
    self.save_filename = fname[0]
    self.project.write_workflow(source=self.save_filename)
