from state import State

import sys

class ScrollingMapState(State):
  

  def __init__(self):
    State.__init__(self)

  def enter(self, map):
    print("enter ScrollingMapState")
    self.map = map
    self.setupControls(map)

  def exit(self, map):
    print("exit ScrollingMapState")
    map.showBase.ignoreAll()
    map.showBase.taskMgr.remove("mouseMove")

    from scenes.states.staticMapState import StaticMapState
    map.state = StaticMapState()
    map.state.enter(map)

  def setupControls(self, map):
    map.showBase.accept('escape', sys.exit)

    cameraManager = map.cameraManager
    map.showBase.accept("wheel_up", cameraManager.zoomIn)
    map.showBase.accept("wheel_down", cameraManager.zoomOut)

    map.showBase.accept("mouse1", self.mouse1Down)
    map.showBase.accept("mouse1-up", self.mouse1Up)

    


  def mouse1Up(self):
    print("mouse1Up")
    self.map.state.exit(self.map)

  def mouse1Down(self):
    cameraManager = self.map.cameraManager
    cameraManager.mouse1Down()
    taskMgr = self.map.showBase.taskMgr
    taskMgr.add(cameraManager.mouseMove, "mouseMove")