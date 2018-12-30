import copy
import itertools

from collections import defaultdict
from pprint import pprint

from direct.showbase.ShowBase import Vec3
from scenes.mapComponents.nodeDrawing import NodeDrawing
from scenes.mapComponents.dataContainer import DataContainer

from utils.reingoldTilford import ReingoldTilford
from utils.utils import Utils
from platform import node
from .nodeDataFilter import NodeDataFilter


class NodeManager():
  ID = 'id'
  NAME = 'name'
  PARENT_ID = 'parentId'
  CHILDREN_IDS = 'childrenIds'

  #Status field
  SELECTED = "selected"
  LATEST_CREATED_DATA = "latestCreatedData"
  FOLDED = 'folded'

  # Main ID
  MAIN_ID = 1

  def __init__(self, allData, allStateData):
    # Will be mutated
    self.allDrawingData = {}
    self.allData = allData
    self.allStateData = allStateData

    self.tree = ReingoldTilford()


#First level functions
  def createNodeData(self, parentId, name, recheckLastId, allData,
    getUniqueId):

    newData = {}
    newData['parentId'] = parentId
    newData['name'] = name
    newData['id'] = getUniqueId(allData, recheckLastId)

    parentData = allData.get(parentId)
    self.addToParent(newData, parentData)
    self.setDepth(newData, parentData)
    return newData

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

  
#createNodeData()
  def addToParent(self, nodeData, parentData):
    if parentData is None:
      return

    children = parentData.get('childrenIds')
    if children is None:
      parentData['childrenIds'] = []
    parentData['childrenIds'].append(nodeData['id'])

  def setDepth(self, nodeData, parentData):
    if parentData is not None:
      nodeData["depth"] = parentData.get("depth") + 1
    else:
      nodeData["depth"] = 1

#Second Level Functions
  def addNodeDrawing(self, nodeData, nodeSettings, loader, mapNode, pos = Vec3()):
    id = nodeData.get('id')
    text = nodeData.get('name')
    selected = False
    if nodeSettings is not None:
      selected = nodeSettings.get('selected')
    
    nodeDrawing = NodeDrawing(text, loader, mapNode, id)
    nodeDrawing.mainNode.setPos(pos)
    
    if selected is not None:
      nodeDrawing.setSelected(selected)

    self.allDrawingData[id] = nodeDrawing
    self.setNodeDrawingHeight(nodeDrawing)

  def setNodeDrawingHeight(self, drawingNode):
    NodeDrawing.ONE_LINE_TEXT_HEIGHT = drawingNode.getActualTextHeight()
    drawingNode.keepTextCenter()
    
  
  """ TODO, implementation needs to be changed """
  def getNodeData(self, nodePath, allDrawingData, filteredData):
    nodePath = nodePath.findNetTag("Node")
    
    for key in allDrawingData:
      nodeDrawing = allDrawingData.get(key)
      if nodePath == nodeDrawing.mainNode:
        return filteredData.get(key)
    return None
  
  def getNodeDataId(self, nodeData):
    nodeDataList = self.dataContainer.nodeDataList
    for key in nodeDataList:
      if nodeData == nodeDataList[key]:
        return key
    
    
  def showCoords(self, coords):
    for depth, coordDepth in enumerate(dummyCoords):
      for coordBreadth in coordDepth:
        print("point " + str(depth) + ": " + str(coordBreadth))
        
  
  def deleteNodeData(self, nodeDataToDelete):
    if nodeDataToDelete["id"] == 1:
      print("Can't delete Main node")
      return
    
    self.removeFromParentChildrenIdList(nodeDataToDelete)
    self.deleteNodeAndChildren(nodeDataToDelete)
    
    
  def removeFromParentChildrenIdList(self, nodeDataToDelete):
    parentId = nodeDataToDelete["parentId"]
    # nodeDataList = self.dataContainer.nodeDataList
    parentNodeData = nodeDataList[parentId]
    
    childrenIds = parentNodeData.get('childrenIds')
    if childrenIds is not None:
      childrenIds.remove(nodeDataToDelete["id"])
      # Remove the childrenIds field if there is no childrenIds left
      if len(childrenIds) == 0:
        parentNodeData.pop('childrenIds')
    
  def deleteNodeAndChildren(self, nodeData):
    nodeDataList = self.dataContainer.nodeDataList
    nodeDataList.pop(nodeData["id"])
    childrenIds = nodeData.get("childrenIds")
    
    if childrenIds is not None:
      for childId in childrenIds:
        childData = nodeDataList[childId]
        self.deleteNodeAndChildren(childData)

  
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
  
  
  def setNodeSelected(self, nodeData, nodeDataList = None):
    self.setAllAsUnselected(nodeDataList)
    selectedNodeDrawing = self.getNodeDrawing(nodeData)
    selectedNodeDrawing.setSelected(True)
    
  def setAllAsUnselected(self, nodeDataList = None):
    for key in self.allDrawingData:
      nodeDrawing = self.allDrawingData[key]
      nodeDrawing.setSelected(False)
      
      if nodeDataList is None:
        nodeData = self.dataContainer.nodeDataList[key]
      else:
        nodeData = nodeDataList[key]
      nodeData['selected'] = False

  def getSelectedNodeData(self):
    settings = self.dataContainer.nodeDataSettings
    for key in settings:
      setting = settings.get(key)
      if setting.get("selected") != None:
        return self.dataContainer.nodeDataList.get(key)
    return None



# Setting the status of the data
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

  def removeFoldedState(self, data, allStateData):
    state = allStateData.get(data.get(NodeManager.ID))
    newState = copy.deepcopy(state)
    newState.pop(NodeManager.FOLDED, None)
    return newState
  
#Getter and setter
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
    removed = self.removeChildren(data, nData)

    newAllData = copy.deepcopy(removed)
    newAllData.pop(data.get(NodeManager.ID), None)

    return self.removeIdFromParent(data, newAllData)

  def removeChildren(self, data, allData):
    childrenIds = data.get(NodeManager.CHILDREN_IDS)
    if childrenIds is not None:
      for id in childrenIds:
        childData = allData.get(id)
        allData.pop(id, None)
        self.removeChildren(childData, allData)
    return allData

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



        
        
        
        
        
        
        
        
        
        
        
        
