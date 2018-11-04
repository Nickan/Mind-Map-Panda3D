from scenes.mapComponents.nodeDataFilter import NodeDataFilter
from state import State
from stateManager import StateManager

from utils.saveManager import SaveManager



class LoadMapState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self):
    nodeManager = self.map.nodeManager
    nodeManager.selectedNodeData = None
    dataContainer = nodeManager.dataContainer

    nodeDataFilter = NodeDataFilter()
    dataContainer.nodeDataList = nodeDataFilter.getFilteredNodeData(dataContainer)

    SaveManager.clearNodeDataList(dataContainer.nodeDataList)
    nodeManager.tree.getCoordinates(dataContainer.nodeDataList)
    
    self.map.drawNodeData(dataContainer)
    self.map.setCameraViewToSelectedNode()

    StateManager.switchToStaticMapState(self)
    
    
  def exit(self):
    self.map.showBase.ignoreAll()
    
    
    