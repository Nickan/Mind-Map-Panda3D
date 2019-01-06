import copy
import itertools

from collections import defaultdict
from pprint import pprint

from direct.showbase.ShowBase import Vec3
from .nodeDrawing import NodeDrawing
from scenes.mapComponents.dataContainer import DataContainer

from utils.keyManager import KeyManager
from utils.reingoldTilford import ReingoldTilford
from utils.utils import Utils
from platform import node

from .nodeData import NodeData
from .nodeDataFilter import NodeDataFilter



class NodeManager():
  #region Global Fields
  ID = 'id'
  NAME = 'name'
  PARENT_ID = 'parentId'
  CHILDREN_IDS = 'childrenIds'
  DEPTH = "depth"

  #Status field
  SELECTED = "selected"
  LATEST_CREATED_DATA = "latestCreatedData"
  FOLDED = 'folded'
  HIDE_ANCESTORS = 'hideAncestors'
  STARTING_DATA = 'startingData'

  # Main ID
  MAIN_ID = 1
  #endregion

  def __init__(self, allData, allStateData):
    # Will be mutated
    self.allDrawingData = {}
    self.allData = allData
    self.allStateData = allStateData

    self.tree = ReingoldTilford()

  #region
  def createNodeData(self, parentId, name, recheckLastId):
    allData = self.allData
    getUniqueIdFn = Utils.getUniqueId

    allData, newData = self.createNodeDataImpl(parentId, name, recheckLastId,
      allData, getUniqueIdFn)
    return allData, newData

  def createNodeDataImpl(self, parentId, name, recheckLastId, allData, 
    getUniqueIdFn):

    nAllData = copy.deepcopy(allData)
    newData = {}
    newData['id'] = getUniqueIdFn(nAllData, recheckLastId)
    
    newData['parentId'] = parentId
    newData['name'] = name
    parentData = nAllData.get(parentId)
    addDepth = self.setDepth(newData, parentData)
    nAllData[newData.get(NodeManager.ID)] = addDepth
    nAllData = self.addToParentAllData(newData, parentData, nAllData)
    
    return nAllData, nAllData.get(newData.get(NodeManager.ID))

  def getFilteredData(self, allData, allStateData):
    return NodeDataFilter.getFilteredData(allData, allStateData)
    
  def drawData(self, filteredData, allStateData, loader, mapNode,
    getNodePosition):
    for key in filteredData:
      nodeData = filteredData.get(key)
      settings = allStateData.get(key)

      breadth = nodeData.get("x")
      depth = nodeData.get("depth")
      pos = getNodePosition(depth, breadth)

      self.addNodeDrawing(nodeData, settings, loader, mapNode, pos)
  
  def removeAllSelectedField(self, allStateData):
    nallStatusData = copy.deepcopy(allStateData)
    for key in nallStatusData:
      nodeSettings = nallStatusData.get(key)
      if nallStatusData.get("selected") is not None:
        nallStatusData.pop("selected", None)
    return nallStatusData
  #endregion

  #region CreateNodeState
  def addToParentAllData(self, nodeData, parentData, allData):
    if parentData is None:
      return allData

    nAllData = copy.deepcopy(allData)
    pData = nAllData.get(parentData.get(NodeManager.ID))
    if pData is None:
      return nAllData

    children = pData.get('childrenIds')
    if children is None:
      pData['childrenIds'] = []

    nData = nAllData.get(nodeData.get(NodeManager.ID))
    nData[NodeManager.PARENT_ID] = pData.get(NodeManager.ID)

    self.setDepthAndChildren(pData.get(NodeManager.DEPTH), nData, nAllData)
    pData['childrenIds'].append(nData.get(NodeManager.ID))
    return nAllData

  def setDepth(self, nodeData, parentData):
    nData = copy.deepcopy(nodeData)
    if parentData is not None:
      nData["depth"] = parentData.get("depth") + 1
    else:
      nData["depth"] = 1
    return nData
  #endregion

  #region Second Level Functions
  def addNodeDrawing(self, nodeData, nodeSettings, loader, mapNode, pos = Vec3()):
    id = nodeData.get('id')
    text = nodeData.get('name')
    
    nodeDrawing = NodeDrawing(text, loader, mapNode, id)
    nodeDrawing.mainNode.setPos(pos)
    
    nodeDrawing.setSelected(nodeSettings)

    self.allDrawingData[id] = nodeDrawing
    self.setNodeDrawingHeight(nodeData, nodeDrawing)

  def setNodeDrawingHeight(self, nodeData, drawingNode):
    if nodeData.get(NodeManager.ID) == NodeManager.MAIN_ID:
      NodeDrawing.ONE_LINE_TEXT_HEIGHT = drawingNode.getActualTextHeight()
    drawingNode.keepTextCenter()
     
  def showCoords(self, coords):
    for depth, coordDepth in enumerate(dummyCoords):
      for coordBreadth in coordDepth:
        print("point " + str(depth) + ": " + str(coordBreadth))
  
  ##################### Utils  
  def clearAllDrawingData(self):
    for key in self.allDrawingData:
      self.allDrawingData[key].dispose()
    return {}
    
    
  
  def getNodeDrawing(self, nodeData):
    return self.allDrawingData[nodeData["id"]]
  
  def getNodeDrawingPos(self, nodeData):
    nodeDrawing = self.getNodeDrawing(nodeData)
    return nodeDrawing.mainNode.getPos()
  
  def getSelectedNodeData(self):
    for key in self.allStateData:
      setting = self.allStateData.get(key)
      if setting.get(NodeManager.SELECTED) != None:
        return self.allData.get(key)
    return None
  #endregion

  #region Setting the status of the data
  def setStatusAsSelected(self, dataId, allStateData):
    
    return self.addFieldToDataMap(dataId, allStateData, 
      NodeManager.SELECTED)

  def setAsLatestCreatedData(self, dataId, allStateData):
    return self.addFieldToDataMap(dataId, allStateData, 
      NodeManager.LATEST_CREATED_DATA)

  def toggleFoldState(self, dataId, allStateData):
    state = allStateData.get(dataId)
    if state.get(NodeManager.FOLDED) is None:
      return self.addFieldToDataMap(dataId, allStateData, NodeManager.FOLDED)
    else:
      newStateData = copy.deepcopy(allStateData)
      newState = newStateData.get(dataId)
      newState.pop(NodeManager.FOLDED, None)
      return newStateData

  def addFieldToDataMap(self, dataId, dataMap, statusName):
    newMap = copy.deepcopy(dataMap)
    data = newMap.get(dataId)

    if data is None:
      newMap[dataId] = { statusName: True }
    else:
      data[statusName] = True
    return newMap

  def removeFoldedStateWithValidity(self, data, allStateData):
    if NodeData.hasChildren(data):
      return self.removeDataState(data, allStateData, 
        NodeManager.FOLDED)
    
    return allStateData

  def removeDataState(self, data, allStateData, stateDataName):
    dataId = data.get(NodeManager.ID)
    state = allStateData.get(dataId)
    if state is None:
      return allStateData

    nAllState = copy.deepcopy(allStateData)
    newState = nAllState.get(dataId)
    newState.pop(stateDataName, None)
    return nAllState

  #endregion
  
  #region Getter and setter
  def getLatestDrawingNode(self, allDrawingData, allStateData):
    for key in allStateData:
      status = allStateData.get(key)
      if status.get(NodeManager.LATEST_CREATED_DATA) is not None:
        return allDrawingData.get(key), key
    return None

  def removeAllFieldFromDataMap(self, dataMap, fieldName):
    newMap = copy.deepcopy(dataMap)

    for key in newMap:
      data = newMap.get(key)
      data.pop(fieldName, None)
    return newMap

  def getDataWithStatus(self, statusName, allData, allStateData):
    for key in allStateData:
      status = allStateData.get(key)
      if status.get(statusName) is not None:
        return allData.get(key)
    return None

  def removeData(self, data, allData):
    nData = copy.deepcopy(allData)
    removed = self.removeChildren(data, nData, True)

    removed.pop(data.get(NodeManager.ID), None)

    return self.removeIdFromParent(data, removed)

  def removeChildren(self, data, allData, mutateData = False):
    nAllData = allData
    if mutateData is False:
      nAllData = copy.deepcopy(allData)

    nData = nAllData.get(data.get(NodeManager.ID))
    if nData is None:
      return

    childrenIds = nData.get(NodeManager.CHILDREN_IDS)
    if childrenIds is not None:
      for id in childrenIds:
        childData = nAllData.get(id)
        nAllData.pop(id, None)
        self.removeChildren(childData, nAllData)
    return nAllData

  def removeIdFromParent(self, data, allData):
    detachedToParent = copy.deepcopy(allData)

    parentId = data.get(NodeManager.PARENT_ID)
    parentData = detachedToParent.get(parentId)

    childrenIds = parentData.get(NodeManager.CHILDREN_IDS)
    indexInChildList = childrenIds.index(data.get(NodeManager.ID))

    del childrenIds[indexInChildList]
    if len(childrenIds) == 0:
      parentData.pop(NodeManager.CHILDREN_IDS, None)
    else:
      parentData[NodeManager.CHILDREN_IDS] = childrenIds

    return detachedToParent

  def getActivatedNodeData(self):
    for key in self.allStateData:
      statusData = self.allStateData.get(key)
      if statusData.get(DataContainer.SELECTED) != None:
        return self.allData.get(key)
    return None

  def removeAllLatestCreatedField(self):
    return self.removeAllFieldFromDataMap(self.allStateData, 
      NodeManager.LATEST_CREATED_DATA)
  #endregion

  #region DragNodeState
  def switchSelectedNodeDrawingParentTo(self, drawing):
    selData = self.getActivatedNodeData()
    return self.switchSelectedNodeDrawingParentToImpl(drawing, selData, self.allData)

  def switchSelectedNodeDrawingParentToImpl(self, nearestDrawing, selectedData,
    allData):
    nAllData = self.removeIdFromParent(selectedData, allData)

    parentData = nAllData.get(nearestDrawing.id)
    selData = nAllData.get(selectedData.get(NodeManager.ID))
    addPData = self.addToParentAllData(selData, parentData, nAllData)

    return addPData
  #endregion

  #region Have to convert into recursion
  def setDepthAndChildren(self, parentDepth, nodeData, allData):
    currentDepth = parentDepth + 1
    nodeData[NodeManager.DEPTH] = currentDepth
    children = Utils.getChildren(nodeData, allData)
    if children is not None:
      for child in children:
        self.setDepthAndChildren(currentDepth, child, allData)
  #endregion

  #region Common
  def getNodeDataByNodePath(self, nodePath, allDrawingData, filteredData):
    nodePath = nodePath.findNetTag("Node")
    
    for key in allDrawingData:
      nodeDrawing = allDrawingData.get(key)
      if nodePath == nodeDrawing.mainNode:
        return filteredData.get(key)
    return None

  def removeHiddenDataByFoldedState(self, allData, allStateData):
    nAllData = copy.deepcopy(allData)
    for dataId, state in allStateData.items():
      if state.get(NodeManager.FOLDED) is not None:
        data = nAllData.get(dataId)
        if data is not None:
          nAllData = self.removeChildrenAndGrandChildren(data, nAllData)
        
    return nAllData

  def removeChildrenAndGrandChildren(self, data, allData):
    nAllData = copy.deepcopy(allData)
    nAllData = self.removeChildren2(data, 0, nAllData, data, True)

    return nAllData

  # Have to mutate existing data as cloning it takes a lot of CPU time
  def removeChildren2(self, data, index, allData, dataNotToRemove,
    mutateAllData = False):

    if data is None:
      print("error")
      return
    nAllData = {}
    if mutateAllData is False:
      nAllData = copy.deepcopy(allData)
    else:
      nAllData = allData

    childrenIds = data.get(NodeManager.CHILDREN_IDS)
    if childrenIds is not None:
      if index < len(childrenIds):
        childData = nAllData.get(childrenIds[index])
        nAllData = self.removeChildren2(data, index + 1, nAllData, 
          dataNotToRemove, mutateAllData)
        nAllData = self.removeChildren2(childData, 0, nAllData,
          dataNotToRemove, mutateAllData)
      else:
        if data != dataNotToRemove:
          self.removeDataAndToParent(data, nAllData)
    else:
      if data != dataNotToRemove:
        self.removeDataAndToParent(data, nAllData)


    return nAllData

  def removeDataAndToParent(self, data, allData):
    dataId = data.get(NodeManager.ID)
    allData.pop(dataId, None)
    parentData = allData.get(data.get(NodeManager.PARENT_ID))
    if parentData is not None:
      childrenIds = parentData.get(NodeManager.CHILDREN_IDS)
      childrenIds.remove(dataId)
      if len(childrenIds) == 0:
        parentData.pop(NodeManager.CHILDREN_IDS, None)
    # return childrenIds


  def dataHasChildren(self, data):
    childrenIds = data.get(NodeManager.CHILDREN_IDS)
    return childrenIds is not None and len(childrenIds) > 0
  #endregion

# Create Node and Edit Node States
  def onKeyDown(self, keyname, onEnterDownFn, dataId):
    data = self.allData.get(dataId)
    dataDrawing = self.getNodeDrawing(data)

    text = dataDrawing.textNode.getText()
    dataId = data.get(NodeManager.ID)
    text = KeyManager.getModifiedKeyFromKeyInput(text, keyname, 
      dataId, onEnterDownFn)
        
    textNode = dataDrawing.textNode
    textNode.setText(text)
    self.setNodeDrawingHeight(data, dataDrawing)


  #region StaticMapState
  def toggleAncestorShowHide(self, selectedData):
    rAllState = NodeDataFilter.removeAllState(self.allStateData
      , NodeData.LATEST_HIDE_ANCESTORS)

    if NodeData.hasState(selectedData, self.allStateData, NodeData.HIDE_ANCESTORS):
      rAllState1 = self.removeDataState(selectedData, rAllState
        , NodeData.HIDE_ANCESTORS)
      self.allStateData = rAllState1
    else:
      allState2 = self.addDataState(selectedData, rAllState,
        NodeData.ID, NodeData.HIDE_ANCESTORS)
      allState3 = self.addDataState(selectedData, allState2,
        NodeData.ID, NodeData.LATEST_HIDE_ANCESTORS)
      self.allStateData = allState3

  def getStartingData(self, allData, allStateData):
    return NodeDataFilter.getStartingData(allData, allStateData)

  def addDataState(self, state, allDataState, idName, stateName):
    nAllState = copy.deepcopy(allDataState)
    nStateId = state.get(idName)
    nState = nAllState.get(nStateId)

    if nState is None:
      nAllState[nStateId] = { stateName: True }
    else:
      nState[stateName] = True
      nAllState[nStateId] = nState
    return nAllState
  #endregion


  
        




        
        
        
        
        
        
        
        
        
        
        
        
