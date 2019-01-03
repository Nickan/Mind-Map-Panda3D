from scenes.map import Map
from scenes.mapComponents.nodeDataFilter import NodeDataFilter
from .state import State
from .stateManager import StateManager

from utils.saveManager import SaveManager



class LoadMapState(State):
  
  def __init__(self, showBase, allData, allStateData, camDict):
    State.__init__(self)
    self.map = Map(showBase, allData, allStateData, camDict)
    self.map.state = self
    
  def enter(self):
    self.map.drawData()
    StateManager.switchToStaticMapState(self)    
    
  def exit(self):
    self.map.showBase.ignoreAll()
    
    
    