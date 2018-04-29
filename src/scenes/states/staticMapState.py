from state import State

from scenes.states.scrollingMapState import ScrollingMapState

import sys

class StaticMapState(State):

  def __init__(self):
    State.__init__(self)

  def enter(self, map):
    print("enter")
    self.setupControls(map)

  def exit(self, map):
    print("exit StaticMapState")
    map.showBase.ignoreAll()
    map.state = ScrollingMapState()
    map.state.enter(map)


  def setupControls(self, map):
    self.map = map
    map.showBase.accept('escape', sys.exit)

    cameraManager = map.cameraManager
    map.showBase.accept("wheel_up", self.zoomIn)
    map.showBase.accept("wheel_down", self.zoomOut)

    map.showBase.accept("mouse1", self.mouse1Down)
    map.showBase.accept("mouse1-up", self.mouse1Up)

  def zoomIn(self):
    self.goToScrollingState()
    self.map.cameraManager.zoomIn()

  def zoomOut(self):
    self.goToScrollingState()
    self.map.cameraManager.zoomOut()

  def mouse1Down(self):
    self.goToScrollingState()
    self.map.state.mouse1Down()

  def mouse1Up(self):
    self.goToScrollingState()
    self.map.cameraManager.mouse1Up()

  def goToScrollingState(self):
    self.map.state.exit(self.map)
    
  
