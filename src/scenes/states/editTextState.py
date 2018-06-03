from state import State

from utils.utils import Utils

class EditTextState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
    
  def enter(self, selectedNodePath, map):
    self.selectedNode = self.map.nodeManager.getNode(selectedNodePath)
    print("EditTextState enter")
    Utils.createTextInput(self.onEnterText)
    
  def exit(self, map):
    print("EditTextState exit")
    self.map.showBase.ignoreAll()
    
  
  """ enter() Helpers """
  def onEnterText(self, text):
    nodeManager = self.map.nodeManager
    self.selectedNode.textNode.setText(text)
    
    self.switchToStaticState(self.map)
    
  def switchToStaticState(self, map):
    map.state.exit(map)
    
    from scenes.states.staticMapState import StaticMapState
    map.state = StaticMapState(map)
    map.state.enter()