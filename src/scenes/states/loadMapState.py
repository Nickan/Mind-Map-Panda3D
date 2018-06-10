from state import State
from stateManager import StateManager


class LoadMapState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self, nodeDataList):
    nodeManager = self.map.nodeManager
    nodeManager.nodeDataList = nodeDataList
    nodeManager.tree.getCoordinates(nodeDataList)
    
    self.map.drawNodeDataList(nodeDataList)
    StateManager.switchToStaticMapState(self)
    
    
  def exit(self):
    self.map.showBase.ignoreAll()
    
    
    