import copy

class DataContainer():
  SELECTED = "selected"

  def __init__(self, unfilteredData, nodeDataSettings):
    self.unfilteredData = unfilteredData
    self.filteredData = copy.deepcopy(unfilteredData)
    self.nodeDataSettings = nodeDataSettings