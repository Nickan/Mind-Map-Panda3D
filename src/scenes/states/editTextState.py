from state import State
from stateManager import StateManager

from utils.utils import Utils

class EditTextState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self, selectedNodeData):
    nodeManager = self.map.nodeManager
    nodeManager.selectedNodeData = selectedNodeData
    Utils.createTextInput(self.onEnterText)
    
  def exit(self):
    self.map.showBase.ignoreAll()
    
  
  """ enter() Helpers """
  def onEnterText(self, newText):
    nodeManager = self.map.nodeManager
    self.map.editNodeData(nodeManager.selectedNodeData, newText)
    StateManager.switchToStaticMapState(self)
