## @package biopredyn
## @author: $Author$
## @date: $Date$
## @copyright: $Copyright: [2013] BioPreDyn $
## @version: $Revision$

import data
import libsedml

## Base class for encoding the outputs of the current work flow.
class Output:
  ## @var id
  # A unique identifier for the object.
  
  ## Constructor.
  # @param self The object pointer.
  # @param id The ID of a SED-ML output.
  def __init__(self, id):
    self.id = id
  
  ## Getter. Returns self.id.
  def get_id(self):
    return self.id

## Output-derived class for 2-dimensional plots.
class Plot2D(Output):
  ## @var curves
  # A list of 2-dimensional signals to be plotted on the output.
  
  ## Overridden constructor.
  # @param self The object pointer.
  # @param plot_2d A SedPlot2D object.
  def __init__(self, plot_2d):
    self.id = plot_2d.getId()
    for p in plot_2d.getNumCurves():
      self.curves.append(data.Curve(plot_2d.getCurve(p)))
  
  ## Plot the result of the task associated with self.data.
  # @param self The object pointer.
  def plot_curves(self):
    print "TODO"

## Output-derived class for 3-dimensional plots.
class Plot3D(Output):
  ## @var surfaces
  # A list of 3-dimensional signals to be plotted on the output.
  
  ## Overridden constructor.
  # @param self The object pointer.
  # @param plot_3d A SedPlot3D object.
  def __init__(self, plot_3d):
    self.id = plot_3d.getId()
    for p in plot_3d.getNumSurfaces():
      self.surfaces.append(data.Curve(plot_3d.getSurface(p)))
  
  ## Plot the result of the task associated with self.data.
  # @param self The object pointer.
  def plot_surfaces(self):
    print "TODO"

## Output-derived class for reports.
class Report(Output):
  
  ## Write the result of the task associated with self.data into a CSV file.
  # @param self The object pointer.
  def write(self):
    print "TODO"