import itertools
from collections import defaultdict
from pprint import pprint

from direct.showbase.ShowBase import Vec3
from scenes.mapComponents.node import Node


from utils.reingoldTilford import ReingoldTilford
from utils.utils import Utils


class NodeManager():
  DEPTH_DIST = 5
  BREADTH_DIST = 15

  def __init__(self):
    self.init = []
    self.nodes = []
    self.tree = ReingoldTilford()

  def loadJson(self, loader, mapNode, jsonData):
    coords = self.tree.getCoordinates(jsonData)
    self.render(loader, mapNode, jsonData)

  def render(self, loader, mapNode, nodeList):
    for key in nodeList:
      nodeData = nodeList[key]
      x = nodeData.get("x") * NodeManager.BREADTH_DIST
      y = int(nodeData.get("depth")) * NodeManager.DEPTH_DIST
      z = 1

      pos = Vec3(x, y, z)

      name = nodeData.get('name') + " x " + str(x) + " y " + str(y)
      self.addNode(name, loader, mapNode, pos)


  
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

  def addNode(self, text, loader, mapNode, pos = Vec3()):
    newNode = Node(text, loader, mapNode)
    newNode.mainNode.setPos(pos)

    self.nodes.append(newNode)


  def showCoords(self, coords):
    for depth, coordDepth in enumerate(dummyCoords):
      for coordBreadth in coordDepth:
        print("point " + str(depth) + ": " + str(coordBreadth))







    # # pprint(jsonData)
    # self.mapNode = mapNode # might not be needed later on

    # # name = jsonData.get('name')
    # # self.addNode(name, loader, mapNode)
    # # self.traverseJsonData(loader, jsonData)

    # nodeList = self.convertJsonDataToListNodes(jsonData)
    # self.createNodes(listNodes)
    

  # def createNodes(self, nodeList):
  #   for index, node in enumerate(nodeList):
  #     children = node.get("children")
  #     if children is not None:
  #       for child in children:
  #         print("index at " + str(index) + " parent: " + node.get("name") +
  #         " child " + child.get("name"))



  #       # depthDistBetweenChildren = NodeManager.DEPTH_DIST
  #       # breadthDistBetweenChildren = NodeManager.BREADTH_DIST


  #       # childrenCount = len(children)
  #       # totalBreadthDist = breadthDistBetweenChildren * (childrenCount - 1)
  #       # startingBreadth = -totalBreadthDist / 2
        
  #       # tempParent = self.mapNode

  #       # x = depthDistBetweenChildren
  #       # z = 1 # Might change later
  #       # for index, child in enumerate(children):
  #       #   y = startingBreadth + (breadthDistBetweenChildren * index)
  #       #   pos = Vec3(x, y, z)
  #       #   self.addNode(child.get('name'), loader, tempParent, pos)


  # def traverseJsonData(self, loader, jsonData):
  #   children = jsonData.get('children')
  #   self.createChildren(None, children, loader, 
  #     NodeManager.DEPTH_DIST, NodeManager.BREADTH_DIST)

  # # Notes
  #   # Position the children
  #   #   Relative to parents local coordinates
  #   #   Separate the nodes into 2 group
  #   #     Based on parents local coordinates
  #   #       First group will go in the y positive
  #   #       Last ground will go in the y negative
  #   # Define the formula
  #   # Do this step by step

  #   # Notes
  #   # Depth axis can be x or y, z if wish to
    
  #   # Others
  #   # There might be a better way to traverse json
  #   #   Useful for address node implementation
  #   #   *Solve later
  # def createChildren(self, parent, children, loader,
  #   depthDistBetweenChildren, breadthDistBetweenChildren):

  #   childrenCount = len(children)
  #   totalBreadthDist = breadthDistBetweenChildren * (childrenCount - 1)
  #   startingBreadth = -totalBreadthDist / 2
    
  #   tempParent = self.mapNode

  #   x = depthDistBetweenChildren
  #   z = 1 # Might change later
  #   for index, child in enumerate(children):
  #     y = startingBreadth + (breadthDistBetweenChildren * index)
  #     pos = Vec3(x, y, z)
  #     self.addNode(child.get('name'), loader, tempParent, pos)

  # # Notes
  #   # Iterate through all names and children
  #   # Add it to list
  #     # Conversion
  #     # list
  #       # Map
  # def convertJsonDataToListNodes(self, jsonData):
  #   nodeList = []
  #   name = jsonData.get('name')
  #   nodeList.append([{ "name": name }])

  #   currentDepthParentList = []
  #   nextDepthParentList = [jsonData]
  #   while len(nextDepthParentList) > 0:
  #     currentDepthParentList = nextDepthParentList
  #     nextDepthParentList = []

  #     nodes, nextDepthParentList = self.convertToNodeAndGetNextParentsDepth(
  #       currentDepthParentList)

  #     nodeList.append(node)

  #   return nodeList
    

  # def convertToNodeAndGetNextParentsDepth(self, currentDepthParentList):
  #   node
  #   nextDepthParentList = []

  #   while len(currentDepthParentList) > 0:
  #     parent = currentDepthParentList[0]
  #     currentDepthParentList.remove(parent)

  #     children = parent.get("children")
  #     parentName = parent.get("name")

  #     if children is not None:
  #       # Iterating to all its children
  #       node = { "name": parentName, "children": children }

  #       for child in children:
  #         grandChildren = child.get('children')
  #         if grandChildren is not None:
  #           nextDepthParentList.append(child)

        
    
  #   return node, nextDepthParentList
      
  # def showNodeList(self, nodeList):
  #   for index, nodes in enumerate(nodeList):
  #     for node in nodes:
  #       print("index at " + str(index) + " " + node.get("name"))




# Brain dump algorithm
  # Breadth positioning calculation
  # Conditions
  #   The parent will always be in the middle
  #   Try out:
  #     Parent node should only position their child node
  #       A one-tier positioning formula

  # System
    # Positioning
    #   Hierarchial
    #     Depth
    #       Fixed
    #     Breadth
    #       Based on the number of the children in the bottom most end 
    #        of the hierarchy
