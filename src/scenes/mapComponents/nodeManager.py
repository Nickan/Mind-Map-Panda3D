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
  SELECTED = "selected"

  def __init__(self):
    # Will be mutated
    self.allDrawingData = {}
    self.allData = {}
    self.allStatusData = {}

    self.tree = ReingoldTilford()


#First level functions
  def createNodeData(self, parentId, name, recheckLastId, allData,
    getUniqueId):

    newData = {}
    newData['parentId'] = parentId
    newData['name'] = name
    parentData = allData.get(parentId)
    self.addToParent(newData, parentData)
    self.setDepth(newData, parentData)

    newData['id'] = getUniqueId(allData, recheckLastId)
    return newData
    # allData[newData['id']] = newData
    # return newData, allData

  def getFilteredData(self, allData, allStatusData):
    return NodeDataFilter.getFilteredData(allData, allStatusData)
    

  def drawData(self, filteredData, allStatusData, loader, mapNode,
    getNodePosition):
    for key in filteredData:
      nodeData = filteredData.get(key)
      settings = allStatusData.get(key)

      breadth = nodeData.get("x")
      depth = nodeData.get("depth")
      pos = getNodePosition(depth, breadth)

      self.addNodeDrawing(nodeData, settings, loader, mapNode, pos)

  def removeAllSelectedField(allStatusData):
    nallStatusData = copy.deepcopy(allStatusData)
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
    nodeDataList = self.dataContainer.nodeDataList
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

        
        
        
        
        
        
        
        
        
        
        
        
