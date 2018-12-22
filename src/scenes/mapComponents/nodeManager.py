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


class NodeManager():
  SELECTED = "selected"

  def __init__(self):
    self.nodeDrawings = {}
    self.unfilteredData = {}
    self.filteredData = {}
    self.settingsOfData = {}
    self.tree = ReingoldTilford()
    self.selectedNodeData = None


#First level functions
  def createNodeData(self, parentId, name, unfilteredData, recheckLastId):
    self.tmpClearNodeDrawings()
    
    newNodeData = {}
    newNodeData['parentId'] = parentId
    #Have to check Utils.getUniqueId() later on
    newNodeData['id'] = Utils.getUniqueId(unfilteredData, recheckLastId)
    newNodeData['name'] = name

    parentData = unfilteredData.get(parentId)
    self.addToParent(newNodeData, parentData)
    self.setDepth(newNodeData, parentData)

    newFD = copy.deepcopy(unfilteredData)
    newFD[newNodeData['id']] = newNodeData
    return newNodeData, newFD



  def renderNodeData(self, loader, mapNode, nodeData, nodeSettings, pos):
    self.addNodeDrawing(nodeData, nodeSettings, loader, mapNode, pos)


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

    self.nodeDrawings[id] = nodeDrawing
    
  
  """ TODO, implementation needs to be changed """
  def getNodeData(self, nodePath):
    nodePath = nodePath.findNetTag("Node")
    
    for key in self.nodeDrawings:
      nodeDrawing = self.nodeDrawings[key]
      if nodePath == nodeDrawing.mainNode:
        return self.dataContainer.nodeDataList[key]
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
  def tmpClearNodeDrawings(self):
    for key in self.nodeDrawings:
      self.nodeDrawings[key].dispose()
    self.nodeDrawings = {}
    
    
  
  def getNodeDrawing(self, nodeData):
    return self.nodeDrawings[nodeData["id"]]
  
  def getNodeDrawingPos(self, nodeData):
    nodeDrawing = self.getNodeDrawing(nodeData)
    return nodeDrawing.mainNode.getPos()
  
  
  def setNodeSelected(self, nodeData, nodeDataList = None):
    self.setAllAsUnselected(nodeDataList)
    selectedNodeDrawing = self.getNodeDrawing(nodeData)
    selectedNodeDrawing.setSelected(True)
    
  def setAllAsUnselected(self, nodeDataList = None):
    for key in self.nodeDrawings:
      nodeDrawing = self.nodeDrawings[key]
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


#Second Level functions
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



    
        
        
        
        
        
        
        
        
        
        
        
        
        
