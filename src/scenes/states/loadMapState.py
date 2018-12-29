from scenes.map import Map
from scenes.mapComponents.nodeDataFilter import NodeDataFilter
from .state import State
from .stateManager import StateManager

from utils.saveManager import SaveManager



class LoadMapState(State):
  
  def __init__(self, map, allData, allStatusData):
    State.__init__(self)
    map.dispose()
    self.map = Map(map.showBase, allData, allStatusData)
    self.map.state = self
    
  def enter(self):
    self.map.drawData()
    StateManager.switchToStaticMapState(self)    
    
  def exit(self):
    self.map.showBase.ignoreAll()
    
    
    