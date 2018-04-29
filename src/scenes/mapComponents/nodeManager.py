from scenes.mapComponents.node import Node

from direct.showbase.ShowBase import Vec3

from pprint import pprint

class NodeManager():

  def __init__(self):
    self.nodes = []

  def loadJson(self, loader, mapNode, jsonData):
    pprint(jsonData)
    

  def addNode(self, loader, mapNode, pos = Vec3()):
    newNode = Node(loader, mapNode)
    newNode.model.setPos(pos)

    self.nodes.append(newNode)