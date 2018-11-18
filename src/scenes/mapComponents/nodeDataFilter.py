from scenes.mapComponents.nodeData import NodeData
from utils.utils import Utils

class NodeDataFilter():

  def getFilteredNodeData(self, dataContainer):
    self.manageData(dataContainer)

    for key, value in dataContainer.unfilteredData.iteritems():
      nodeId = value.get(NodeData.ID)
      nodeSettings = dataContainer.nodeDataSettings.get(nodeId)
      if nodeSettings is not None:
        folded = nodeSettings.get("folded")
        if folded is not None and folded is True:
          dataContainer.nodeDataList = self.removeChildrenIds(
            dataContainer.nodeDataList, nodeId)
    return dataContainer.nodeDataList


  def removeChildrenIds(self, nodeDataList, nodeId):
    nodeData = nodeDataList.get(nodeId)
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


  def manageData(self, dataContainer):
    unfilteredData = dataContainer.unfilteredData
    nodeDataList = dataContainer.nodeDataList

    if self.listIsEmpty(unfilteredData):
      dataContainer.unfilteredData = self.getListAddressFrom(nodeDataList)
    else:
      dataContainer.nodeDataList = self.getListAddressFrom(unfilteredData)

  def listIsEmpty(self, list):
    return len(list) == 0

  def getListAddressFrom(self, fromList):
    newList = {}
    for key, value in fromList.iteritems():
      newList[value.get(NodeData.ID)] = value
    return newList

