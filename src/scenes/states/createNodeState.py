from state import State
from stateManager import StateManager

from utils.utils import Utils


class CreateNodeState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self, selectecNodeData):
    nodeManager = self.map.nodeManager
    nodeManager.selectecNodeData = selectecNodeData
    Utils.createTextInput(self.onEnterText)
    
  def exit(self):
    print("exit CreateNodeState")
    self.map.showBase.ignoreAll()
    
    
  """ enter() Helpers """
  def onEnterText(self, text):
    if text is not None:
      nodeManager = self.map.nodeManager
      id = nodeManager.getNodeDataId(nodeManager.selectecNodeData)
      self.map.createNodeData(id, text)
      
    StateManager.switchToStaticMapState(self)






