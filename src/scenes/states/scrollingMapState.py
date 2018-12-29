from .state import State
from .stateManager import StateManager

import sys

class ScrollingMapState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map

  def enter(self):
    self.setupControls()

  def exit(self):
    print("exit ScrollingMapState")
    map = self.map
    map.showBase.ignoreAll()
    map.showBase.taskMgr.remove("mouseMove")


  def setupControls(self):
    map = self.map
    map.showBase.accept('escape', sys.exit)

    cameraManager = map.cameraManager
    map.showBase.accept("wheel_up", cameraManager.zoomIn)
    map.showBase.accept("wheel_down", cameraManager.zoomOut)

    map.showBase.accept("mouse1", self.mouse1Down)
    map.showBase.accept("mouse1-up", self.mouse1Up)

    
  def mouse1Up(self):
    self.map.state.exit()
    self.switchToStaticMap(self.map)
    
  def switchToStaticMap(self, map):
    from scenes.states.staticMapState import StaticMapState
    map.state = StaticMapState(map)
    map.state.enter()

  def mouse1Down(self):
    selectedNodeData = self.map.getSelectedNodeData()
    if selectedNodeData is None:
      cameraManager = self.map.cameraManager
      cameraManager.mouse1Down()
      taskMgr = self.map.showBase.taskMgr
      taskMgr.add(cameraManager.mouseMove, "mouseMove")
    else:
      StateManager.switchToNodeClickedState(self, selectedNodeData)
    
    
    
    
    
    
    