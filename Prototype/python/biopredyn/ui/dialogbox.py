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
  # Layout of 'self', a PySide.QtGui.QGridLayout object.
  ## @var up_layout
  # Upper layout of 'self', a PySide.QtGui.QFormLayout object.
  ## @var mid_layout
  # Central layout of 'self', a PySide.QtGui.QStackedLayout object.

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
    # middle layout: displays widgets depending on the nature of the dialog box
    self.mid_layout = QStackedLayout()
    self.layout.addLayout(self.mid_layout, 1, 0)
    # buttons: standard 'ok' and 'cancel' buttons at the bottom of the dialog
    self.buttons = QDialogButtonBox(
      QDialogButtonBox.Ok | QDialogButtonBox.Cancel, parent=self)
    self.buttons.accepted.connect(self.accept)
    self.buttons.rejected.connect(self.reject)
    self.layout.addWidget(self.buttons, 2, 0)
    self.setLayout(self.layout)

## DialogBox-derived class for editing biopredyn.ui.tree.ChangeElement objects.
class ChangeBox(DialogBox):
  ## @var ax_wid
  # A PySide.QtGui.QWidget object providing widgets for editing self.change in
  # case it is a biopredyn.change.addXML object.
  ## @var ca_wid
  # A PySide.QtGui.QWidget object providing widgets for editing self.change in
  # case it is a biopredyn.change.changeAttribute object.
  ## @var cc_wid
  # A PySide.QtGui.QWidget object providing widgets for editing self.change in
  # case it is a biopredyn.change.computeChange object.
  ## @var change
  # Reference to the biopredyn.change.Change element to be edited by 'self'.
  ## @var cx_wid
  # A PySide.QtGui.QWidget object providing widgets for editing self.change in
  # case it is a biopredyn.change.changeXML object.
  ## @var mth_edit
  # A PySide.QtGui.QLineEdit object for editing the 'math' attribute of
  # self.change ('computeChange' case).
  ## @var rx_wid
  # A PySide.QtGui.QWidget object providing widgets for editing self.change in
  # case it is a biopredyn.change.removeXML object.
  ## @var tgt_edit
  # A PySide.QtGui.QLineEdit object for editing the 'target' attribute of
  # self.change.
  ## @var typ_box
  # A PySide.QtGui.QComboBox object for editing the 'type' attribute of
  # self.change; possible values are 'computeChange', 'changeAttribute',
  # 'changeXML', 'addXML' and 'removeXML'.
  ## @var val_edit
  # A PySide.QtGui.QLineEdit object for editing the 'value' attribute of
  # self.change ('changeAttribute' case).
  ## @var xml_edit
  # A PySide.QtGui.QLineEdit object for editing the 'xml' attribute of
  # self.change ('addXML' and 'changeXML' cases).

  ## Constructor.
  # @param self The object pointer.
  # @param change A biopredyn.change.Change object; optional (default: None).
  def __init__(self, change=None):
    DialogBox.__init__(self)
    self.setWindowTitle("Edit change")
    # 'target' editor - common to all types
    self.tgt_edit = QLineEdit()
    self.up_layout.addRow("Target", self.tgt_edit)
    # 'type' combo box
    types = ['computeChange', 'changeAttribute', 'addXML', 'changeXML',
      'removeXML']
    self.typ_box = QComboBox()
    self.typ_box.addItems(types)
    self.up_layout.addRow("Type", self.typ_box)
    # 'computeChange' widget
    self.cc_wid = QWidget()
    cc_lay = QFormLayout(self.cc_wid)
    self.mth_edit = QLineEdit()
    cc_lay.addRow("Math", self.mth_edit)
    self.mid_layout.addWidget(self.cc_wid)
    # 'changeAttribute' widget
    self.ca_wid = QWidget()
    ca_lay = QFormLayout(self.ca_wid)
    self.val_edit = QLineEdit()
    ca_lay.addRow("Value", self.val_edit)
    self.mid_layout.addWidget(self.ca_wid)
    # 'addXML' widget
    self.ax_wid = QWidget()
    ax_lay = QFormLayout(self.ax_wid)
    self.xml_edit = QLineEdit()
    ax_lay.addRow("XML", self.xml_edit)
    self.mid_layout.addWidget(self.ax_wid)
    # 'changeXML' widget
    self.cx_wid = QWidget()
    cx_lay = QFormLayout(self.cx_wid)
    self.xml_edit = QLineEdit()
    cx_lay.addRow("XML", self.xml_edit)
    self.mid_layout.addWidget(self.cx_wid)
    # 'removeXML' widget
    self.rx_wid = QWidget()
    rx_lay = QFormLayout(self.rx_wid)
    self.mid_layout.addWidget(self.rx_wid)
    if change is not None:
      self.change = change
      self.id_edit.setText(self.change.get_id())
      self.name_edit.setText(self.change.get_name())
      self.tgt_edit.setText(str(self.change.get_target()))
      self.typ_box.setCurrentIndex(types.index(self.change.get_type()))
      self.typ_box.setDisabled(True)
      if self.change.get_type() == 'computeChange':
        self.mth_edit.setText(str(self.change.get_math()))
      elif self.change.get_type() == 'changeAttribute':
        self.val_edit.setText(self.change.get_value())
      elif (self.change.get_type() == 'addXML' or
        self.change.get_type() == 'changeXML'):
        self.xml_edit.setText(self.change.get_xml())
      self.update_layout()
    # catch and process currentIndexChanged signal
    self.typ_box.currentIndexChanged.connect(self.update_layout)

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    self.change.set_id(str(self.id_edit.text()))
    self.change.set_target(str(self.tgt_edit.text()))
    if self.name_edit.text() is not None:
      self.change.set_name(str(self.name_edit.text()))
    if (self.change.get_type() == 'computeChange'):
      self.change.set_math(str(self.mth_edit.text()))
    elif (self.change.get_type() == 'changeAttribute'):
      self.change.set_value(str(self.val_edit.text()))
    elif (self.change.get_type() == 'addXML'):
      self.change.set_xml(str(self.xml_edit.text()))
    elif (self.change.get_type() == 'changeXML'):
      self.change.set_xml(str(self.xml_edit.text()))
    self.done(QDialog.Accepted)

  ## Adapt self.mid_layout depending on the current text in self.typ_box.
  # @param self The object pointer.
  def update_layout(self):
    if (self.typ_box.currentText() == 'computeChange'):
      self.mid_layout.setCurrentWidget(self.cc_wid)
    elif (self.typ_box.currentText() == 'changeAttribute'):
      self.mid_layout.setCurrentWidget(self.ca_wid)
    elif (self.typ_box.currentText() == 'addXML'):
      self.mid_layout.setCurrentWidget(self.ax_wid)
    elif (self.typ_box.currentText() == 'changeXML'):
      self.mid_layout.setCurrentWidget(self.cx_wid)
    elif (self.typ_box.currentText() == 'removeXML'):
      self.mid_layout.setCurrentWidget(self.rx_wid)

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
    wid = QWidget()
    lay = QFormLayout(wid)
    # 'Language' field
    self.lng_edit = QLineEdit(self)
    lay.addRow("Language", self.lng_edit)
    self.lng_edit.setText(str(self.model.get_language()))
    # 'Source' field
    self.source_edit = QLineEdit(self)
    lay.addRow("Source", self.source_edit)
    self.source_edit.setText(str(self.model.get_source()))
    self.mid_layout.addWidget(wid)

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
    wid = QWidget()
    lay = QFormLayout(wid)
    # add 'Value' field
    self.value_edit = QLineEdit(self)
    self.value_edit.setValidator(QDoubleValidator())
    lay.addRow("Value", self.value_edit)
    self.value_edit.setText(str(self.par.get_value()))
    self.mid_layout.addWidget(wid)

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
  ## @var utc_wid
  # A PySide.QtGui.QWidget object providing widgets for editing self.sim in
  # case it is a biopredyn.UniformTimeCourse object.
  ## @var one_wid
  # A PySide.QtGui.QWidget object providing widgets for editing self.sim in
  # case it is a biopredyn.OneStep object.
  ## @var std_wid
  # A PySide.QtGui.QWidget object providing widgets for editing self.sim in
  # case it is a biopredyn.SteadyState object.
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
    # widget for uniformTimeCourse case
    self.utc_wid = QWidget()
    utc_lay = QFormLayout(self.utc_wid)
    self.start_edit = QLineEdit()
    self.start_edit.setValidator(QDoubleValidator())
    utc_lay.addRow("Start time", self.start_edit)
    self.end_edit = QLineEdit()
    self.end_edit.setValidator(QDoubleValidator())
    utc_lay.addRow("End time", self.end_edit)
    self.out_st_edit = QLineEdit()
    self.out_st_edit.setValidator(QDoubleValidator())
    utc_lay.addRow("Output start time", self.out_st_edit)
    self.pts_edit = QLineEdit()
    self.pts_edit.setValidator(QIntValidator())
    utc_lay.addRow("Number of points", self.pts_edit)
    self.mid_layout.addWidget(self.utc_wid)
    # widget for oneStep case
    self.one_wid = QWidget()
    one_lay = QFormLayout(self.one_wid)
    self.step_edit = QLineEdit()
    self.step_edit.setValidator(QDoubleValidator())
    one_lay.addRow("Step", self.step_edit)
    self.mid_layout.addWidget(self.one_wid)
    # widget for steadyState case
    self.std_wid = QWidget()
    std_lay = QFormLayout(self.std_wid)
    self.mid_layout.addWidget(self.std_wid)
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

  ## Adapt self.mid_layout depending on the current text in self.typ_box.
  # @param self The object pointer.
  def update_layout(self):
    if (self.typ_box.currentText() == 'uniformTimeCourse'):
      self.mid_layout.setCurrentWidget(self.utc_wid)
    elif (self.typ_box.currentText() == 'oneStep'):
      self.mid_layout.setCurrentWidget(self.one_wid)
    elif (self.typ_box.currentText() == 'steadyState'):
      self.mid_layout.setCurrentWidget(self.std_wid)

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
    wid = QWidget()
    lay = QFormLayout(wid)
    self.tsk_id_edit = QLineEdit(self)
    self.tsk_id_edit.setText(str(self.sub.get_task_id()))
    lay.addRow("Task ID", self.tsk_id_edit)
    self.order_edit = QLineEdit(self)
    self.order_edit.setText(str(self.sub.get_order()))
    self.order_edit.setValidator(QIntValidator())
    lay.addRow("Order", self.order_edit)
    self.mid_layout.addWidget(wid)
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
  ## @var mod_edit
  # An instance of PySide.QtGui.QLineEdit for editing 'model_id' attribute of
  # self.tsk.
  ## @var rng_edit
  # An instance of PySide.QtGui.QLineEdit for editing 'master_range' attribute
  # of self.tsk.
  ## @var rpt_wid
  # A PySide.QtGui.QWidget object providing widgets for editing self.tsk in
  # case it is a biopredyn.task.RepeatedTask object.
  ## @var rst_box
  # An instance of PySide.QtGui.QCheckBox for editing 'reset_model' attribute
  # of self.tsk.
  ## @var sim_edit
  # An instance of PySide.QtGui.QLineEdit for editing 'simulation_id' attribute
  # of self.tsk.
  ## @var tsk
  # Reference to the biopredyn.task.Task element to be edited by 'self'.
  ## @var tsk_wid
  # A PySide.QtGui.QWidget object providing widgets for editing self.tsk in
  # case it is a biopredyn.task.Task object.

  ## Constructor.
  # @param self The object pointer.
  # @param tsk A biopredyn.task.Task object; optional (default: None).
  def __init__(self, tsk=None):
    DialogBox.__init__(self)
    self.setWindowTitle("Edit task")
    self.tsk = tsk
    self.id_edit.setText(self.tsk.get_id())
    self.name_edit.setText(self.tsk.get_name())
    # 'type' combo box
    types = ['task', 'repeatedTask']
    self.typ_box = QComboBox()
    self.typ_box.addItems(types)
    self.up_layout.addRow("Type", self.typ_box)
    # layout for 'task' case
    self.tsk_wid = QWidget()
    tsk_lay = QFormLayout(self.tsk_wid)
    # add 'Model reference' field
    self.mod_edit = QLineEdit(self)
    tsk_lay.addRow("Model reference", self.mod_edit)
    # add 'Simulation reference' field
    self.sim_edit = QLineEdit(self)
    tsk_lay.addRow("Simulation reference", self.sim_edit)
    self.mid_layout.addWidget(self.tsk_wid)
    # layout for 'repeatedTask' case
    self.rpt_wid = QWidget()
    rpt_lay = QFormLayout(self.rpt_wid)
    # add 'Reset model' check box
    self.rst_box = QCheckBox(self)
    rpt_lay.addRow("Reset model", self.rst_box)
    # add 'Range reference' field
    self.rng_edit = QLineEdit(self)
    rpt_lay.addRow("Range reference", self.rng_edit)
    self.mid_layout.addWidget(self.rpt_wid)
    if tsk is not None:
      self.tsk = tsk
      self.id_edit.setText(self.tsk.get_id())
      self.name_edit.setText(self.tsk.get_name())
      self.typ_box.setCurrentIndex(types.index(self.tsk.get_type()))
      #self.typ_box.setDisabled(True)
      if (self.typ_box.currentText() == 'task'):
        self.mod_edit.setText(str(self.tsk.get_model_id()))
        self.sim_edit.setText(str(self.tsk.get_simulation_id()))
      elif (self.typ_box.currentText() == 'repeatedTask'):
        self.rst_box.setChecked(self.tsk.get_reset_model())
        self.rng_edit.setText(str(self.tsk.get_master_range()))
      self.update_layout()
    # catch and process currentIndexChanged signal
    self.typ_box.currentIndexChanged.connect(self.update_layout)

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    if self.tsk is not None:
      self.tsk.set_id(str(self.id_edit.text()))
      if self.name_edit.text() is not None:
        self.tsk.set_name(str(self.name_edit.text()))
      if (self.tsk.get_type() == 'task'):
        self.tsk.set_model_id(str(self.mod_edit.text()))
        self.tsk.set_simulation_id(str(self.sim_edit.text()))
      elif (self.tsk.get_type() == 'repeatedTask'):
        self.tsk.set_reset_model(self.rst_box.isChecked())
        self.tsk.set_master_range(str(self.rng_edit.text()))
    self.done(QDialog.Accepted)

  ## Adapt self.mid_layout depending on the current text in self.typ_box.
  # @param self The object pointer.
  def update_layout(self):
    if (self.typ_box.currentText() == 'task'):
      self.mid_layout.setCurrentWidget(self.tsk_wid)
    elif (self.typ_box.currentText() == 'repeatedTask'):
      self.mid_layout.setCurrentWidget(self.rpt_wid)

## DialogBox-derived class for editing biopredyn.ui.tree.VariableElement
## objects.
class VariableBox(DialogBox):
  ## @var mod_edit
  # An instance of PySide.QtGui.QLineEdit for editing 'model_id' attribute of
  # self.var.
  ## @var sym_edit
  # An instance of PySide.QtGui.QLineEdit for editing 'symbol' attribute of
  # self.var.
  ## @var tgt_edit
  # An instance of PySide.QtGui.QLineEdit for editing 'target' attribute of
  # self.var.
  ## @var tsk_edit
  # An instance of PySide.QtGui.QLineEdit for editing 'task_id' attribute of
  # self.var.
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
    wid = QWidget()
    lay = QFormLayout(wid)
    # add 'Target' field
    self.tgt_edit = QLineEdit(self)
    lay.addRow("Target", self.tgt_edit)
    self.tgt_edit.setText(str(self.var.get_target()))
    # add 'Symbol' field
    self.sym_edit = QLineEdit(self)
    lay.addRow("Symbol", self.sym_edit)
    self.sym_edit.setText(str(self.var.get_symbol()))
    # add 'Task reference' field
    self.tsk_edit = QLineEdit(self)
    lay.addRow("Task reference", self.tsk_edit)
    self.tsk_edit.setText(str(self.var.get_task_id()))
    # add 'Model reference' field
    self.mod_edit = QLineEdit(self)
    lay.addRow("Model reference", self.mod_edit)
    self.mod_edit.setText(str(self.var.get_model_id()))
    self.mid_layout.addWidget(wid)

  ## Overriden accept method.
  # @param self The object pointer.
  def accept(self):
    self.var.set_id(str(self.id_edit.text()))
    if self.name_edit.text() is not None:
      self.var.set_name(str(self.name_edit.text()))
    if self.tgt_edit.text() is not None:
      self.var.set_target(str(self.tgt_edit.text()))
    if self.sym_edit.text() is not None:
      self.var.set_symbol(str(self.sym_edit.text()))
    if self.tsk_edit.text() is not None:
      self.var.set_task_id(str(self.tsk_edit.text()))
    if self.mod_edit.text() is not None:
      self.var.set_model_id(str(self.mod_edit.text()))
    self.done(QDialog.Accepted)
