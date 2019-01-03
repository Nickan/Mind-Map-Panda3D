from scenes.mapComponents.nodeData import NodeData
from utils.utils import Utils

import copy

class NodeDataFilter():

  @staticmethod
  def getFilteredData(allData, allStateData):
    filteredData = copy.deepcopy(allData)

    for key, value in allData.items():
      nodeId = value.get(NodeData.ID)
      nodeSettings = allStateData.get(nodeId)
      if nodeSettings is not None:
        folded = nodeSettings.get("folded")
        if folded is not None and folded is True:
          filteredData = NodeDataFilter.removeChildrenIds(
            filteredData, nodeId)
    return filteredData
    

  @staticmethod
  def removeChildrenIds(nodeDataList, nodeId):
    nodeData = nodeDataList.get(nodeId)
    if nodeData != None:
      nodeDataList = NodeDataFilter.removeChildren(nodeData, nodeDataList,
        False)

    return nodeDataList

  @staticmethod
  def removeChildren(nodeData, nodeDataList, includeSelf = True):
    childNodes = Utils.getChildren(nodeData, nodeDataList)
    if childNodes != None:
      for childNode in childNodes:
        NodeDataFilter.removeChildren(childNode, nodeDataList)
    if includeSelf:
      nodeDataList.pop(nodeData.get("id"), None)
    else:
      nodeData.pop("childrenIds", None)
    
    return nodeDataList

  def listIsEmpty(self, list):
    return len(list) == 0

  def getListAddressFrom(self, fromList):
    newList = {}
    for key, value in fromList.items():
      newList[value.get(NodeData.ID)] = value
    return newList

