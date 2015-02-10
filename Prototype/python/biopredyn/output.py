#!/usr/bin/env python
# coding=utf-8

## @package biopredyn
## Copyright: [2012-2015] The CoSMo Company, All Rights Reserved
## License: BSD 3-Clause

import io, csv
from random import gauss
import signals
import libsbml
import libsedml, libnuml
from matplotlib import pyplot as plt
import colorsys

## Base class for encoding the outputs of the current work flow.
class Output:
  ## @var id
  # A unique identifier for the object.
  ## @var signals
  # A list of biopredyn.signals.Data objects.
  ## @var name
  # Name of this object.
  ## @var type
  # Type of output.
  
  ## Constructor; either 'out' or 'idf' and 'typ' must be passed as keyword
  ## argument(s).
  # @param self The object pointer.
  # @param out A libsedml.SedOutput object; optional (default: None).
  # @param idf A unique identifier; optional (default: None).
  # @param name A name for 'self'; optional (default: None).
  # @param typ The type of output encoded in 'self'; can be either 'plot2D',
  # 'plot3D', 'report' or 'output'. Optional (default: None).
  def __init__(self, out=None, idf=None, name=None, typ=None):
    if out is None and (idf is None or typ is None):
      raise RuntimeError("Either 'out' or 'idf' and 'typ' must be " +
        "passed as keyword argument(s).")
    else:
      self.signals = []
      if out is not None:
        self.id = out.getId()
        self.name = out.getName()
        self.type = out.getElementName()
      else:
        self.id = idf
        self.name = name
        self.type = typ
  
  ## String representation of this. Displays it as a hierarchy.
  # @param self The object pointer.
  # @return A string representing this as a hierarchy.
  def __str__(self):
    tree = "  |-" + self.type + " id=" + self.id + " name=" + self.name + "\n"
    return tree

  ## Appends the input biopredyn.signals.Data object to self.signals.
  # @param self The object pointer.
  # @param data A biopredyn.signals.Data object.
  def add_data(self, data):
    self.signals.append(data)
  
  ## Getter. Returns self.id.
  # @param self The object pointer.
  # @return self.id
  def get_id(self):
    return self.id
  
  ## Setter for self.id.
  # @param self The object pointer.
  # @param id New value for self.id.
  def set_id(self, id):
    self.id = id
  
  ## Getter. Returns self.name.
  # @param self The object pointer.
  # @return self.name
  def get_name(self):
    return self.name
  
  ## Setter for self.name.
  # @param self The object pointer.
  # @param name New value for self.name.
  def set_name(self, name):
    self.name = name

  ## Setter for self.signals.
  # @param self The object pointer.
  # @return self.signals
  def get_signals(self):
    return self.signals
  
  ## Getter. Returns self.type.
  # @param self The object pointer.
  # @return self.type
  def get_type(self):
    return self.type

## Output-derived class for 2-dimensional plots.
class Plot2D(Output):
  ## @var plot
  # A matplotlib figure.
  
  ## Overridden constructor; either 'plot_2d' or 'idf' must be passed as keyword
  ## argument(s).
  # @param self The object pointer.
  # @param workflow A WorkFlow object.
  # @param plot_2d A libsedml.SedPlot2D object; optional (default: None).
  # @param idf A unique identifier; optional (default: None).
  # @param name A name for 'self'; optional (default: None).
  def __init__(self, workflow, plot_2d=None, idf=None, name=None):
    if plot_2d is None and idf is None:
      raise RuntimeError("Either 'plot_2d' or 'idf' must be passed as " +
        "keyword argument(s).")
    else:
      if plot_2d is not None:
        Output.__init__(self, out=plot_2d)
        for p in plot_2d.getListOfCurves():
          self.add_data(signals.Curve(workflow, curve=p))
      else:
        Output.__init__(self, idf=idf, name=name, typ="plot2D")
  
  ## String representation of this. Displays it as a hierarchy.
  # @param self The object pointer.
  # @return A string representing this as a hierarchy.
  def __str__(self):
    tree = "  |-" + self.type + " id=" + self.id + " name=" + self.name + "\n"
    tree += "    |-listOfCurves\n"
    for c in self.signals:
      tree += str(c)
    return tree
  
  ## Getter. Returns self.plot.
  # @param self The object pointer.
  # @return self.plot
  def get_plot(self):
    return self.plot
  
  ## Plot the result of the task associated with self.data.
  # @param self The object pointer.
  def process(self):
    self.plot = plt.figure()
    ax = self.plot.add_subplot(111)
    step = 1.0 / len(self.signals)
    hue = 0.0
    for c in self.signals:
      rgb = colorsys.hsv_to_rgb(hue, 0.75, 1.0)
      c.plot(ax, rgb)
      hue += step
    ax.legend()
    ax.autoscale()

  ## Returns the libsedml.SedPlot2D representation of this.
  # @param self The object pointer.
  # @param level Level of SED-ML language to be used.
  # @param version Version of SED-ML language to be used.
  # @return A libsedml.SedPlot2D object.
  def to_sedml(self, level, version):
    plt = libsedml.SedPlot2D(level, version)
    plt.setId(self.get_id())
    plt.setName(self.get_name())
    # curves
    for c in self.get_signals():
      plt.addCurve(c.to_sedml(level, version))
    return plt
  
## Output-derived class for 3-dimensional plots.
class Plot3D(Output):
  ## @var plot
  # A matplotlib figure.
  
  ## Overridden constructor; either 'plot_3d' or 'idf' must be passed as keyword
  ## argument.
  # @param self The object pointer.
  # @param workflow A WorkFlow object.
  # @param plot_3d A libsedml.SedPlot3D object; optional (default: None).
  # @param idf A unique identifier; optional (default: None).
  # @param name A name for 'self'; optional (default: None).
  def __init__(self, workflow, plot_3d=None, idf=None, name=None):
    if plot_3d is None and idf is None:
      raise RuntimeError("Either 'plot_3d' or 'idf' must be passed as " +
        "keyword argument.")
    else:
      if plot_3d is not None:
        Output.__init__(self, out=plot_3d)
        for s in plot_3d.getListOfSurfaces():
          self.add_data(signals.Surface(workflow, surf=s))
      else:
        Output.__init__(self, idf=idf, name=name, typ="plot3D")
  
  ## String representation of this. Displays it as a hierarchy.
  # @param self The object pointer.
  # @return A string representing this as a hierarchy.
  def __str__(self):
    tree = "  |-" + self.type + " id=" + self.id + " name=" + self.name + "\n"
    tree += "    |-listOfSurfaces\n"
    for s in self.signals:
      tree += str(s)
    return tree
  
  ## Getter. Returns self.plot.
  # @param self The object pointer.
  # @return self.plot
  def get_plot(self):
    return self.plot
  
  ## Plot the result of the task associated with self.data.
  # @param self The object pointer.
  def process(self):
    self.plot = plt.figure(self.id)
    ax = self.plot.add_subplot(111, projection='3d')
    for s in self.signals:
      s.plot(ax)
    ax.legend()
    ax.autoscale()

  ## Returns the libsedml.SedPlot3D representation of this.
  # @param self The object pointer.
  # @param level Level of SED-ML language to be used.
  # @param version Version of SED-ML language to be used.
  # @return A libsedml.SedPlot3D object.
  def to_sedml(self, level, version):
    plt = libsedml.SedPlot3D(level, version)
    plt.setId(self.get_id())
    plt.setName(self.get_name())
    # surfaces
    for s in self.get_signals():
      plt.addSurface(s.to_sedml(level, version))
    return plt

## Output-derived class for reports.
class Report(Output):
  
  ## Overridden constructor; either 'report' or 'idf' must be passed as keyword
  ## argument.
  # @param self The object pointer.
  # @param workflow A WorkFlow object.
  # @param report A libsedml.SedReport object; optional (default: None).
  # @param idf A unique identifier; optional (default: None).
  # @param name A name for 'self'; optional (default: None).
  def __init__(self, workflow, report=None, idf=None, name=None):
    if report is None and idf is None:
      raise RuntimeError("Either 'report' or 'idf' must be passed as " +
        "keyword argument.")
    else:
      if report is not None:
        Output.__init__(self, out=report)
        for d in report.getListOfDataSets():
          self.add_data(signals.DataSet(workflow, data=d))
      else:
        Output.__init__(self, idf=idf, name=name, typ="report")
  
  ## Write the result of the task associated with self.data into a report file.
  ## The report format depends on the extension of the input file: if it ends
  ## with '.csv', it will be a CSV file, if it ends with '.xml', it will be a
  ## NuML file.
  # @param self The object pointer.
  # @param filename Where to write the report file.
  def process(self, filename):
    if (filename.endswith('.csv')):
      self.write_as_csv(filename)
    elif (filename.endswith('.xml')):
      self.write_as_numl(filename)
    else:
      raise RuntimeError("Invalid report format. Possible formats " +
        "are: .csv, .xml")

  ## Returns the libsedml.SedReport representation of this.
  # @param self The object pointer.
  # @param level Level of SED-ML language to be used.
  # @param version Version of SED-ML language to be used.
  # @return A libsedml.SedReport object.
  def to_sedml(self, level, version):
    rpt = libsedml.SedReport(level, version)
    rpt.setId(self.get_id())
    rpt.setName(self.get_name())
    # datasets
    for d in self.get_signals():
      rpt.addDataSet(d.to_sedml(level, version))
    return rpt
  
  ## Write the result of the task associated with self.data into a column 
  ## oriented CSV file. Each column corresponds to one iteration of each
  ## biopredyn.signals.DataSet object, except the time column.
  # @param self The object pointer.
  # @param filename Where to write the CSV file.
  # @param artificial Whether this report should be used to generate artificial
  # data by adding noise to the non-time datasets. Default: False.
  # @param noise_type The type of noise to be added to the datasets. Possible
  # values are 'homoscedastic' (standard deviation of the noise is constant)
  # and 'heteroscedastic' (standard deviation is proportional to the value of
  # each data point). Default: 'heteroscedastic'.
  # @param std_dev Standard deviation of the noise distribution (gaussian). If
  # noise_type is 'homoscedastic', std_dev is the exact value of the standard
  # deviation; if noise_type is 'heteroscedastic', std_dev is a percentage.
  # Default: 0.1
  def write_as_csv(self, filename, artificial=False,
    noise_type='heteroscedastic', std_dev=0.1):
    # Open a file at the given location
    f = open(filename, 'w')
    writer = csv.writer(f, delimiter=',')
    # writing header
    header = []
    for d in self.signals:
      header.append(d.get_label())
    writer.writerow(header)
    # writing data - it is assumed all datasets have the same number of points
    n_points = self.signals[0].get_data_gen().get_number_of_points()
    # for each time_point
    for n in range(n_points):
      num_exp = 0
      # number of experiments is detected
      for d in self.signals:
        if d.get_num_experiments() > num_exp:
          num_exp = d.get_num_experiments()
      # data is written
      for e in range(num_exp):
        data = []
        for d in self.signals:
          if str.lower(d.get_label()).__contains__("time"):
            data.append(d.get_data_gen().get_values()[0][n])
          else: # non-time series might be added noise
            v = d.get_data_gen().get_values()[e][n]
            if not artificial:
              data.append(v)
            elif noise_type == "heteroscedastic":
              data.append(gauss(v, v * std_dev))
            elif noise_type == "homoscedastic":
              data.append(gauss(v, std_dev))
            else:
              raise RuntimeError("Invalid noise type; expected noise types " +
                "are 'homoscedastic' or 'heteroscedastic'.")
        writer.writerow(data)
    f.close()
  
  ## Write the result of the task associated with self.data into a NuML file.
  # @param self The object pointer.
  # @param filename Where to write the NuML file.
  # @param artificial Whether this report should be used to generate artificial
  # data by adding noise to the non-time datasets. Default: False.
  # @param noise_type The type of noise to be added to the datasets. Possible
  # values are 'homoscedastic' (standard deviation of the noise is constant)
  # and 'heteroscedastic' (standard deviation is proportional to the value of
  # each data point). Default: 'heteroscedastic'.
  # @param std_dev Standard deviation of the noise distribution (gaussian). If
  # noise_type is 'homoscedastic', std_dev is the exact value of the standard
  # deviation; if noise_type is 'heteroscedastic', std_dev is a percentage.
  # Default: 0.1
  def write_as_numl(self, filename, artificial=False,
    noise_type='heteroscedastic', std_dev=0.1):
    # Create a new NuML document and complete it
    doc = libnuml.NUMLDocument()
    # Add a ResultComponent
    comp = doc.createResultComponent()
    comp.setId(self.name)
    # Add the default DimensionDescription
    time_desc = comp.createCompositeDescription()
    time_desc.setName("time")
    time_desc.setIndexType("double")
    series_desc = time_desc.createCompositeDescription()
    series_desc.setName("series")
    series_desc.setIndexType("string")
    exp_desc = series_desc.createCompositeDescription()
    exp_desc.setName("experiment")
    exp_desc.setIndexType("integer")
    val_desc = exp_desc.createAtomicDescription()
    val_desc.setName("value")
    val_desc.setValueType("double")
    # Create iterations and indices
    num_indices = self.signals[0].get_number_of_points()
    for i in range(num_indices):
      i_value = comp.createCompositeValue()
      i_value.setIndexValue(str(i)) # temporary value
    # Populate the indices with values
    for d in self.signals:
      d.write_as_numl(comp.getDimension(), artificial, noise_type, std_dev)
    writer = libnuml.NUMLWriter()
    writer.writeNUML(doc, filename)
