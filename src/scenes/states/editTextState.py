from state import State
from stateManager import StateManager

from utils.keyManager import KeyManager
from utils.utils import Utils


class EditTextState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self, selectedNodeData):
    self.setupControls()
    nodeManager = self.map.nodeManager
    nodeManager.selectedNodeData = selectedNodeData
    
    self.nodeDrawingToEdit = nodeManager.getNodeDrawing(selectedNodeData)
    KeyManager.setupKeyListener(self.map.showBase, self.onKeyDown)
    
  def onKeyDown(self, keyname):
    text = self.nodeDrawingToEdit.textNode.getText()
    text = KeyManager.getModifiedKeyFromKeyInput(text, keyname, self.onEnterDown)
        
    textNode = self.nodeDrawingToEdit.textNode
    textNode.setText(text)
    self.nodeDrawingToEdit.keepTextCenter()
    
  def onEnterDown(self, text):
    nodeData = self.map.nodeManager.getNodeData(self.nodeDrawingToEdit.mainNode)
    self.map.editNodeData(nodeData, text)
    StateManager.switchToStaticMapState(self)
    
    
    
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
