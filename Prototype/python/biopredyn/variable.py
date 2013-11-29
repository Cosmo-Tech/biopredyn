## @package biopredyn
## @author: $Author$
## @date: $Date$
## @copyright: $Copyright: [2013] BioPreDyn $
## @version: $Revision$

import libsedml

class Variable:
  ## @var id
  # A unique identifier for this object.
  ## @var model
  # Reference to the Model object this refers to.
  ## @var name
  # Name of this object.
  ## @var task
  # Reference to the Task object this refers to.
  
  ## Constructor.
  # @param self The object pointer.
  # @param variable A SED-ML variable element.
  # @param workflow A WorkFlow object.
  def __init__(self, variable, workflow):
    self.id = variable.getId()
    self.name = variable.getName()
    self.model = workflow.get_model_by_id(variable.getModelReference())
    self.task = workflow.get_task_by_id(variable.getTaskReference())
  
  ## Getter. Returns self.id.
  # @param self The object pointer.
  # @return self.id
  def get_id(self):
    return self.id
  
  ## Getter. Returns self.name.
  # @param self The object pointer.
  # @return self.name
  def get_name(self):
    return self.name
  
  ## Getter. Returns self.model.
  # @param self The object pointer.
  # @return self.model
  def get_model(self):
    return self.model
  
  ## Getter. Returns self.task.
  # @param self The object pointer.
  # @return self.task
  def get_task(self):
    return self.task