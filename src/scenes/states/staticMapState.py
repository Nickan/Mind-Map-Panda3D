from state import State

class StaticMapState(State):

  def __init__(self):
    State.__init__(self)

  def enter(self, map):
    map.initCamera()
    map.initNode()

  # def exit(self):
  #   print("exit StaticMapState")