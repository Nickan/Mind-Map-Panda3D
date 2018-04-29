from scenes.mapComponents.node import Node

from direct.showbase.ShowBase import Vec3


class NodeManager():

  def __init__(self):
    self.nodes = []


  def addNode(self, loader, mapNode, pos = Vec3(4, 0, 1)):
    newNode = Node(loader, mapNode)
    newNode.model.setPos(pos)

    self.nodes.append(newNode)