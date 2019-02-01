#!/usr/bin/env python
# coding=utf-8

## @package biopredyn
## Copyright: [2012-2019] Cosmo Tech, All Rights Reserved
## License: BSD 3-Clause

from PySide.QtGui import *                                                      
import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

## PySIde.QtGui.QWidget-derived class for embedding matplotlib graphical outputs
## from the execution of SED-ML work flows.
class Tab(QWidget):
  ## @var canvas
  # A matplotlib canvas embedding a plot in 'self'.
  ## @var nav_bar
  # Toolbar for manipulating the plot displayed in 'self'.

  ## Constructor.
  # @param self The object pointer.
  # @param plot A matplotlib.pyplot.figure object.
  # @param parent A biopredyn.ui.tabpanel.TabPanel object.
  def __init__(self, plot, parent):
    QWidget.__init__(self, parent)
    self.canvas = FigureCanvas(plot)
    self.nav_bar = NavigationToolbar(self.canvas, self)
    self.setLayout(QVBoxLayout(self))
    self.layout().addWidget(self.nav_bar)
    self.layout().addWidget(self.canvas)

## PySIde.QtGui.QTabWidget-derived class for displaying graphical outputs from
## the execution of SED-ML work flows.
class TabPanel(QTabWidget):

  ## Constructor.
  # @param self The object pointer.
  # @param parent A biopredyn.ui.mainwindow.MainWindow object.
  def __init__(self, parent):
    QTabWidget.__init__(self, parent)
    self.setTabsClosable(True)
    self.tabCloseRequested.connect(self.removeTab)

  ## Builds a Tab object from the input 'output' argument and appends it to
  ## 'self'.
  # @param self The object pointer.
  # @param output A processed graphical biopredyn.output.Output object; i.e.
  # either a biopredyn.output.Plot2D or a biopredyn.output.Plot3D object.
  def add_tab(self, output):
    tab = Tab(output.get_plot(), self)
    self.addTab(tab, output.get_id())
