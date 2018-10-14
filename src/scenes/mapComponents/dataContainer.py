import copy

class DataContainer():
  SELECTED = "selected"

  def __init__(self, nodeDataList, nodeDataSettings):
    self.unfilteredData = copy.deepcopy(nodeDataList)
    self.nodeDataList = nodeDataList
    self.nodeDataSettings = nodeDataSettings