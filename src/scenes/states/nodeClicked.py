from state import State

class NodeClicked(State):
  
  def __init__(self):
    State.__init__(self)
    
    
  def enter(self, map, nodePath):
    self.map = map
    node = self.map.nodeManager.getNode(nodePath)
    print(node.text.getText())
  
  def exit(self, map):
    self.map.showBase.ignoreAll()
    self.map.showBase.taskMgr.remove("mouseMove")
    
  
  