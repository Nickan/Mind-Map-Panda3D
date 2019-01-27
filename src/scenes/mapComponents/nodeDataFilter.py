from scenes.mapComponents.nodeData import NodeData
from utils.utils import Utils

import copy

class NodeDataFilter():

  @staticmethod
  def getFilteredData(allData, allStateData):
    filteredData = copy.deepcopy(allData)
    nFilteredData = copy.deepcopy(allData)

    startingData1 = NodeDataFilter.getStartingData(allData, allStateData)
    removedAncestors = NodeDataFilter.removeAncestors(startingData1, 
      nFilteredData, allStateData)        

    startingData2 = NodeDataFilter.getStartingData(removedAncestors,
      allStateData)
    endResultFilteredData = NodeDataFilter.removeChildrenOfFoldedData(
      startingData2, removedAncestors, allStateData)

    if endResultFilteredData is None:
      return filteredData
    return endResultFilteredData
  
  @staticmethod
  def removeChildrenOfFoldedData(startingData, allData, allStateData):
    return NodeDataFilter.removeChildrenOfFoldedDataImpl(startingData,
      0, allData, allStateData)

  @staticmethod
  def removeChildrenOfFoldedDataImpl(data, childIndex, allData, allStateData):
    dataId = data.get(NodeData.ID)
    state = allStateData.get(dataId)
    
    if state is not None and state.get(NodeData.FOLDED) is not None:
      childrenIds = data.get(NodeData.CHILDREN_IDS)
      if childrenIds is not None:
        return NodeDataFilter.removeChildrenIds(allData, dataId, data)
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
  def getStartingData(allData, allStateData):
    data = NodeDataFilter.getDataWithStatus(NodeData.LATEST_HIDE_ANCESTORS,
      allData, allStateData)
    if data is None:
      return NodeDataFilter.getNoParentData(allData)
    return data

  @staticmethod
  def getNoParentData(allData):
    for key, value in allData.items():
      if value.get(NodeData.PARENT_ID) is None:
        return value
    return None
  
  @staticmethod
  def removeChildrenIds(allData, nodeId, dataNotToRemove = None, 
    mutateData = True):
    data = allData.get(nodeId)
    if data is None:
      return allData

    nAllData = allData
    if mutateData is False:
      nAllData = copy.deepcopy(allData)
      
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
  def removeAncestors(startingData, allData, allStateData):
    if startingData is None:
      return allData

    nAllData1 = copy.deepcopy(allData)

    nAllData2 = NodeDataFilter.removeAncestorsImpl(startingData, 0, 
      nAllData1, allStateData, NodeData.ID, NodeData.PARENT_ID,
      NodeData.CHILDREN_IDS)
    return nAllData2

  @staticmethod
  def removeAncestorsImpl(data, childIndex, allData, allStateData, idName,
    parentIdName, childrenIdsName):
    if data is None:
      return allData

    if NodeData.hasState(data, allStateData, NodeData.HIDE_ANCESTORS):
      return NodeDataFilter.removeAllAncestors(data, allData)
    else:
      childrenIds = data.get(childrenIdsName)
      if childrenIds is not None and childIndex < len(childrenIds):
        childId = childrenIds[childIndex]
        childData = allData.get(childId)
        allData1 = NodeDataFilter.removeAncestorsImpl(data, childIndex + 1, 
          allData, allStateData, idName, parentIdName, childrenIdsName)
        allData2 = NodeDataFilter.removeAncestorsImpl(childData, 
          0, allData1, allStateData, idName, parentIdName, 
          childrenIdsName)
        return allData2
      return allData

  @staticmethod
  def removeAllAncestors(data, allData):
    if data is None:
      return allData

    allData1 = copy.deepcopy(allData)

    allData2 = NodeDataFilter.removeDataAndToParent(data, allData1,
      NodeData.ID, NodeData.PARENT_ID, NodeData.CHILDREN_IDS)

    allData3 = NodeDataFilter.removeAllAncestorsRecursion(data, allData2)

    newData = copy.deepcopy(data)
    dataId = newData.get(NodeData.ID)
    newData.pop(NodeData.PARENT_ID, None)
    allData3[dataId] = newData
    return allData3
    
  @staticmethod
  def removeAllAncestorsRecursion(data, allData):
    parent = NodeDataFilter.getParent(data, allData, NodeData.PARENT_ID)
    if parent != None:
      allData1 = NodeDataFilter.removeChildrenIds(allData, 
        parent.get(NodeData.ID))
      return NodeDataFilter.removeAllAncestorsRecursion(parent, allData1)

    allData.pop(data.get(NodeData.ID), None)
    return allData

  @staticmethod
  def getParent(data, allData, parentIdName):
    parentId = data.get(parentIdName)
    if parentId == None:
      return None
    return allData.get(parentId)

  @staticmethod
  def removeAllState(allStateData, stateName):
    nAllStatusData = copy.deepcopy(allStateData)
    for key in nAllStatusData:
      state = nAllStatusData.get(key)
      if state.get(stateName) is not None:
        state.pop(stateName, None)
    return nAllStatusData

  @staticmethod
  def getDataWithStatus(stateName, allData, allStateData):
    for key in allStateData:
      status = allStateData.get(key)
      if status.get(stateName) is not None:
        return allData.get(key)
    return None

  @staticmethod
  def removeData(self, data, allData):
    nData = copy.deepcopy(allData)
    # removed = self.removeChildren2(data, 0, nData)
    dataId = data.get(NodeData.ID)
    removed = self.removeChildren2(nData, dataId)
    removed.pop(data.get(NodeData.ID), None)
    return NodeDataFilter.removeIdFromParent(data, removed)

  def removeIdFromParent(self, data, allData):
    # detachedToParent = copy.deepcopy(allData)
    detachedToParent = allData

    parentId = data.get(NodeData.PARENT_ID)
    parentData = detachedToParent.get(parentId)

    childrenIds = parentData.get(NodeData.CHILDREN_IDS)
    indexInChildList = childrenIds.index(data.get(NodeData.ID))

    del childrenIds[indexInChildList]
    if len(childrenIds) == 0:
      parentData.pop(NodeData.CHILDREN_IDS, None)
    else:
      parentData[NodeData.CHILDREN_IDS] = childrenIds

    return detachedToParent

  @staticmethod
  def getDataWithFoldedAncestorNearestTo(startingData, allData,
    allStateData):
    parentId = startingData.get(NodeData.PARENT_ID)
    if parentId is None:
      return startingData

    state = allStateData.get(parentId)
    if state is None or state.get(NodeData.HIDE_ANCESTORS) is None:
      return NodeDataFilter.getDataWithFoldedAncestorNearestTo(
        allData.get(parentId), allData, allStateData)
    else:
      return allData.get(parentId)