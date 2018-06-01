from state import State

from utils.utils import Utils


class CreateNodeState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
#     self.selectedNode = None
    
  def enter(self, selectedNode):
    print("enter CreateNodeState")
    self.selectedNode = selectedNode
    Utils.createTextInput(self.onEnterText)
    
  def exit(self):
    print("exit CreateNodeState")
    self.map.showBase.ignoreAll()
    
    
  """ enter() Helpers """
  def onEnterText(self, text):
    nodeManager = self.map.nodeManager
    id = nodeManager.getNodeId(self.selectedNode)
    nodeManager.createNode(id, text, self.map.showBase.loader, 
                           self.map.mapNode)
    self.switchToStaticMapState(self.map)


  def switchToStaticMapState(self, map):
    map.state.exit()
    
    from scenes.states.staticMapState import StaticMapState
    map.state = StaticMapState(map)
    map.state.enter()






