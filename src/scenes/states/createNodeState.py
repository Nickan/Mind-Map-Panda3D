from state import State
from stateManager import StateManager

from utils.utils import Utils


class CreateNodeState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self, selectedNodeData):
    self.setupControls()
    nodeManager = self.map.nodeManager
    nodeManager.selectedNodeData = selectedNodeData
    
    
    self.tmpCreatePotentialNewNode(nodeManager, selectedNodeData)
    Utils.createTextInput(self.onEnterText)
    
  def setupControls(self):
    map = self.map
    map.showBase.accept("mouse1", self.mouse1Down)
    
  def exit(self):
    print("exit CreateNodeState")
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
    pos = nodeManager.getNodeDrawingPos(self.tmpNewNodeData)
#         Need way how to pass the position to convert to screen coords
    print("Node pos " + str(pos))






