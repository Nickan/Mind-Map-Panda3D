from state import State
from stateManager import StateManager

from utils.saveManager import SaveManager


class LoadMapState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self, dataContainer):
    nodeManager = self.map.nodeManager
    nodeManager.dataContainer = dataContainer
    nodeManager.selectedNodeData = None
    SaveManager.clearNodeDataList(dataContainer.nodeDataList)
    nodeManager.tree.getCoordinates(dataContainer.nodeDataList)
    
    self.map.drawNodeData(dataContainer)
    StateManager.switchToStaticMapState(self)
    
    
  def exit(self):
    self.map.showBase.ignoreAll()
    
    
    