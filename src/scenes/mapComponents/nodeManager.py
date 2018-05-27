import itertools
from collections import defaultdict
from pprint import pprint

from direct.showbase.ShowBase import Vec3
from scenes.mapComponents.node import Node


from utils.reingoldTilford import ReingoldTilford
from utils.utils import Utils


class NodeManager():

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
      x = nodeData.get("x") * Utils.BREADTH_DIST
      y = int(nodeData.get("depth")) * Utils.DEPTH_DIST
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
