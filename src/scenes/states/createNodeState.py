from state import State
from stateManager import StateManager

from utils.utils import Utils


class CreateNodeState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self, selectedNodeData):
    nodeManager = self.map.nodeManager
    nodeManager.selectedNodeData = selectedNodeData
    
    # Need way how to pass the position to convert to screen coords
#     pos = nodeManager.getNodeDrawingPos()
#     print("Node pos " + str(pos))
    
    Utils.createTextInput(self.onEnterText)
    
  def exit(self):
    print("exit CreateNodeState")
    self.map.showBase.ignoreAll()
    
    
  """ enter() Helpers """
  def onEnterText(self, text):
    if text is not None:
      nodeManager = self.map.nodeManager
      id = nodeManager.getNodeDataId(nodeManager.selectedNodeData)
      self.map.createNodeData(id, text)
      
    StateManager.switchToStaticMapState(self)






