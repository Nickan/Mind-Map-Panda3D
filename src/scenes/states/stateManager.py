

class StateManager():
  
  @staticmethod
  def switchToEditTextState(currentState, clickedNode):
    map = currentState.map
    currentState.exit()
    
    from scenes.states.editTextState import EditTextState
    map.state = EditTextState(map)
    map.state.enter(clickedNode, map)
    
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
    map.state.exit(map)
    
    from scenes.states.staticMapState import StaticMapState
    map.state = StaticMapState(map)
    map.state.enter()