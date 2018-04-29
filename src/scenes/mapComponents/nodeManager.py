from scenes.mapComponents.node import Node

from direct.showbase.ShowBase import Vec3

from pprint import pprint

class NodeManager():
  DEPTH_DIST = 10
  BREADTH_DIST = 6

  def __init__(self):
    self.nodes = []

  def loadJson(self, loader, mapNode, jsonData):
    pprint(jsonData)

    name = jsonData.get('name')
    self.addNode(name, loader, mapNode)
    children = jsonData.get('children')

    depth = 1
    breadth = 1
    while children is not None:
      for child in children:
        name = child.get('name')

        depthDist = depth * NodeManager.DEPTH_DIST
        breadthDist = breadth * NodeManager.BREADTH_DIST
        pprint(depthDist)
        self.addNode(name, loader, mapNode, Vec3(depthDist, breadthDist, 0))

        breadth += 1
        # assignation of breadth distances is temporary
      depth += 1

      children = child.get('children')


    
    # System
    # Positioning
    #   Hierarchial
    #     Depth
    #       Fixed
    #     Breadth
    #       Based on the number of the children in the bottom most end 
    #        of the hierarchy

  def addNode(self, text, loader, mapNode, pos = Vec3()):
    newNode = Node(text, loader, mapNode)
    newNode.mainNode.setPos(pos)

    self.nodes.append(newNode)