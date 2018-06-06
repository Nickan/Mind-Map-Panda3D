from direct.showbase.ShowBase import ShowBase

from panda3d.core import AntialiasAttrib
from panda3d.core import NodePath
from panda3d.core import TextNode
from panda3d.core import BitMask32
from panda3d.core import TextProperties

from utils.utils import Utils

class NodeDrawing():
  
  def __init__(self, text, loader, parentNodePath):
    self.scale = Utils.NODE_SCALE
    
    self.mainNode = NodePath("Node")
    self.mainNode.reparentTo(parentNodePath)
    
    self.addText(text, self.mainNode)
    self.addModel(loader, self.mainNode)
    
    self.mainNode.setTag("Node", self.textNode.getText())
    self.mainNode.setCollideMask(BitMask32.bit(1))
    self.keepTextCenter()
    
    
  def addModel(self, loader, nodePath):
    self.model = loader.loadModel("../models/capsule") 
    self.model.setScale(self.scale)
    self.model.reparentTo(nodePath)
    
    

  def addText(self, text, nodePath):
    self.textNode = TextNode("Node 1") # This should be different for every instance?
    
     #this is case-sensitive
    from scenes.map import Map
    
    textNode = self.textNode
    self.textNode.setFont(Map.FONT_UBUNTU)
    self.textNode.setAlign(TextProperties.A_center)
    textNode.setWordwrap(Utils.NODE_SCALE.x * 1.4)
    
    self.textNode.setText(text)
    self.textNode.setTextColor(0, 0, 1, 1)
#     self.textNode.setAlign(TextNode.A_center)
    
    
    self.text3d = NodePath(self.textNode)
    self.text3d.reparentTo(nodePath)
    self.text3d.setPos(0, 0, -2)
    self.text3d.setHpr(0, 90, 0)
    self.text3d.setTwoSided(True)

    self.text3d.setScale(2, 2, 2)
#     self.text3d.setScale(1, 1, 1)
    self.text3d.setAntialias(AntialiasAttrib.MAuto)
    
  
  def setClicked(self, isClicked = True):
    if isClicked:
      self.model.setColor(0.9, 0.9, 0.9, 1)
      
  
  def dispose(self):
    self.mainNode.removeNode()
    
  
  def keepTextCenter(self):
    textHeight = self.getTextHeight()
    
    if textHeight == 0:
      return
    
    
    lineRows = self.textNode.getNumRows()
    oneLineHeight = textHeight / lineRows
    
    heightAdj = 0
    if lineRows == 1:
      heightAdj = (textHeight / 2)
    else:
      heightAdj = (oneLineHeight / 1) - (textHeight / 1.5)
    self.text3d.setPos(0, heightAdj, -2)
    
  def getTextHeight(self):
    text = self.textNode.getText()
    if len(text) < 1:
      return 0
    
    if self.text3d.getTightBounds() is None:
      return 0
    
    
    pt1, pt2 = self.text3d.getTightBounds()
    width = pt2.getX()  - pt1.getX()
    height = pt2.getY() - pt1.getY()
    return height
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    