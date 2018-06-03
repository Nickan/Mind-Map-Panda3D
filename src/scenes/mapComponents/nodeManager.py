import itertools
from collections import defaultdict
from pprint import pprint

from direct.showbase.ShowBase import Vec3
from scenes.mapComponents.node import Node


from utils.reingoldTilford import ReingoldTilford
from utils.utils import Utils
from platform import node

import copy


class NodeManager():

  def __init__(self):
    self.nodes = {}
    self.nodeData = {}
    self.tree = ReingoldTilford()

  def loadJson(self, loader, mapNode, jsonData):
    coords = self.tree.getCoordinates(jsonData)
    self.render(loader, mapNode, jsonData)

  def render(self, loader, mapNode, nodeList):
    for key in nodeList:
      tmpNodeData = nodeList[key]
      x = tmpNodeData.get("x") * Utils.BREADTH_DIST
      y = int(tmpNodeData.get("depth")) * Utils.DEPTH_DIST
      z = 1

      pos = Vec3(x, y, z)

#       name = tmpNodeData.get('name') + " x " + str(x) + " y " + str(y)
      self.addNodeGraphics(key, tmpNodeData.get('name'), loader, mapNode, pos)


  
  def createChildren(self, parent, children, loader,
    depthDistBetweenChildren, breadthDistBetweenChildren):

    childrenCount = len(children)
    totalBreadthDist = breadthDistBetweenChildren * (childrenCount - 1)
    startingBreadth = -totalBreadthDist / 2
    
    tempParent = self.mapNode

    x = depthDistBetweenChildren
    z = 1 # Might change later
    for index, child in enumerate(children):
      y = startingBreadth + (breadthDistBetweenChildren * index)
      pos = Vec3(x, y, z)
      self.addNode(child.get('name'), loader, tempParent, pos)

  def addNodeGraphics(self, id, text, loader, mapNode, pos = Vec3()):
    nodeGraphics = Node(text, loader, mapNode)
    nodeGraphics.mainNode.setPos(pos)

    self.nodes[id] = nodeGraphics
    
  
  def getNode(self, nodePath):
    nodePath = nodePath.findNetTag("Node")
    
    for key in self.nodes:
      node = self.nodes[key]
      if nodePath == node.mainNode:
        return node
    return None
  
  def getNodeId(self, node):
    for key in self.nodes:
      if node == self.nodes[key]:
        return key
    
    
  def showCoords(self, coords):
    for depth, coordDepth in enumerate(dummyCoords):
      for coordBreadth in coordDepth:
        print("point " + str(depth) + ": " + str(coordBreadth))
        
  
  
  def createNode(self, parentId, name, loader, mapNode):
    self.tmpClearNodes()
    
    childNodeData = {}
    
    if parentId is not None:
      childNodeData['parentId'] = parentId
      
      
    childNodeData['id'] = Utils.getUniqueId()
    childNodeData['name'] = name
    self.nodeData[childNodeData['id']] = childNodeData
    
    parentNodeData = self.nodeData.get(parentId)
    if parentNodeData is not None:
      childNodeData["depth"] = parentNodeData.get("depth") + 1
      
      children = parentNodeData.get('childrenIds')
      if children is None:
        parentNodeData['childrenIds'] = []
      parentNodeData['childrenIds'].append(childNodeData['id'])
    else:
      childNodeData["depth"] = 1
    
    self.loadJson(loader, mapNode, self.nodeData)
    
    
  def tmpClearNodes(self):
    for key in self.nodes:
      self.nodes[key].dispose()
    self.nodes = {}
    
    
        
        
        
        
        
        
        
        
        
        
        
        
        
