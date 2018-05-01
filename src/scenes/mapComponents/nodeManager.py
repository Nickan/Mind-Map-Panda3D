from direct.showbase.ShowBase import Vec3
from scenes.mapComponents.node import Node

from pprint import pprint

class NodeManager():
  DEPTH_DIST = 10
  BREADTH_DIST = 6

  def __init__(self):
    self.nodes = []

  def loadJson(self, loader, mapNode, jsonData):
    pprint(jsonData)
    self.mapNode = mapNode # might not be needed later on

    name = jsonData.get('name')
    self.addNode(name, loader, mapNode)
    self.traverseJsonData(loader, jsonData)

    

  def addNode(self, text, loader, mapNode, pos = Vec3()):
    newNode = Node(text, loader, mapNode)
    newNode.mainNode.setPos(pos)

    self.nodes.append(newNode)


  def traverseJsonData(self, loader, jsonData):
    children = jsonData.get('children')
    self.createChildren(None, children, loader, 
      NodeManager.DEPTH_DIST, NodeManager.BREADTH_DIST)

  # Notes
    # Position the children
    #   Relative to parents local coordinates
    #   Separate the nodes into 2 group
    #     Based on parents local coordinates
    #       First group will go in the y positive
    #       Last ground will go in the y negative
    # Define the formula
    # Do this step by step

    # Notes
    # Depth axis can be x or y, z if wish to
    
    # Others
    # There might be a better way to traverse json
    #   Useful for address node implementation
    #   *Solve later
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