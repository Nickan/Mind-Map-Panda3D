from state import State
from stateManager import StateManager

from utils.utils import Utils
from utils.coordManager import CoordManager

from panda3d.core import ModifierButtons


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
    
    self.setupRealTimeTypingOnNodeDrawing()

  def setupRealTimeTypingOnNodeDrawing(self):
    showBase = self.map.showBase
    showBase.buttonThrowers[0].node().setButtonDownEvent('buttonDown')
    showBase.accept('buttonDown', self.onButtonDown)
    
    
    
  def onButtonDown(self, keyname):
    text = self.tmpNodeDrawing.textNode.getText()
    if keyname == "backspace":
      text = text[:-1]
    else:
      if len(keyname) == 1:
        text += keyname
       
      if keyname == "space":
        text += " "
        
      if keyname == "enter":
        self.map.editNodeData(self.tmpNewNodeData, text)
        StateManager.switchToStaticMapState(self)
        
    self.tmpNodeDrawing.textNode.setText(text)
    

    
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
    if self.map.clickedOutsideTextInput():
      self.onClickedOutsideTextInput()
    
    
  def onClickedOutsideTextInput(self):
    Utils.closeTextInput()
    StateManager.switchToStaticMapState(self)
    self.map.deleteNodeData(self.tmpNewNodeData)
    self.tmpNewNodeData = None
    
    
  def tmpCreatePotentialNewNode(self, nodeManager, selectedNodeData):
    id = nodeManager.getNodeDataId(nodeManager.selectedNodeData)
    self.tmpNewNodeData = self.map.createNodeData(id, "")
    return self.tmpNewNodeData






