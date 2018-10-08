from state import State
from stateManager import StateManager

from utils.saveManager import SaveManager
from scenes.mapComponents.nodeDataFilter import NodeDataFilter

class FoldNode(State):

  def __init__(self, map):
    State.__init__(self)
    self.map = map

  
  def enter(self):
    self.setupControls()
    self.setFoldNode()
      
  def exit(self):
    print("exit")

  def setupControls(self):
    map = self.map
    

  def setFoldNode(self):
    nodeManager = self.map.nodeManager
    selectedNodeId = nodeManager.selectedNodeData.get("id")
    nodeDataSettings = nodeManager.dataContainer.nodeDataSettings

    nodeSettings = nodeDataSettings.get(selectedNodeId)
    if nodeSettings is not None:
      if nodeSettings.get("folded") != None:
        nodeSettings["folded"] = not nodeSettings.get("folded")
      else:
        nodeSettings["folded"] = True
    else:
      nodeSettings = { "folded": True }

    dataContainer = nodeManager.dataContainer
    nodeDataList = dataContainer.nodeDataList

    nodeDataFilter = NodeDataFilter()
    nodeDataList = nodeDataFilter.getFilteredNodeData(dataContainer)
    StateManager.switchToLoadMapState(self, dataContainer)


  