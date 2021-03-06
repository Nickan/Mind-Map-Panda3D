from direct.showbase.ShowBase import ShowBase

from panda3d.core import AntialiasAttrib
from panda3d.core import NodePath
from panda3d.core import TextNode
from panda3d.core import BitMask32
from panda3d.core import TextProperties, VBase4, ColorAttrib, TransparencyAttrib

# from .nodeManager import NodeManager
from utils.utils import Utils

class NodeDrawing():
  
  ONE_LINE_TEXT_HEIGHT = 0
  
  def __init__(self, text, loader, parentNodePath, id):
    self.scale = Utils.NODE_SCALE
    
    self.mainNode = NodePath("Node")
    self.mainNode.reparentTo(parentNodePath)
    
    self.addText(text, self.mainNode)
    self.addModel(loader, self.mainNode)
    
    self.mainNode.setTag("Node", self.textNode.getText())
    self.mainNode.setCollideMask(BitMask32.bit(1))
    self.keepTextCenter()
    self.id = id
    
    
  def addModel(self, loader, nodePath):
    self.model = loader.loadModel("../models/capsule")
    self.model.setScale(self.scale)
    self.model.reparentTo(nodePath)
    self.model.setPos(0, 0, 0)
    self.model.setTransparency(TransparencyAttrib.MAlpha)

  def addText(self, text, nodePath):
    self.textNode = TextNode("Node 1") # This should be different for every instance?
    
    #this is case-sensitive
    from scenes.map import Map
    
    textNode = self.textNode
    self.textNode.setFont(Map.FONT_UBUNTU)
    self.textNode.setAlign(TextProperties.A_center)
    textNode.setWordwrap(Utils.NODE_SCALE.x * 1.4)
    
    self.textNode.setText(text)
    self.textNode.setTextColor(0, 0, 0, 1)
    
    
    self.text3d = NodePath(self.textNode)
    self.text3d.reparentTo(nodePath)
    self.text3d.setHpr(0, 90, 0)
    self.text3d.setTwoSided(True)

    self.text3d.setScale(2, 0.1, 2)
    # self.text3d.setScale(1, 1, 1)
    self.text3d.setAntialias(AntialiasAttrib.MAuto)
    
  
  def dispose(self):
    self.mainNode.removeNode()
    
  
  def keepTextCenter(self):
    lineRows = self.textNode.getNumRows()
    if lineRows == 0:
      return NodeDrawing.ONE_LINE_TEXT_HEIGHT
    
    textHeight = lineRows * NodeDrawing.ONE_LINE_TEXT_HEIGHT
    oneLineHeight = textHeight / lineRows
    
    heightAdj = 0
    if lineRows == 1:
      heightAdj = (textHeight / 2)
    else:
      heightAdj = (oneLineHeight / 1) - (textHeight / 1.5)
    self.text3d.setPos(0, heightAdj, -1)
    
  """ Calculates text height based on the created tightbounds 
      might not be the accurate height of the text """
  def getActualTextHeight(self):
    text = self.textNode.getText()
    if len(text) < 1:
      return 0
    
    if self.text3d.getTightBounds() is None:
      return 0
    
    pt1, pt2 = self.text3d.getTightBounds()
    width = pt2.getX()  - pt1.getX()
    height = pt2.getY() - pt1.getY()
    return height
  
  
  def setSelected(self, stateData, alpha = 1):
    from .nodeManager import NodeManager
    if stateData is None:
      self.model.setColor(1, 1, 1, 1)
      self.model.setAlphaScale(1)
      return

    selected = stateData.get(NodeManager.SELECTED)
    folded = stateData.get(NodeManager.FOLDED)

    if selected and folded is None:
      self.model.setColor(1, 0.84, 0, 1)
    elif selected and folded:
      self.model.setColor(0, 0.5, 1, 1)
    elif selected is None and folded:
      self.model.setColor(0.84, 0.85, 0.86, 1)

    self.model.setTransparency(TransparencyAttrib.MAlpha)
    self.model.setAlphaScale(alpha)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    