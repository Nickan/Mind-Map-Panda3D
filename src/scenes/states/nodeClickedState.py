from state import State

import sys


class NodeClickedState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self, nodePath):
    node = self.map.nodeManager.getNode(nodePath)
    self.selectedNode = node
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
  
  
  """ Events """
  def mouse1Down(self):
    print("NodeClickedState mouse1Down")
    clickedNode = self.map.cameraManager.getClickedNode()
    if clickedNode is not None:
      node = self.map.nodeManager.getNode(clickedNode)
      self.map.nodeManager.selectedNode = node
      print(node.textNode.getText())
    else:
      self.goToScrollingState()
      self.map.state.mouse1Down()
    
  def mouse1Up(self):
    print("NodeClickedState mouse1Up")
    
  
  def onTab(self):
    self.switchToCreateNode()
    
    
    
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
    self.map.state.enter(self.map.nodeManager.selectedNode)
    
  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
  