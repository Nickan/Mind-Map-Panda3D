from scenes.mapComponents.nodeData import NodeData
from state import State
from stateManager import StateManager

from utils.saveManager import SaveManager


class FoldNode(State):
  FOLDED = "folded"

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
    selected = nodeManager.getSelectedNodeData()
    selectedNodeId = selected.get(NodeData.ID)
    nodeDataSettings = nodeManager.dataContainer.nodeDataSettings

    nodeSettings = nodeDataSettings.get(selectedNodeId)

    if nodeSettings is not None:
      folded = nodeSettings.get(FoldNode.FOLDED)
      if folded != None:
        nodeSettings.pop(FoldNode.FOLDED, None)
      else:
        nodeSettings[FoldNode.FOLDED] = True
    else:
      nodeSettings = { FoldNode.FOLDED: True }

    nodeManager.dataContainer.nodeDataSettings = nodeDataSettings

    StateManager.switchToLoadMapState(self)
    


  