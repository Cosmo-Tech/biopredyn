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
  ## @var id_edit
  # A PySide.QtGui.QLineEdit object for editing 'id' attributes.
  ## @var name_edit
  # A PySide.QtGui.QLineEdit object for editing 'name' attributes.
  ## @var layout
  # Layout of 'self', a PySide.QtGui.QFormLayout object.

  ## Constructor.
  # @param self The object pointer.
  # @param parent A biopredyn.ui.tree.TreeElement object.
  def __init__(self, parent):
    QDialog.__init__(self, parent)
    self.id_edit = QLineEdit(self)
    self.name_edit = QLineEdit(self)
    self.layout = QFormLayout(self)
    self.layout.addRow("ID", self.id_edit)
    self.layout.addRow("Name", self.name_edit)
    buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
      self)
    buttons.accepted.connect(self.accept)
    buttons.rejected.connect(self.reject)
    self.setLayout(self.layout)

## DialogBox-derived class for editing biopredyn.ui.tree.ChangeElement objects.
class ChangeBox(DialogBox):
  ## @var change
  # Reference to the biopredyn.change.Change element to be edited by 'self'.

  ## Constructor.
  # @param self The object pointer.
  # @param change A biopredyn.change.Change object.
  # @param parent A biopredyn.ui.tree.ChangeElement object.
  def __init__(self, change, parent):
    DialogBox.__init__(self, parent)
    self.setWindowTitle("Edit change")
    self.change = change
    self.id_edit.set_text(self.change.get_id())
    self.name_edit.set_text(self.change.get_name())

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    self.change.set_id(str(self.id_edit.text()))
    if self.name_edit.text() is not None:
      self.change.set_name(str(self.name_edit.text()))

## DialogBox-derived class for editing biopredyn.ui.tree.DataElement objects.
class DataBox(DialogBox):
  ## @var data
  # Reference to the biopredyn.signals.Data element to be edited by 'self'.

  ## Constructor.
  # @param self The object pointer.
  # @param data A biopredyn.signals.Data object.
  # @param parent A biopredyn.ui.tree.DataElement object.
  def __init__(self, data, parent):
    DialogBox.__init__(self, parent)
    self.setWindowTitle("Edit data")
    self.data = data
    self.id_edit.set_text(self.data.get_id())
    self.name_edit.set_text(self.data.get_name())

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    self.data.set_id(str(self.id_edit.text()))
    if self.name_edit.text() is not None:
      self.data.set_name(str(self.name_edit.text()))

## DialogBox-derived class for editing biopredyn.ui.tree.DataGeneratorElement
## objects.
class DataGeneratorBox(DialogBox):
  ## @var data_gen
  # Reference to the biopredyn.datagenerator.DataGenerator element to be edited
  # by 'self'.

  ## Constructor.
  # @param self The object pointer.
  # @param data_gen A biopredyn.datagenerator.DataGenerator object.
  # @param parent A biopredyn.ui.tree.DataGeneratorElement object.
  def __init__(self, data_gen, parent):
    DialogBox.__init__(self, parent)
    self.setWindowTitle("Edit datagenerator")
    self.data_gen = data_gen
    self.id_edit.set_text(self.data_gen.get_id())
    self.name_edit.set_text(self.data_gen.get_name())

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    self.data_gen.set_id(str(self.id_edit.text()))
    if self.name_edit.text() is not None:
      self.data_gen.set_name(str(self.name_edit.text()))

## DialogBox-derived class for editing biopredyn.ui.tree.ModelElement objects.
class ModelBox(DialogBox):
  ## @var model
  # Reference to the biopredyn.model.Model element to be edited by 'self'.

  ## Constructor.
  # @param self The object pointer.
  # @param model A biopredyn.model.Model object.
  # @param parent A biopredyn.ui.tree.ModelElement object.
  def __init__(self, model, parent):
    DialogBox.__init__(self, parent)
    self.setWindowTitle("Edit model")
    self.model = model
    self.id_edit.set_text(self.model.get_id())
    self.name_edit.set_text(self.model.get_name())

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    self.model.set_id(str(self.id_edit.text()))
    if self.name_edit.text() is not None:
      self.model.set_name(str(self.name_edit.text()))

## DialogBox-derived class for editing biopredyn.ui.tree.OutputElement objects.
class OutputBox(DialogBox):
  ## @var out
  # Reference to the biopredyn.output.Output element to be edited by 'self'.

  ## Constructor.
  # @param self The object pointer.
  # @param out A biopredyn.output.Output object.
  # @param parent A biopredyn.ui.tree.OutputElement object.
  def __init__(self, out, parent):
    DialogBox.__init__(self, parent)
    self.setWindowTitle("Edit output")
    self.out = out
    self.id_edit.set_text(self.out.get_id())
    self.name_edit.set_text(self.out.get_name())

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    self.out.set_id(str(self.id_edit.text()))
    if self.name_edit.text() is not None:
      self.out.set_name(str(self.name_edit.text()))

## DialogBox-derived class for editing biopredyn.ui.tree.ParameterElement
## objects.
class ParameterBox(DialogBox):
  ## @var par
  # Reference to the biopredyn.parameter.Parameter element to be edited by
  # 'self'.

  ## Constructor.
  # @param self The object pointer.
  # @param par A biopredyn.parameter.Parameter object.
  # @param parent A biopredyn.ui.tree.ParameterElement object.
  def __init__(self, data, parent):
    DialogBox.__init__(self, parent)
    self.setWindowTitle("Edit parameter")
    self.par = par
    self.id_edit.set_text(self.par.get_id())
    self.name_edit.set_text(self.par.get_name())

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    self.par.set_id(str(self.id_edit.text()))
    if self.name_edit.text() is not None:
      self.par.set_name(str(self.name_edit.text()))

## DialogBox-derived class for editing biopredyn.ui.tree.RangeElement objects.
class RangeBox(DialogBox):
  ## @var rng
  # Reference to the biopredyn.ranges.Range element to be edited by 'self'.

  ## Constructor.
  # @param self The object pointer.
  # @param rng A biopredyn.range.Range object.
  # @param parent A biopredyn.ui.tree.RangeElement object.
  def __init__(self, rng, parent):
    DialogBox.__init__(self, parent)
    self.setWindowTitle("Edit range")
    self.rng = rng
    self.id_edit.set_text(self.par.get_id())
    self.name_edit.set_text(self.par.get_name())

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    self.rng.set_id(str(self.id_edit.text()))
    if self.name_edit.text() is not None:
      self.rng.set_name(str(self.name_edit.text()))

## DialogBox-derived class for editing biopredyn.ui.tree.SimulationElement
## objects.
class SimulationBox(DialogBox):
  ## @var sim
  # Reference to the biopredyn.simulation.Simulation element to be edited by
  # 'self'.

  ## Constructor.
  # @param self The object pointer.
  # @param sim A biopredyn.simulation.Simulation object.
  # @param parent A biopredyn.ui.tree.SimulationElement object.
  def __init__(self, sim, parent):
    DialogBox.__init__(self, parent)
    self.setWindowTitle("Edit simulation")
    self.sim = sim
    self.id_edit.set_text(self.sim.get_id())
    self.name_edit.set_text(self.sim.get_name())

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    self.sim.set_id(str(self.id_edit.text()))
    if self.name_edit.text() is not None:
      self.sim.set_name(str(self.name_edit.text()))

## DialogBox-derived class for editing biopredyn.ui.tree.SubTaskElement objects.
class SubTaskBox(DialogBox):
  ## @var sub
  # Reference to the biopredyn.task.SubTask element to be edited by 'self'.

  ## Constructor.
  # @param self The object pointer.
  # @param sub A biopredyn.task.SubTask object.
  # @param parent A biopredyn.ui.tree.SubTaskElement object.
  def __init__(self, sub, parent):
    DialogBox.__init__(self, parent)
    self.setWindowTitle("Edit subtask")
    self.sub = sub
    self.id_edit.set_text(self.sub.get_id())
    self.name_edit.set_text(self.sub.get_name())

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    self.sub.set_id(str(self.id_edit.text()))
    if self.name_edit.text() is not None:
      self.sub.set_name(str(self.name_edit.text()))

## DialogBox-derived class for editing biopredyn.ui.tree.TaskElement objects.
class TaskBox(DialogBox):
  ## @var tsk
  # Reference to the biopredyn.task.Task element to be edited by 'self'.

  ## Constructor.
  # @param self The object pointer.
  # @param tsk A biopredyn.task.Task object.
  # @param parent A biopredyn.ui.tree.TaskElement object.
  def __init__(self, tsk, parent):
    DialogBox.__init__(self, parent)
    self.setWindowTitle("Edit task")
    self.tsk = tsk
    self.id_edit.set_text(self.tsk.get_id())
    self.name_edit.set_text(self.tsk.get_name())

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    self.tsk.set_id(str(self.id_edit.text()))
    if self.name_edit.text() is not None:
      self.tsk.set_name(str(self.name_edit.text()))

## DialogBox-derived class for editing biopredyn.ui.tree.VariableElement
## objects.
class VariableBox(DialogBox):
  ## @var var
  # Reference to the biopredyn.variable.Variable element to be edited by 'self'.

  ## Constructor.
  # @param self The object pointer.
  # @param var A biopredyn.variable.Variable object.
  # @param parent A biopredyn.ui.tree.VariableElement object.
  def __init__(self, var, parent):
    DialogBox.__init__(self, parent)
    self.setWindowTitle("Edit variable")
    self.var = var
    self.id_edit.set_text(self.var.get_id())
    self.name_edit.set_text(self.var.get_name())

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    self.var.set_id(str(self.id_edit.text()))
    if self.name_edit.text() is not None:
      self.var.set_name(str(self.name_edit.text()))
