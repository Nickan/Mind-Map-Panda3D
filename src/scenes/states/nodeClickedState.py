from scenes.states.components.dragNodeStartDetector import DragNodeStartDetector
from state import State
from dragNodeState import DragNodeState
from stateManager import StateManager
from utils.utils import Utils

import sys


class NodeClickedState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self):
    selectedNodeData = self.map.getSelectedNodeData()
    self.setNodeSelected(selectedNodeData)
    self.setupControls(selectedNodeData)

  
  
  def exit(self):
    self.map.showBase.ignoreAll()
    self.map.showBase.taskMgr.remove("mouseMove")
    
    
  """ enter helper """
  def setupControls(self, selectedNodeData):
    showBase = self.map.showBase
    showBase.accept('escape', sys.exit)

    showBase.accept("mouse1", self.mouse1Down)
    showBase.accept("mouse1-up", self.mouse1Up)
    showBase.accept("mouse3", self.mouse3Down)
    
    showBase.accept("tab", self.onTab)
    showBase.accept("delete", self.onDelete)
    
    self.setupDragNodeManager(selectedNodeData)

    # Temporary, have to change the control later on
    showBase.accept("f3", self.onF3Down)

    """ Events """
  def mouse1Down(self):
    print("NodeClickedState mouse1Down")
    nodeManager = self.map.nodeManager
    selectedNodeData = self.map.getSelectedNodeData()
    if selectedNodeData is None:
      self.goToScrollingState()
      self.map.state.mouse1Down()
    else:
      self.setupDragNodeManager(selectedNodeData)
      self.setNodeSelected(selectedNodeData)
    
  def mouse1Up(self):
    print("NodeClickedState mouse1Up")

  def mouse3Down(self):
    selectedNodeData = self.map.getSelectedNodeData()
    if selectedNodeData is None:
      print("None selected")
    else:
      StateManager.switchToEditTextState(self, selectedNodeData)
    
  def onTab(self):
    selectedNodeData = self.map.nodeManager.selectedNodeData
    StateManager.switchToCreateNodeDataState(self, selectedNodeData)

  def onDelete(self):
    nodeManager = self.map.nodeManager
    StateManager.switchToDeleteNodeDataState(self, nodeManager.selectedNodeData)

  def onNodeDrag(self):
    self.map.changeState(DragNodeState(self.map))
    
  def onF3Down(self):
    from scenes.states.foldNode import FoldNode
    self.map.state.exit()
    self.map.state = FoldNode(self.map)
    self.map.state.enter()

  # mouse1Down() helpers
  def setNodeSelected(self, selectedNodeData):
    nodeManager = self.map.nodeManager

    nodeDataSettings = nodeManager.dataContainer.nodeDataSettings
    self.clearSelectedField(nodeDataSettings)

    nodeManager.selectedNodeData = selectedNodeData
    nodeManager.setNodeSelected(selectedNodeData)
    
    nodeId = selectedNodeData.get("id")
    self.setSelected(nodeDataSettings, nodeId)

  def setupDragNodeManager(self, selectedNodeData):
    nodeDrawing = self.map.nodeManager.getNodeDrawing(selectedNodeData)
    DragNodeStartDetector(nodeDrawing, self.map, self.onNodeDrag)



  def setSelected(self, nodeDataSettings, nodeId):
    # nodeSettings = { "selected": True }
    if nodeId != None:
      nodeSettings = nodeDataSettings.get(nodeId)
      if nodeSettings == None:
        nodeDataSettings[nodeId] = { "selected": True }
      else:
        nodeDataSettings.get(nodeId)["selected"] = True

  def clearSelectedField(self, nodeDict):
    for key in nodeDict:
      nodeSettings = nodeDict.get(key)
      if nodeSettings.get("selected") is not None:
        nodeSettings.pop("selected", None)
    return nodeDict

  

    
  """ mouse1Down Helper """
  def goToScrollingState(self):
    
    from scenes.states.scrollingMapState import ScrollingMapState
    self.map.state.exit()
    self.map.state = ScrollingMapState(self.map)
    self.map.state.enter()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
  