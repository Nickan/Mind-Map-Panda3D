from scenes.states.components.dragNodeStartDetector import DragNodeStartDetector
from .state import State
from .dragNodeState import DragNodeState
from .stateManager import StateManager
from utils.utils import Utils

import sys


class NodeClickedState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self):
    map = self.map
    data = map.getSelectedNodeData()
    map.setStatusAsSelected(data)
    map.drawData()
    self.setupControls(data)

  def exit(self):
    self.map.showBase.ignoreAll()
    self.map.showBase.taskMgr.remove("mouseMove")
    

  # mouse1Down() helpers
  def setNodeSelected(self, data):
    nodeManager = self.map.nodeManager

    nodeDataSettings = nodeManager.dataContainer.nodeDataSettings
    self.removeAllSelectedField(nodeDataSettings)

    nodeManager.setNodeSelected(data)
    
    nodeId = data.get("id")
    self.setSelected(nodeDataSettings, nodeId)
    
  """ enter helper """
  def setupControls(self, data):
    showBase = self.map.showBase
    showBase.accept('escape', sys.exit)

    showBase.accept("mouse1", self.mouse1Down)
    showBase.accept("mouse1-up", self.mouse1Up)
    showBase.accept("mouse3", self.mouse3Down)
    
    showBase.accept("tab", self.onTab)
    
    self.setupDragNodeDetector(data)

    # Temporary, have to change the control later on
    showBase.accept("f3", self.onF3Down)

  """ Events """
  def mouse1Down(self):
    nodeManager = self.map.nodeManager
    data = self.map.getSelectedNodeData()
    if data is None:
      self.goToScrollingState()
      self.map.state.mouse1Down()
    else:
      self.setupDragNodeDetector(data)
      self.setNodeSelected(data)
    
  def mouse1Up(self):
    from scenes.states.staticMapState import StaticMapState
    self.map.changeState(StaticMapState(self.map))

  def mouse3Down(self):
    data = self.map.getSelectedNodeData()
    if data is None:
      print("None selected")
    else:
      StateManager.switchToEditTextState(self, data)
    
  def onTab(self):
    StateManager.switchToCreateNodeDataState(self)

  # Have to refactor, as won't be triggered here
  def onDelete(self):
    nodeManager = self.map.nodeManager
    StateManager.switchToDeleteNodeDataState(self, nodeManager.data)

  def onNodeDrag(self):
    self.map.changeState(DragNodeState(self.map))
    
  def onF3Down(self):
    from scenes.states.foldNode import FoldNode
    self.map.state.exit()
    self.map.state = FoldNode(self.map)
    self.map.state.enter()

  def setupDragNodeDetector(self, data):
    nodeDrawing = self.map.nodeManager.getNodeDrawing(data)
    DragNodeStartDetector(nodeDrawing, self.map, self.onNodeDrag)



  def setSelected(self, nodeDataSettings, nodeId):
    # nodeSettings = { "selected": True }
    if nodeId != None:
      nodeSettings = nodeDataSettings.get(nodeId)
      if nodeSettings == None:
        nodeDataSettings[nodeId] = { "selected": True }
      else:
        nodeDataSettings.get(nodeId)["selected"] = True

  # def removeAllSelectedField(self, nodeDict):
  #   for key in nodeDict:
  #     nodeSettings = nodeDict.get(key)
  #     if nodeSettings.get("selected") is not None:
  #       nodeSettings.pop("selected", None)
  #   return nodeDict

  

    
  """ mouse1Down Helper """
  def goToScrollingState(self):
    
    from scenes.states.scrollingMapState import ScrollingMapState
    self.map.state.exit()
    self.map.state = ScrollingMapState(self.map)
    self.map.state.enter()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
  