from state import State

class CleanState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self):
    map = self.map
    map.initCamera()
    map.initMapNode(map.showBase)
    map.initNodeManager()
    
    map.nodeManager.addNode("Main", map.showBase.loader, map.mapNode)
    
    self.initEvents()
    
  def exit(self):
    print("exit clean state")
    self.map.showBase.ignoreAll()
    
    
    
    
  """ enter() helpers """
  def initEvents(self):
    map = self.map
#     map.showBase.accept('escape', sys.exit)
#     
#     map.showBase.accept("wheel_up", self.zoomIn)
#     map.showBase.accept("wheel_down", self.zoomOut)

    map.showBase.accept("mouse1", self.mouse1Down)
#     map.showBase.accept("mouse1-up", self.mouse1Up)

  def mouse1Down(self):
    clickedNode = self.map.cameraManager.getClickedNode()
    if clickedNode is None:
      print("Nothing will happen")
    else:
      self.switchToNodeClickedState(clickedNode)
      
      
  def switchToNodeClickedState(self, clickedNode):
    print("Switch to node clicked mode")
    
    map = self.map
    self.exit()
    from scenes.states.nodeClicked import NodeClickedState
    map.state = NodeClickedState(self.map)
    map.state.enter(clickedNode)