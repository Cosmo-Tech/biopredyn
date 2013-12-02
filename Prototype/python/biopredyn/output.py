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
  ## @var name
  # Name of this object.
  ## @var type
  # Type of output.
  
  ## Constructor.
  # @param self The object pointer.
  # @param out A SedOutput object.
  def __init__(self, out):
    self.id = out.getId()
    self.name = out.getName()
    self.type = out.getElementName()
  
  ## String representation of this. Displays it as a hierarchy.
  # @param self The object pointer.
  # @return A string representing this as a hierarchy.
  def __str__(self):
    tree = "  +- " + self.type + " id=" + self.id + " name=" + self.name + "\n"
    return tree
  
  ## Getter. Returns self.id.
  def get_id(self):
    return self.id
  
  ## Getter. Returns self.name.
  # @param self The object pointer.
  def get_name(self):
    return self.name
  
  ## Getter. Returns self.type.
  # @param self The object pointer.
  # @return self.type
  def get_type(self):
    return self.type

## Output-derived class for 2-dimensional plots.
class Plot2D(Output):
  ## @var curves
  # A list of 2-dimensional signals to be plotted on the output.
  
  ## Overridden constructor.
  # @param self The object pointer.
  # @param plot_2d A SedPlot2D object.
  # @param workflow A WorkFlow object.
  def __init__(self, plot_2d, workflow):
    self.id = plot_2d.getId()
    self.name = plot_2d.getName()
    self.type = plot_2d.getElementName()
    self.curves = []
    for p in plot_2d.getListOfCurves():
      self.curves.append(data.Curve(p, workflow))
  
  ## String representation of this. Displays it as a hierarchy.
  # @param self The object pointer.
  # @return A string representing this as a hierarchy.
  def __str__(self):
    tree = "  +- " + self.type + " id=" + self.id + " name=" + self.name + "\n"
    tree += "    +- listOfCurves\n"
    for c in self.curves:
      tree += str(c)
    return tree
  
  ## Plot the result of the task associated with self.data.
  # @param self The object pointer.
  def plot_curves(self):
    print "Plot2D::plot_curves TODO"
  
  ## Getter. Returns self.curves.
  # @param self The object pointer.
  # @return self.curves
  def get_curves(self):
    return self.curves

## Output-derived class for 3-dimensional plots.
class Plot3D(Output):
  ## @var surfaces
  # A list of 3-dimensional signals to be plotted on the output.
  
  ## Overridden constructor.
  # @param self The object pointer.
  # @param plot_3d A SedPlot3D object.
  # @param workflow A WorkFlow object.
  def __init__(self, plot_3d, workflow):
    self.id = plot_3d.getId()
    self.name = plot_3d.getName()
    self.type = plot_3d.getElementName()
    self.surfaces = []
    for s in plot_3d.getListOfSurfaces():
      self.surfaces.append(data.Surface(s, workflow))
  
  ## String representation of this. Displays it as a hierarchy.
  # @param self The object pointer.
  # @return A string representing this as a hierarchy.
  def __str__(self):
    tree = "  +- " + self.type + " id=" + self.id + " name=" + self.name + "\n"
    tree += "    +- listOfSurfaces\n"
    for s in self.surfaces:
      tree += str(s)
    return tree
  
  ## Plot the result of the task associated with self.data.
  # @param self The object pointer.
  def plot_surfaces(self):
    print "Plot3D::plot_surfaces TODO"
  
  ## Getter. Returns self.surfaces.
  # @param self The object pointer.
  # @return self.surfaces
  def get_surfaces(self):
    return self.surfaces

## Output-derived class for reports.
class Report(Output):
  
  ## Constructor.
  # @param self The object pointer.
  # @param report A SedReport object.
  # @param workflow A WorkFlow object.
  def __init__(self, report, workflow):
    self.id = out.getId()
    self.name = out.getName()
    self.type = out.getElementName()
    # TODO: list of DataSet objects.
  
  ## Write the result of the task associated with self.data into a CSV file.
  # @param self The object pointer.
  def write(self):
    print "Report::write TODO"