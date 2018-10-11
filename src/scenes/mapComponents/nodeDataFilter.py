import copy

from utils.utils import Utils

class NodeDataFilter():

  def getFilteredNodeData(self, dataContainer):
    dataContainer.nodeDataList = copy.deepcopy(dataContainer.unfilteredData)

    for key in dataContainer.unfilteredData:
      nodeSettings = dataContainer.nodeDataSettings.get(key)
      if nodeSettings is not None:
        folded = nodeSettings.get("folded")
        if folded is not None and folded is True:
          dataContainer.nodeDataList = self.removeChildrenIds(
            dataContainer.nodeDataList, key)
    return dataContainer.nodeDataList


  def removeChildrenIds(self, nodeDataList, key):
    nodeData = nodeDataList.get(key)
    if nodeData != None:
      nodeDataList = self.removeChildren(nodeData, nodeDataList,
        False)

    return nodeDataList

  def removeChildren(self, nodeData, nodeDataList, includeSelf = True):
    childNodes = Utils.getChildren(nodeData, nodeDataList)
    if childNodes != None:
      for childNode in childNodes:
        self.removeChildren(childNode, nodeDataList)
    if includeSelf:
      nodeDataList.pop(nodeData.get("id"), None)
    else:
      nodeData.pop("childrenIds", None)
    
    return nodeDataList

