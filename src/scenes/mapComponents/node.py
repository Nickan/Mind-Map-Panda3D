from direct.showbase.ShowBase import ShowBase

from panda3d.core import NodePath
from panda3d.core import TextNode

class Node():

  def __init__(self, text, loader, nodePath):
    # self.showBase = showBase

    self.mainNode = NodePath("Node")
    self.mainNode.reparentTo(nodePath)

    self.addModel(loader, self.mainNode)
    self.addText(text, self.mainNode)

  def addModel(self, loader, nodePath):
    self.model = loader.loadModel("../models/capsule") 
    scale = 1
    # self.model.setScale(4, 4, scale)
    self.model.reparentTo(nodePath)

  def addText(self, text, nodePath):
    self.text = TextNode("Node 1") # This should be different for every instance?
    self.text.setText(text)
    self.text.setTextColor(0, 0, 1, 1)
    self.text.setAlign(TextNode.A_center)
    
    
    self.text3d = NodePath(self.text)
    self.text3d.reparentTo(nodePath)
    self.text3d.setPos(0, 0, -0.7)
    self.text3d.setHpr(0, 90, 0)
    self.text3d.setTwoSided(True)

    self.text3d.setScale(2, 2, 2)