#!/usr/bin/env python
# coding=utf-8

## @package biopredyn
## Copyright: [2012-2015] The CoSMo Company, All Rights Reserved
## License: BSD 3-Clause

from PySide.QtGui import QMainWindow

## Class describing the main window for the BioPreDyn user interface.
# Derived from PySide.QtGui.QMainWindow.
class MainWindow(QMainWindow):

  ## Constructor.
  # @param self The object pointer.
  def __init__(self):
    QMainWindow.__init__(self)
    self.setObjectName("biopredynUI")
    self.resize(800, 600)
