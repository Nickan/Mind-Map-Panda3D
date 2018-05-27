from state import State

from scrollingMapState import ScrollingMapState

import sys

class StaticMapState(State):

  def __init__(self):
    State.__init__(self)

  def enter(self, map):
    self.map = map
    self.setupControls(map)

  def exit(self, map):
    print("exit StaticMapState")
    map.showBase.ignoreAll()
    

  """ enter helper """
  def setupControls(self, map):
    self.map = map
    map.showBase.accept('escape', sys.exit)

    cameraManager = map.cameraManager
    map.showBase.accept("wheel_up", self.zoomIn)
    map.showBase.accept("wheel_down", self.zoomOut)

    map.showBase.accept("mouse1", self.mouse1Down)
    map.showBase.accept("mouse1-up", self.mouse1Up)
  
  """ Events """
  def zoomIn(self):
    self.goToScrollingState()
    self.map.cameraManager.zoomIn()

  def zoomOut(self):
    self.goToScrollingState()
    self.map.cameraManager.zoomOut()

  def mouse1Down(self):
    clickedNode = self.map.cameraManager.getClickedNode()
    if clickedNode is not None:
      self.switchToClickedNodeState(clickedNode)
    else:
      self.goToScrollingState()
      self.map.state.mouse1Down()

  def mouse1Up(self):
    print("static move up")
  
  """ mouse1Down Helper """
  def switchToClickedNodeState(self, clickedNode):
    self.exit(self.map)
    
    from scenes.states.nodeClicked import NodeClicked
    self.map.state = NodeClicked()
    self.map.state.enter(self.map, clickedNode)
    
    
  """ mouse1Up Helper """
  def goToScrollingState(self):
    self.map.state.exit(self.map)
    self.map.state = ScrollingMapState()
    self.map.state.enter(self.map)
    
  
  
  
  
  
  
  
