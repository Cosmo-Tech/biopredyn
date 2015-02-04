#!/usr/bin/env python
# coding=utf-8

## @package biopredyn
## Copyright: [2012-2015] The CoSMo Company, All Rights Reserved
## License: BSD 3-Clause

from PySide.QtGui import *

## PySIde.QtGui.QTabWidget-derived class for displaying graphical outputs from
## the execution of SED-ML work flows.
class TabPanel(QTabWidget):

  ## Constructor.
  # @param self The object pointer.
  # @param parent A biopredyn.ui.mainwindow.MainWindow object.
  def __init__(self, parent):
    QTabWidget.__init__(self, parent)
