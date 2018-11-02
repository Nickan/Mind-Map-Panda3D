from state import State

from scenes.states.components.dragNodeMove import DragNodeMove

class DragNodeState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self):
    print("DragNodeState")
    self.dragNodeMove = DragNodeMove(self.map, self.onRelease)

  def exit(self):
    print("exit DragNodeState")


  def onRelease(self):
    print("Release")
    from scenes.states.staticMapState import StaticMapState
    self.map.changeState(StaticMapState(self.map))












