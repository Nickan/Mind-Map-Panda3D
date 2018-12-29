

class StateManager():
  
  @staticmethod
  def switchToEditTextState(currentState, clickedNode):
    map = currentState.map
    currentState.exit()
    
    from scenes.states.editTextState import EditTextState
    map.state = EditTextState(map)
    map.state.enter(clickedNode)
    
  @staticmethod
  def switchToNodeClickedState(currentState, selectedNodeData):
    map = currentState.map
    currentState.exit()
    
    from scenes.states.nodeClickedState import NodeClickedState
    map.state = NodeClickedState(map)
    map.state.enter()
    
  @staticmethod
  def switchToStaticMapState(currentState):
    map = currentState.map
    map.state.exit()
    
    from scenes.states.staticMapState import StaticMapState
    map.state = StaticMapState(map)
    map.state.enter()
    
  @staticmethod
  def switchToDeleteNodeDataState(currentState, selectedNodeData):
    map = currentState.map
    map.state.exit()
    
    from scenes.states.deleteNodeDataState import DeleteNodeDataState
    map.state = DeleteNodeDataState(map)
    map.state.enter(selectedNodeData)
    
  @staticmethod
  def switchToCreateNodeDataState(currentState):
    map = currentState.map
    currentState.exit()

    from .createNodeState import CreateNodeState
    map.state = CreateNodeState(map)
    map.state.enter()
    
  @staticmethod
  def switchToLoadMapState(currentState, allData, allStatusData):
    map = currentState.map
    map.dispose()
    currentState.exit()
    
    from scenes.states.loadMapState import LoadMapState
    state = LoadMapState(map.showBase, allData, allStatusData)
    state.enter()

  @staticmethod
  def switchToScrollingState(currentState):
    map = currentState.map
    currentState.exit()
    
    from scenes.states.scrollingMapState import ScrollingMapState
    map.state = ScrollingMapState(map)
    map.state.enter()
    map.state.mouse1Down()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    