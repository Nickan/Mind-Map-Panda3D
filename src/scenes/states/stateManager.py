

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
    map.state.enter(selectedNodeData)
    
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
  def switchToCreateNodeDataState(currentState, selectedNodeData):
    map = currentState.map
    currentState.exit()
    
    from scenes.states.createNodeState import CreateNodeState
    map.state = CreateNodeState(map)
    map.state.enter(map.nodeManager.selectedNodeData)
    
  @staticmethod
  def switchToLoadMapState(currentState, dataContainer):
    map = currentState.map
    currentState.exit()
    
    from scenes.states.loadMapState import LoadMapState
    map.state = LoadMapState(map)
    map.state.enter(dataContainer)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    