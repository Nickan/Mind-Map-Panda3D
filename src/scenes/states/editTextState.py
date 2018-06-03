from state import State
from stateManager import StateManager

from utils.utils import Utils

class EditTextState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self, selectedNodeData, map):
    nodeManager = map.nodeManager
    nodeManager.selectedNodeData = selectedNodeData
    Utils.createTextInput(self.onEnterText)
    
  def exit(self, map):
    self.map.showBase.ignoreAll()
    
  
  """ enter() Helpers """
  def onEnterText(self, newText):
    nodeManager = self.map.nodeManager
    nodeManager.editNodeData(nodeManager.selectedNodeData, newText, 
                             self.map.showBase.loader, self.map.mapNode)
    StateManager.switchToStaticMapState(self)
