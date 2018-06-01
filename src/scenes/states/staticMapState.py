from state import State

from scrollingMapState import ScrollingMapState

import sys

class StaticMapState(State):

  def __init__(self, map):
    State.__init__(self)
    self.map = map

  def enter(self):
    self.setupControls()

  def exit(self):
    print("exit StaticMapState")
    self.map.showBase.ignoreAll()
    

  """ enter helper """
  def setupControls(self):
    map = self.map
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
    self.exit()
    
    from scenes.states.nodeClickedState import NodeClickedState
    self.map.state = NodeClickedState(self.map)
    self.map.state.enter(clickedNode)
    
    
  """ mouse1Up Helper """
  def goToScrollingState(self):
    self.map.state.exit()
    self.map.state = ScrollingMapState(self.map)
    self.map.state.enter()
    
    
  
  
  
  
  
  
  
