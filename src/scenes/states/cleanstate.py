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
    map.showBase.accept("mouse1", self.mouse1Down)

  def mouse1Down(self):
    clickedNode = self.map.cameraManager.getClickedNode()
    if clickedNode is None:
      self.switchToScrollingState()
    else:
      self.switchToNodeClickedState(clickedNode)
      
      
  def switchToNodeClickedState(self, clickedNode):
    print("Switch to node clicked mode")
    
    map = self.map
    self.exit()
    from scenes.states.nodeClicked import NodeClickedState
    map.state = NodeClickedState(self.map)
    map.state.enter(clickedNode)
    
  def switchToScrollingState(self):
    self.map.state.exit()
    
    from scenes.states.scrollingMapState import ScrollingMapState
    self.map.state = ScrollingMapState(self.map)
    self.map.state.enter()
    self.map.state.mouse1Down()