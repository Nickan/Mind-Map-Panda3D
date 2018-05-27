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
    
  def exit(self):
    print("exit clean state")