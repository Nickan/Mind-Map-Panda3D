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
    self.addNodeDrawing(nodeData.get('id'), nodeData.get('name'), loader, mapNode, pos)

  def render(self, loader, mapNode, nodeDataList):
    for key in nodeDataList:
      tmpNodeData = nodeDataList[key]
      if Utils.VERTICAL_DEPTH:
        x = tmpNodeData.get("x") * Utils.VERT_BREADTH_DIST
        y = int(tmpNodeData.get("depth")) * Utils.VERT_DEPTH_DIST
      else:
        y = tmpNodeData.get("x") * Utils.HORT_BREADTH_DIST
        x = int(tmpNodeData.get("depth")) * Utils.HORT_DEPTH_DIST
      z = 1

      pos = Vec3(x, y, z)
      self.addNodeDrawing(key, tmpNodeData.get('name'), loader, mapNode, pos)


  def addNodeDrawing(self, id, text, loader, mapNode, pos = Vec3()):
    nodeDrawing = NodeDrawing(text, loader, mapNode)
    nodeDrawing.mainNode.setPos(pos)

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
    parentNodeData["childrenIds"]
    
    childrenIds = parentNodeData.get('childrenIds')
    if childrenIds is not None:
      childrenIds.remove(nodeDataToDelete["id"])
    print("test")
    
  def deleteNodeAndChildren(self, nodeData):
    self.nodeDataList.pop(nodeData["id"])
    childrenIds = nodeData.get("childrenIds")
    
    if childrenIds is not None:
      for childId in childrenIds:
        childData = self.nodeDataList[childId]
        self.deleteNodeAndChildren(childData)
        
        
        
  
    
  def tmpClearNodes(self):
    for key in self.nodeDrawings:
      self.nodeDrawings[key].dispose()
    self.nodeDrawings = {}
    
    
  #Utils
  def getNodeDrawing(self, nodeData):
    return self.nodeDrawings[nodeData["id"]]
  
  def getNodeDrawingPos(self, nodeData):
    nodeDrawing = self.getNodeDrawing(nodeData)
    return nodeDrawing.mainNode.getPos()
  
  
  def setNodeSelected(self, nodeData):
    self.setAllAsUnselected()
    selectedNodeDrawing = self.getNodeDrawing(nodeData)
    selectedNodeDrawing.setSelected(True)
    
  def setAllAsUnselected(self):
    for key in self.nodeDrawings:
      nodeDrawing = self.nodeDrawings[key]
      nodeDrawing.setSelected(False)
    
        
        
        
        
        
        
        
        
        
        
        
        
        
