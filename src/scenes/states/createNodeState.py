from state import State
from stateManager import StateManager

from utils.keyManager import KeyManager
from utils.saveManager import SaveManager
from utils.utils import Utils



class CreateNodeState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self, selectedNodeData):
    self.setupControls()
    nodeManager = self.map.nodeManager
    nodeManager.selectedNodeData = selectedNodeData
    
    self.tmpNewNodeData = self.tmpCreatePotentialNewNode(nodeManager, selectedNodeData)
    SaveManager.clearNodeDataList(nodeManager.nodeDataList)
    
    self.map.drawNodeDataList(nodeManager.nodeDataList)
    KeyManager.setupKeyListener(self.map.showBase, self.onKeyDown)
    
  def onKeyDown(self, keyname):
    nodeManager = self.map.nodeManager
    self.tmpNodeDrawing = nodeManager.getNodeDrawing(self.tmpNewNodeData)
    text = self.tmpNodeDrawing.textNode.getText()
    text = KeyManager.getModifiedKeyFromKeyInput(text, keyname, self.onEnterDown)
        
    textNode = self.tmpNodeDrawing.textNode
    textNode.setText(text)
    self.tmpNodeDrawing.keepTextCenter()
    
  def onEnterDown(self, text):
    self.map.editNodeData(self.tmpNewNodeData, text)
    StateManager.switchToStaticMapState(self)
    
    
    
  def setupControls(self):
    map = self.map
    map.showBase.accept("mouse1", self.mouse1Down)
    
  def exit(self):
    KeyManager.clear()
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
    
    self.map.deleteNodeData(self.tmpNewNodeData)
    self.tmpNewNodeData = None
    StateManager.switchToStaticMapState(self)
    
    
  def tmpCreatePotentialNewNode(self, nodeManager, selectedNodeData):
    id = nodeManager.getNodeDataId(nodeManager.selectedNodeData)
    self.tmpNewNodeData = nodeManager.createNodeData(id, "", False)
    return self.tmpNewNodeData






