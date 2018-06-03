from state import State
from stateManager import StateManager

import sys


class NodeClickedState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self, selectedNodeData):
    nodeManager = self.map.nodeManager
    nodeManager.selectedNodeData = selectedNodeData
    self.setupControls()
  
  def exit(self):
    self.map.showBase.ignoreAll()
    self.map.showBase.taskMgr.remove("mouseMove")
    
    
  """ enter helper """
  def setupControls(self):
    map = self.map
    map.showBase.accept('escape', sys.exit)

    cameraManager = map.cameraManager
#     map.showBase.accept("wheel_up", self.zoomIn)
#     map.showBase.accept("wheel_down", self.zoomOut)
    map.showBase.accept("mouse1", self.mouse1Down)
    map.showBase.accept("mouse1-up", self.mouse1Up)
    
    map.showBase.accept("tab", self.onTab)
    map.showBase.accept("delete", self.onDelete)
  
  
  """ Events """
  def mouse1Down(self):
    nodeManager = self.map.nodeManager
    selectedNodeData = self.map.getSelectedNodeData()
    if selectedNodeData is None:
      self.goToScrollingState()
      self.map.state.mouse1Down()
    else:
      nodeManager.selectedNodeData = selectedNodeData
      
#     if clickedNode is not None:
#       node = self.map.nodeManager.getNode(clickedNode)
#       self.map.nodeManager.selectedNode = node
#       print(node.textNode.getText())
#     else:
#       self.goToScrollingState()
#       self.map.state.mouse1Down()
    
  def mouse1Up(self):
    print("NodeClickedState mouse1Up")
    
  
  def onTab(self):
    self.switchToCreateNode()
    
  def onDelete(self):
    nodeManager = self.map.nodeManager
    StateManager.switchToDeleteNodeDataState(self, nodeManager.selectedNodeData)
    
    
    
  """ mouse1Down Helper """
  def goToScrollingState(self):
    from scenes.states.scrollingMapState import ScrollingMapState
    self.map.state.exit()
    self.map.state = ScrollingMapState(self.map)
    self.map.state.enter()
    
    
  def switchToCreateNode(self):
    self.exit()
    
    from scenes.states.createNodeState import CreateNodeState
    self.map.state = CreateNodeState(self.map)
    self.map.state.enter(self.map.nodeManager.selectedNodeData)
    
  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
  