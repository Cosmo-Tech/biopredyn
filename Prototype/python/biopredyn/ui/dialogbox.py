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
    self.id_edit = QLineEdit(self)
    self.name_edit = QLineEdit(self)
    self.layout = QFormLayout(self)
    self.layout.addRow("ID", self.id_edit)
    self.layout.addRow("Name", self.name_edit)
    self.buttons = QDialogButtonBox(
      QDialogButtonBox.Ok | QDialogButtonBox.Cancel, parent=self)
    self.buttons.accepted.connect(self.accept)
    self.buttons.rejected.connect(self.reject)
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
    self.layout.addRow(self.buttons)

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
    self.layout.addRow(self.buttons)

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
    self.layout.addRow(self.buttons)

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

  ## Constructor.
  # @param self The object pointer.
  # @param model A biopredyn.model.Model object.
  def __init__(self, model):
    DialogBox.__init__(self)
    self.setWindowTitle("Edit model")
    self.model = model
    self.id_edit.setText(self.model.get_id())
    self.name_edit.setText(self.model.get_name())
    self.layout.addRow(self.buttons)

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    self.model.set_id(str(self.id_edit.text()))
    if self.name_edit.text() is not None:
      self.model.set_name(str(self.name_edit.text()))
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
    self.layout.addRow(self.buttons)

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
    # add 'Value' field
    self.name_edit.setText(self.par.get_name())
    self.value_edit = QLineEdit(self)
    self.value_edit.setValidator(QDoubleValidator())
    self.layout.addRow("Value", self.value_edit)
    self.value_edit.setText(str(self.par.get_value()))
    # add self.buttons
    self.layout.addRow(self.buttons)

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
    self.layout.addRow(self.buttons)

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

  ## Constructor.
  # @param self The object pointer.
  # @param sim A biopredyn.simulation.Simulation object.
  def __init__(self, sim):
    DialogBox.__init__(self)
    self.setWindowTitle("Edit simulation")
    self.sim = sim
    self.id_edit.setText(self.sim.get_id())
    self.name_edit.setText(self.sim.get_name())
    self.layout.addRow(self.buttons)

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    self.sim.set_id(str(self.id_edit.text()))
    if self.name_edit.text() is not None:
      self.sim.set_name(str(self.name_edit.text()))
    self.done(QDialog.Accepted)

## DialogBox-derived class for editing biopredyn.ui.tree.SubTaskElement objects.
class SubTaskBox(DialogBox):
  ## @var sub
  # Reference to the biopredyn.task.SubTask element to be edited by 'self'.

  ## Constructor.
  # @param self The object pointer.
  # @param sub A biopredyn.task.SubTask object.
  def __init__(self, sub):
    DialogBox.__init__(self)
    self.setWindowTitle("Edit subtask")
    self.sub = sub
    self.id_edit.setText(self.sub.get_task_id())
    self.order_edit = QLineEdit(self)
    self.order_edit.setValidator(QIntValidator())
    self.layout.addRow("Order", self.order_edit)
    self.order_edit.setText(str(self.sub.get_order()))
    # add self.buttons
    self.layout.addRow(self.buttons)

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    try:
      self.sub.set_task_id(str(self.id_edit.text()))
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
    self.layout.addRow(self.buttons)

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
    self.layout.addRow(self.buttons)

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    self.var.set_id(str(self.id_edit.text()))
    if self.name_edit.text() is not None:
      self.var.set_name(str(self.name_edit.text()))
    self.done(QDialog.Accepted)
