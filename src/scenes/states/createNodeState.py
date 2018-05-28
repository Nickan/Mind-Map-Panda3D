from state import State

from gui.textinput import TextInput


class CreateNodeState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self, selectedNode):
    print("enter CreateNodeState")
    self.createTextInput(selectedNode)
    
  def exit(self):
    print("exit CreateNodeState")
    
    
  """ enter() Helpers """
  def createTextInput(self, node):
    self.node = node
    textInput = TextInput(self.onEnterText)
    
  def onEnterText(self, text):
    self.node.textNode.setText(text)