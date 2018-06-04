from state import State
from stateManager import StateManager

class DeleteNodeDataState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self, selectedNodeData):
    nodeManager = self.map.nodeManager
    nodeManager.selectedNodeData = selectedNodeData
    self.map.deleteNodeData(nodeManager.selectedNodeData)
    nodeManager.selectedNodeData = None
    StateManager.switchToStaticMapState(self)
    
  
  def exit(self):
    self.map.showBase.ignoreAll()
    self.map.showBase.taskMgr.remove("mouseMove")