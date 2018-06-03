from direct.showbase.ShowBase import ShowBase

from panda3d.core import AntialiasAttrib
from panda3d.core import NodePath
from panda3d.core import TextNode
from panda3d.core import BitMask32



from utils.utils import Utils




class NodeDrawing():

  def __init__(self, text, loader, nodePath):
    self.scale = Utils.NODE_SCALE
    
    self.mainNode = NodePath("Node")
    self.mainNode.reparentTo(nodePath)
    
    self.addText(text, self.mainNode)
    self.addModel(loader, self.mainNode)
    
    self.mainNode.setTag("Node", self.textNode.getText())
    self.mainNode.setCollideMask(BitMask32.bit(1))
    
    
  def addModel(self, loader, nodePath):
    self.model = loader.loadModel("../models/capsule") 
    self.model.setScale(self.scale)
    self.model.reparentTo(nodePath)
    
    

  def addText(self, text, nodePath):
    self.textNode = TextNode("Node 1") # This should be different for every instance?
    
     #this is case-sensitive
    from scenes.map import Map
    self.textNode.setFont(Map.FONT_UBUNTU)
    
    self.textNode.setText(text)
    self.textNode.setTextColor(0, 0, 1, 1)
    self.textNode.setAlign(TextNode.A_center)
    
    
    self.text3d = NodePath(self.textNode)
    self.text3d.reparentTo(nodePath)
    self.text3d.setPos(0, 0, -2)
    self.text3d.setHpr(0, 90, 0)
    self.text3d.setTwoSided(True)

    self.text3d.setScale(2, 2, 2)
    self.text3d.setAntialias(AntialiasAttrib.MAuto)
    
  
  def setClicked(self, isClicked = True):
    if isClicked:
      self.model.setColor(0.9, 0.9, 0.9, 1)
      
  
  def dispose(self):
    self.mainNode.removeNode()
#     self.mainNode.dispose()
#     self.model.dispose()
#     self.textNode.dispose()
#     self.text3d.dispose()
    
    
    
    
    
    