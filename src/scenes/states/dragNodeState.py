

from state import State


class DragNodeState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self, nodeData):
    print("enter DragNodeState")
    
    
  def exit(self):
    print("exit DragNodeState")










