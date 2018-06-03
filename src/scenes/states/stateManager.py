

class StateManager():
  
  @staticmethod
  def switchToEditTextState(currentState, clickedNode):
    map = currentState.map
    currentState.exit()
    
    from scenes.states.editTextState import EditTextState
    map.state = EditTextState(map)
    map.state.enter(clickedNode, map)