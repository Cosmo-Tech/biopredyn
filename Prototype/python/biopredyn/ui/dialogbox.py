#!/usr/bin/env python
# coding=utf-8

## @package biopredyn
## Copyright: [2012-2015] The CoSMo Company, All Rights Reserved
## License: BSD 3-Clause

import os
from PySide.QtGui import *

## Base class for SED-ML element dialog box.
# This widget proposes several objects for editing the content of an element of
# the current workflow.
class DialogBox(QDialog):
  ## @var buttons
  # An instance of PySide.QtGui.QDialogButtonBox providing standard 'Ok' and
  # 'Cancel' buttons.
  ## @var id_edit
  # A PySide.QtGui.QLineEdit object for editing 'id' attributes.
  ## @var name_edit
  # A PySide.QtGui.QLineEdit object for editing 'name' attributes.
  ## @var layout
  # Layout of 'self', a PySide.QtGui.QFormLayout object.

  ## Constructor.
  # @param self The object pointer.
  def __init__(self):
    QDialog.__init__(self)
    # main layout: vertical grid
    self.layout = QGridLayout(self)
    # upper layout: displays widgets for editing 'name' and 'ID' attributes,
    # common to (almost) all dialog boxes
    self.up_layout = QFormLayout()
    self.id_edit = QLineEdit(self)
    self.name_edit = QLineEdit(self)
    self.up_layout.addRow("ID", self.id_edit)
    self.up_layout.addRow("Name", self.name_edit)
    self.layout.addLayout(self.up_layout, 0, 0)
    # lower layout: displays widgets depending on the nature of the dialog box
    self.low_layout = QFormLayout()
    self.layout.addLayout(self.low_layout, 1, 0)
    # buttons: standard 'ok' and 'cancel' buttons at the bottom of the dialog
    self.buttons = QDialogButtonBox(
      QDialogButtonBox.Ok | QDialogButtonBox.Cancel, parent=self)
    self.buttons.accepted.connect(self.accept)
    self.buttons.rejected.connect(self.reject)
    self.layout.addWidget(self.buttons, 2, 0)
    self.setLayout(self.layout)

## DialogBox-derived class for editing biopredyn.ui.tree.ChangeElement objects.
class ChangeBox(DialogBox):
  ## @var change
  # Reference to the biopredyn.change.Change element to be edited by 'self'.

  ## Constructor.
  # @param self The object pointer.
  # @param change A biopredyn.change.Change object.
  def __init__(self, change):
    DialogBox.__init__(self)
    self.setWindowTitle("Edit change")
    self.change = change
    self.id_edit.setText(self.change.get_id())
    self.name_edit.setText(self.change.get_name())

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    self.change.set_id(str(self.id_edit.text()))
    if self.name_edit.text() is not None:
      self.change.set_name(str(self.name_edit.text()))
    self.done(QDialog.Accepted)

## DialogBox-derived class for editing biopredyn.ui.tree.DataElement objects.
class DataBox(DialogBox):
  ## @var data
  # Reference to the biopredyn.signals.Data element to be edited by 'self'.

  ## Constructor.
  # @param self The object pointer.
  # @param data A biopredyn.signals.Data object.
  def __init__(self, data):
    DialogBox.__init__(self)
    self.setWindowTitle("Edit data")
    self.data = data
    self.id_edit.setText(self.data.get_id())
    self.name_edit.setText(self.data.get_name())

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    self.data.set_id(str(self.id_edit.text()))
    if self.name_edit.text() is not None:
      self.data.set_name(str(self.name_edit.text()))
    self.done(QDialog.Accepted)

## DialogBox-derived class for editing biopredyn.ui.tree.DataGeneratorElement
## objects.
class DataGeneratorBox(DialogBox):
  ## @var data_gen
  # Reference to the biopredyn.datagenerator.DataGenerator element to be edited
  # by 'self'.

  ## Constructor.
  # @param self The object pointer.
  # @param data_gen A biopredyn.datagenerator.DataGenerator object.
  def __init__(self, data_gen):
    DialogBox.__init__(self)
    self.setWindowTitle("Edit datagenerator")
    self.data_gen = data_gen
    self.id_edit.setText(self.data_gen.get_id())
    self.name_edit.setText(self.data_gen.get_name())

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    self.data_gen.set_id(str(self.id_edit.text()))
    if self.name_edit.text() is not None:
      self.data_gen.set_name(str(self.name_edit.text()))
    self.done(QDialog.Accepted)

## DialogBox-derived class for editing biopredyn.ui.tree.ModelElement objects.
class ModelBox(DialogBox):
  ## @var model
  # Reference to the biopredyn.model.Model element to be edited by 'self'.
  ## @var lng_edit
  # An instance of PySide.QtGui.QLineEdit for editing the 'language' attribute
  # of self.model.
  ## @var source_edit
  # An instance of PySide.QtGui.QLineEdit for editing the 'value' attribute of
  # self.model.

  ## Constructor.
  # @param self The object pointer.
  # @param model A biopredyn.model.Model object.
  def __init__(self, model):
    DialogBox.__init__(self)
    self.setWindowTitle("Edit model")
    self.model = model
    self.id_edit.setText(self.model.get_id())
    self.name_edit.setText(self.model.get_name())
    # 'Language' field
    self.lng_edit = QLineEdit(self)
    self.low_layout.addRow("Language", self.lng_edit)
    self.lng_edit.setText(str(self.model.get_language()))
    # 'Source' field
    self.source_edit = QLineEdit(self)
    self.low_layout.addRow("Source", self.source_edit)
    self.source_edit.setText(str(self.model.get_source()))

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    self.model.set_id(str(self.id_edit.text()))
    self.model.set_source(str(self.source_edit.text()))
    if self.name_edit.text() is not None:
      self.model.set_name(str(self.name_edit.text()))
    if self.lng_edit.text() is not None:
      self.model.set_language(str(self.lng_edit.text()))
    self.done(QDialog.Accepted)

## DialogBox-derived class for editing biopredyn.ui.tree.OutputElement objects.
class OutputBox(DialogBox):
  ## @var out
  # Reference to the biopredyn.output.Output element to be edited by 'self'.

  ## Constructor.
  # @param self The object pointer.
  # @param out A biopredyn.output.Output object.
  def __init__(self, out):
    DialogBox.__init__(self)
    self.setWindowTitle("Edit output")
    self.out = out
    self.id_edit.setText(self.out.get_id())
    self.name_edit.setText(self.out.get_name())

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    self.out.set_id(str(self.id_edit.text()))
    if self.name_edit.text() is not None:
      self.out.set_name(str(self.name_edit.text()))
    self.done(QDialog.Accepted)

## DialogBox-derived class for editing biopredyn.ui.tree.ParameterElement
## objects.
class ParameterBox(DialogBox):
  ## @var par
  # Reference to the biopredyn.parameter.Parameter element to be edited by
  # 'self'.
  ## @var value_edit
  # An instance of PySide.QtGui.QLineEdit for editing 'value' attribute of
  # self.par.

  ## Constructor.
  # @param self The object pointer.
  # @param par A biopredyn.parameter.Parameter object.
  def __init__(self, par):
    DialogBox.__init__(self)
    self.setWindowTitle("Edit parameter")
    self.par = par
    self.id_edit.setText(self.par.get_id())
    self.name_edit.setText(self.par.get_name())
    # add 'Value' field
    self.value_edit = QLineEdit(self)
    self.value_edit.setValidator(QDoubleValidator())
    self.low_layout.addRow("Value", self.value_edit)
    self.value_edit.setText(str(self.par.get_value()))

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    try:
      self.par.set_id(str(self.id_edit.text()))
      self.par.set_value(float(self.value_edit.text()))
      if self.name_edit.text() is not None:
        self.par.set_name(str(self.name_edit.text()))
      self.done(QDialog.Accepted)
    except ValueError:
      self.value_edit.setStyleSheet("background: #FFB2B2")

## DialogBox-derived class for editing biopredyn.ui.tree.RangeElement objects.
class RangeBox(DialogBox):
  ## @var rng
  # Reference to the biopredyn.ranges.Range element to be edited by 'self'.

  ## Constructor.
  # @param self The object pointer.
  # @param rng A biopredyn.range.Range object.
  def __init__(self, rng):
    DialogBox.__init__(self)
    self.setWindowTitle("Edit range")
    self.rng = rng
    self.id_edit.setText(self.rng.get_id())
    self.name_edit.setText(self.rng.get_name())

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    self.rng.set_id(str(self.id_edit.text()))
    if self.name_edit.text() is not None:
      self.rng.set_name(str(self.name_edit.text()))
    self.done(QDialog.Accepted)

## DialogBox-derived class for editing biopredyn.ui.tree.SimulationElement
## objects.
class SimulationBox(DialogBox):
  ## @var sim
  # Reference to the biopredyn.simulation.Simulation element to be edited by
  # 'self'.
  ## @var typ_box
  # A PySide.QtGui.QComboBox object for editing the 'type' attribute of
  # self.sim; possible values are 'uniformTimeCourse', 'steadyState' and
  # 'oneStep'.
  ## @var utc_layout
  # A PySide.QtGui.QFormLayout object providing widgets for editing self.sim in
  # case it is a biopredyn.UniformTimeCourse object.
  ## @var step_layout
  # A PySide.QtGui.QFormLayout object providing widgets for editing self.sim in
  # case it is a biopredyn.OneStep object.
  ## @var start_edit
  # A PySide.QtGui.QLineEdit object for editing the 'initial_time' attribute of
  # self.sim (UniformTimeCourse case).
  ## @var end_edit
  # A PySide.QtGui.QLineEdit object for editing the 'output_end_time' attribute
  # of self.sim (UniformTimeCourse case).
  ## @var pts_edit
  # A PySide.QtGui.QLineEdit object for editing the 'number_of_points' attribute
  # of self.sim (UniformTimeCourse case).
  ## @var out_st_edit
  # A PySide.QtGui.QLineEdit object for editing the 'output_start_time'
  # attribute of self.sim (UniformTimeCourse case).

  ## Constructor.
  # @param self The object pointer.
  # @param sim A biopredyn.simulation.Simulation object; optional (default:
  # None).
  def __init__(self, sim=None):
    DialogBox.__init__(self)
    self.setWindowTitle("Edit simulation")
    # 'Type' combo box
    types = ['uniformTimeCourse', 'steadyState', 'oneStep']
    self.typ_box = QComboBox()
    self.typ_box.addItems(types)
    self.up_layout.addRow("Type", self.typ_box)
    # layout for uniformTimeCourse case
    self.utc_layout = QFormLayout()
    self.start_edit = QLineEdit()
    self.start_edit.setValidator(QDoubleValidator())
    self.utc_layout.addRow("Start time", self.start_edit)
    self.end_edit = QLineEdit()
    self.end_edit.setValidator(QDoubleValidator())
    self.utc_layout.addRow("End time", self.end_edit)
    self.out_st_edit = QLineEdit()
    self.out_st_edit.setValidator(QDoubleValidator())
    self.utc_layout.addRow("Output start time", self.out_st_edit)
    self.pts_edit = QLineEdit()
    self.pts_edit.setValidator(QIntValidator())
    self.utc_layout.addRow("Number of points", self.pts_edit)
    # layout for oneStep case
    self.step_layout = QFormLayout()
    self.step_edit = QLineEdit()
    self.step_edit.setValidator(QDoubleValidator())
    self.step_layout.addRow("Step", self.step_edit)
    if sim is not None:
      self.sim = sim
      self.id_edit.setText(self.sim.get_id())
      self.name_edit.setText(self.sim.get_name())
      self.typ_box.setCurrentIndex(types.index(self.sim.get_type()))
      self.typ_box.setDisabled(True)
      if (self.typ_box.currentText() == 'uniformTimeCourse'):
        self.start_edit.setText(str(self.sim.get_initial_time()))
        self.end_edit.setText(str(self.sim.get_output_end_time()))
        self.out_st_edit.setText(str(self.sim.get_output_start_time()))
        self.pts_edit.setText(str(self.sim.get_number_of_points()))
      elif (self.typ_box.currentText() == 'oneStep'):
        self.step_edit.setText(str(self.sim.get_step()))
      self.update_layout()
    # catch and process currentIndexChanged signal
    self.typ_box.currentIndexChanged.connect(self.update_layout)

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    if self.sim is not None:
      self.sim.set_id(str(self.id_edit.text()))
      if self.name_edit.text() is not None:
        self.sim.set_name(str(self.name_edit.text()))
      if (self.sim.get_type() == 'uniformTimeCourse'):
        self.sim.set_initial_time(float(self.start_edit.text()))
        self.sim.set_output_end_time(float(self.end_edit.text()))
        self.sim.set_output_start_time(float(self.out_st_edit.text()))
        self.sim.set_number_of_points(int(self.pts_edit.text()))
      elif (self.sim.get_type() == 'oneStep'):
        self.sim.set_step(float(self.step_edit.text()))
    self.done(QDialog.Accepted)

  ## Adapt self.layout depending on the current text in self.typ_box.
  # @param self The object pointer.
  def update_layout(self):
    if (self.typ_box.currentText() == 'uniformTimeCourse'):
      self.layout.addLayout(self.utc_layout, 1, 0)
    elif (self.typ_box.currentText() == 'oneStep'):
      self.layout.addLayout(self.step_layout, 1, 0)

## DialogBox-derived class for editing biopredyn.ui.tree.SubTaskElement objects.
class SubTaskBox(DialogBox):
  ## @var sub
  # Reference to the biopredyn.task.SubTask element to be edited by 'self'.
  ## @var order_edit
  # A PySide.QtGui.QLineEdit object for editing the 'order' attribute of
  # self.sub.
  ## @var tsk_id_edit
  # A PySide.QtGui.QLineEdit object for editing the 'task_id' attribute of
  # self.sub.

  ## Constructor.
  # @param self The object pointer.
  # @param sub A biopredyn.task.SubTask object.
  def __init__(self, sub):
    DialogBox.__init__(self)
    self.setWindowTitle("Edit subtask")
    self.sub = sub
    self.tsk_id_edit = QLineEdit(self)
    self.tsk_id_edit.setText(str(self.sub.get_task_id()))
    self.low_layout.addRow("Task ID", self.tsk_id_edit)
    self.order_edit = QLineEdit(self)
    self.order_edit.setText(str(self.sub.get_order()))
    self.order_edit.setValidator(QIntValidator())
    self.low_layout.addRow("Order", self.order_edit)
    # remove widgets from upper layout since self.sub does not have a 'name' nor
    # an 'id' attribute
    for i in reversed(range(self.up_layout.count())): 
      self.up_layout.itemAt(i).widget().setParent(None)

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    try:
      self.sub.set_task_id(str(self.tsk_id_edit.text()))
      self.sub.set_order(int(self.order_edit.text()))
      self.done(QDialog.Accepted)
    except ValueError:
      self.order_edit.setStyleSheet("background: #FFB2B2")

## DialogBox-derived class for editing biopredyn.ui.tree.TaskElement objects.
class TaskBox(DialogBox):
  ## @var tsk
  # Reference to the biopredyn.task.Task element to be edited by 'self'.

  ## Constructor.
  # @param self The object pointer.
  # @param tsk A biopredyn.task.Task object.
  def __init__(self, tsk):
    DialogBox.__init__(self)
    self.setWindowTitle("Edit task")
    self.tsk = tsk
    self.id_edit.setText(self.tsk.get_id())
    self.name_edit.setText(self.tsk.get_name())

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    self.tsk.set_id(str(self.id_edit.text()))
    if self.name_edit.text() is not None:
      self.tsk.set_name(str(self.name_edit.text()))
    self.done(QDialog.Accepted)

## DialogBox-derived class for editing biopredyn.ui.tree.VariableElement
## objects.
class VariableBox(DialogBox):
  ## @var var
  # Reference to the biopredyn.variable.Variable element to be edited by 'self'.

  ## Constructor.
  # @param self The object pointer.
  # @param var A biopredyn.variable.Variable object.
  def __init__(self, var):
    DialogBox.__init__(self)
    self.setWindowTitle("Edit variable")
    self.var = var
    self.id_edit.setText(self.var.get_id())
    self.name_edit.setText(self.var.get_name())

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    self.var.set_id(str(self.id_edit.text()))
    if self.name_edit.text() is not None:
      self.var.set_name(str(self.name_edit.text()))
    self.done(QDialog.Accepted)
