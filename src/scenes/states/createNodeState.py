from state import State
from stateManager import StateManager

from utils.utils import Utils
from utils.keyManager import KeyManager


class CreateNodeState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self, selectedNodeData):
    self.setupControls()
    nodeManager = self.map.nodeManager
    nodeManager.selectedNodeData = selectedNodeData
    
    self.tmpNewNodeData = self.tmpCreatePotentialNewNode(nodeManager, selectedNodeData)
    self.tmpNodeDrawing = nodeManager.getNodeDrawing(self.tmpNewNodeData)
    
    KeyManager.setupKeyListener(self.map.showBase, self.onButtonDown)
    
  def onButtonDown(self, keyname):
    text = self.tmpNodeDrawing.textNode.getText()
    
    if keyname == "\b":
      text = text[:-1]
    else:
        
      if keyname == "\r":
        self.map.editNodeData(self.tmpNewNodeData, text)
        StateManager.switchToStaticMapState(self)
        
      if keyname != "\t":
        text += keyname
        
    textNode = self.tmpNodeDrawing.textNode
    textNode.setText(text)
    self.tmpNodeDrawing.keepTextCenter()
    
    
    
  def setupControls(self):
    map = self.map
    map.showBase.accept("mouse1", self.mouse1Down)
    
  def exit(self):
    self.map.showBase.ignoreAll()
    
    
  """ enter() Helpers """
  def onEnterText(self, text):
    if text is not None:
      self.map.editNodeData(self.tmpNewNodeData, text)
      
    StateManager.switchToStaticMapState(self)
    
  def mouse1Down(self):
    if self.map.clickedOnMapBg():
      self.onClickedOutsideTextInput()
    
    
  def onClickedOutsideTextInput(self):
    StateManager.switchToStaticMapState(self)
    self.map.deleteNodeData(self.tmpNewNodeData)
    self.tmpNewNodeData = None
    
    
  def tmpCreatePotentialNewNode(self, nodeManager, selectedNodeData):
    id = nodeManager.getNodeDataId(nodeManager.selectedNodeData)
    self.tmpNewNodeData = self.map.createNodeData(id, "")
    return self.tmpNewNodeData






