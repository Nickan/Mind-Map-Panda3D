import itertools
from collections import defaultdict
from pprint import pprint

from direct.showbase.ShowBase import Vec3
from scenes.mapComponents.nodeDrawing import NodeDrawing


from utils.reingoldTilford import ReingoldTilford
from utils.utils import Utils
from platform import node

import copy


class NodeManager():

  def __init__(self):
    self.nodeDrawings = {}
    self.nodeDataList = {}
    self.tree = ReingoldTilford()
    self.selectedNodeData = None


  def renderNodeData(self, loader, mapNode, nodeData, pos):
    self.addNodeDrawing(nodeData, loader, mapNode, pos)


  def addNodeDrawing(self, nodeData, loader, mapNode, pos = Vec3()):
    id = nodeData.get('id')
    text = nodeData.get('name')
#     text = "id " + str(id) + " x " + str(nodeData['x']) + "y " + str(nodeData['depth']) # For debugging
    selected = nodeData.get('selected')
    
    
    nodeDrawing = NodeDrawing(text, loader, mapNode)
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
        return self.nodeDataList[key]
    return None
  
  def getNodeDataId(self, nodeData):
    for key in self.nodeDataList:
      if nodeData == self.nodeDataList[key]:
        return key
    
    
  def showCoords(self, coords):
    for depth, coordDepth in enumerate(dummyCoords):
      for coordBreadth in coordDepth:
        print("point " + str(depth) + ": " + str(coordBreadth))
        
  
  
  def createNodeData(self, parentId, name, recheckLastId):
    self.tmpClearNodes()
    
    newNodeData = {}
    
    if parentId is not None:
      newNodeData['parentId'] = parentId
      
    newNodeData['id'] = Utils.getUniqueId(self.nodeDataList, recheckLastId)
    newNodeData['name'] = name
    self.nodeDataList[newNodeData['id']] = newNodeData
    
    parentData = self.nodeDataList.get(parentId)
    if parentData is not None:
      newNodeData["depth"] = parentData.get("depth") + 1
      
      children = parentData.get('childrenIds')
      if children is None:
        parentData['childrenIds'] = []
      parentData['childrenIds'].append(newNodeData['id'])
    else:
      newNodeData["depth"] = 1
    
    return newNodeData
  
  def deleteNodeData(self, nodeDataToDelete):
    if nodeDataToDelete["id"] == 1:
      print("Can't delete Main node")
      return
    
    self.removeFromParentChildrenIdList(nodeDataToDelete)
    self.deleteNodeAndChildren(nodeDataToDelete)
    
    
  def removeFromParentChildrenIdList(self, nodeDataToDelete):
    parentId = nodeDataToDelete["parentId"]
    parentNodeData = self.nodeDataList[parentId]
    
    childrenIds = parentNodeData.get('childrenIds')
    if childrenIds is not None:
      childrenIds.remove(nodeDataToDelete["id"])
      # Temp
      if len(childrenIds) == 0:
        parentNodeData.pop('childrenIds')
    
  def deleteNodeAndChildren(self, nodeData):
    self.nodeDataList.pop(nodeData["id"])
    childrenIds = nodeData.get("childrenIds")
    
    if childrenIds is not None:
      for childId in childrenIds:
        childData = self.nodeDataList[childId]
        self.deleteNodeAndChildren(childData)
        
        
        
  
  ##################### Utils  
  def tmpClearNodes(self):
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
        nodeData = self.nodeDataList[key]
      else:
        nodeData = nodeDataList[key]
      nodeData['selected'] = False
    
        
        
        
        
        
        
        
        
        
        
        
        
        
