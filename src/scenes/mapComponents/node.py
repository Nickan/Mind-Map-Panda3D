from direct.showbase.ShowBase import ShowBase

from panda3d.core import NodePath
from panda3d.core import TextNode

class Node():

  def __init__(self, loader, nodePath):
    # self.showBase = showBase
    self.addModel(loader, nodePath)
    self.addText(nodePath)

  def addModel(self, loader, nodePath):
    self.model = loader.loadModel("../models/capsule") 
    scale = 1
    self.model.setScale(4, 4, scale)
    self.model.reparentTo(nodePath)

  def addText(self, nodePath):
    self.text = TextNode("Node 1") # This should be different for every instance?
    self.text.setText("Nickan")
    self.text.setTextColor(0, 0, 1, 1)
    self.text.setAlign(TextNode.A_center)
    
    self.text3d = NodePath(self.text)
    self.text3d.reparentTo(nodePath)
    self.text3d.setPos(0, 0, -0.7)
    self.text3d.setHpr(0, 90, 0)
    self.text3d.setTwoSided(True)