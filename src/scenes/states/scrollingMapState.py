from state import State

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
    # print("mouse1Up")
    self.map.state.exit()
    self.switchToStaticMap(self.map)
    
  def switchToStaticMap(self, map):
    from scenes.states.staticMapState import StaticMapState
    map.state = StaticMapState(map)
    map.state.enter()

  def mouse1Down(self):
    clickedNode = self.map.cameraManager.getClickedNode()
    if clickedNode is not None:
      self.switchToClickedNodeState(clickedNode)
    else:
      cameraManager = self.map.cameraManager
      cameraManager.mouse1Down()
      taskMgr = self.map.showBase.taskMgr
      taskMgr.add(cameraManager.mouseMove, "mouseMove")
      
  
  
  def switchToClickedNodeState(self, clickedNode):
    self.exit()
    
    from scenes.states.nodeClickedState import NodeClickedState
    self.map.state = NodeClickedState(self.map)
    self.map.state.enter(clickedNode)
    
    
    
    
    
    
    