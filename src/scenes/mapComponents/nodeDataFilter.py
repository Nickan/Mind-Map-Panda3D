from scenes.mapComponents.nodeData import NodeData
from utils.utils import Utils

import copy

class NodeDataFilter():

  @staticmethod
  def getFilteredData(allData, allStateData, startingData):
    filteredData = copy.deepcopy(allData)
    nFilteredData = copy.deepcopy(allData)

    # removedAncestors = NodeDataFilter.removeAncestors(startingData, 
    #   nFilteredData, allStateData)        

    endResultFilteredData = NodeDataFilter.removeChildrenOfFoldedData(
      filteredData, allStateData)

    if endResultFilteredData is None:
      return filteredData
    return endResultFilteredData
  
  @staticmethod
  def removeChildrenOfFoldedData(allData, allStateData):
    startingData = NodeDataFilter.getStartingData(allData)

    return NodeDataFilter.removeChildrenOfFoldedDataImpl(startingData,
      0, allData, allStateData)

  @staticmethod
  def removeChildrenOfFoldedDataImpl(data, childIndex, allData, allStateData):
    dataId = data.get(NodeData.ID)
    state = allStateData.get(dataId)
    
    if state is not None and state.get(NodeData.FOLDED) is not None:
      childrenIds = data.get(NodeData.CHILDREN_IDS)
      if childrenIds is not None:
        return NodeDataFilter.removeChildrenIds(allData, dataId)
    else:
      childrenIds = data.get(NodeData.CHILDREN_IDS)
      if childrenIds is not None: 
        if childIndex < len(childrenIds):
          childId = childrenIds[childIndex]
          childData = allData.get(childId)
          rAll1 = NodeDataFilter.removeChildrenOfFoldedDataImpl(data, 
            childIndex + 1, allData, allStateData)
          rAll2 = NodeDataFilter.removeChildrenOfFoldedDataImpl(childData, 
            0, rAll1, allStateData)
          return rAll2
    return allData
    


  @staticmethod
  def getStartingData(allData):
    for key, value in allData.items():
      if value.get(NodeData.PARENT_ID) is None:
        return value
    return None
  
    

  @staticmethod
  def removeChildrenIds(allData, nodeId, mutateData = True):
    data = allData.get(nodeId)
    if data is None:
      return allData

    nAllData = copy.deepcopy(allData)
    if mutateData:
      nAlldata = allData
      
    from scenes.mapComponents.nodeManager import NodeManager
    return NodeDataFilter.removeChildren(data, 0, nAllData, data,
      NodeManager.ID, NodeManager.PARENT_ID, NodeManager.CHILDREN_IDS,
      True)

  @staticmethod
  def removeChildren(data, index, allData, dataNotToRemove, 
    idName, parentIdName, chilrenIdsName, mutateAllData = False):

    if data is None:
      print("removeChildren() Data is None")
      return allData
    nAllData = {}
    if mutateAllData is False:
      nAllData = copy.deepcopy(allData)
    else:
      nAllData = allData

    childrenIds = data.get(chilrenIdsName)
    if childrenIds is not None:
      if index < len(childrenIds):
        childData = nAllData.get(childrenIds[index])
        nAllData = NodeDataFilter.removeChildren(data, index + 1, nAllData, 
          dataNotToRemove, idName, parentIdName, chilrenIdsName, mutateAllData)
        nAllData = NodeDataFilter.removeChildren(childData, 0, nAllData,
          dataNotToRemove, idName, parentIdName, chilrenIdsName, mutateAllData)
      else:
        if data != dataNotToRemove:
          NodeDataFilter.removeDataAndToParent(data, nAllData, idName, 
            parentIdName, chilrenIdsName)
    else:
      if data != dataNotToRemove:
        NodeDataFilter.removeDataAndToParent(data, nAllData, idName,
          parentIdName, chilrenIdsName)

    return nAllData

  def removeDataAndToParent(data, allData, idName, parentIdName, 
    chilrenIdsName):
    dataId = data.get(idName)
    allData.pop(dataId, None)
    parentData = allData.get(data.get(parentIdName))
    if parentData is not None:
      childrenIds = parentData.get(chilrenIdsName)
      childrenIds.remove(dataId)
      if len(childrenIds) == 0:
        parentData.pop(chilrenIdsName, None)
    return allData

  @staticmethod
  def removeAncestors(data, allData, allDataState):
    from scenes.mapComponents.nodeManager import NodeManager
    nAllData = copy.deepcopy(allData)

    if data is not None:
      nAllData = NodeDataFilter.removeDataAndToParent(data, nAllData, 
        NodeManager.ID, NodeManager.PARENT_ID, NodeManager.CHILDREN_IDS)

      nAllData = NodeDataFilter.removeAncestorsImpl(data, nAllData,
        allDataState,
        NodeManager.ID, NodeManager.PARENT_ID, NodeManager.CHILDREN_IDS)

      data.pop(NodeManager.PARENT_ID, None)
      nAllData[data.get(NodeManager.ID)] = data
    return nAllData

  @staticmethod
  def removeAncestorsImpl(data, allData, allDataState, idName, parentIdName,
    childrenIdsName):

    # data will be the starting point
    # It will be considered as the Main data
    parent = NodeDataFilter.getParent(data, allData, parentIdName)
    if parent != None:
      allData = NodeDataFilter.removeChildrenIds(allData, parent.get(idName))

      return NodeDataFilter.removeAncestorsImpl(parent, allData, allDataState,
        idName, parentIdName, childrenIdsName)
    else:
      allData.pop(data.get(idName), None)
    return allData


  @staticmethod
  def getParent(data, allData, parentIdName):
    parentId = data.get(parentIdName)
    if parentId == None:
      return None
    return allData.get(parentId)

  # @staticmethod
  # def getSiblings(data, parent, allData, childrenIdsName):
  #   childrenIds = parent.get(childrenIdsName)
  #   if childrenIds is None:
  #     return None

