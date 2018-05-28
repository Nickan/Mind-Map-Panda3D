from state import State

import sys

from gui.textinput import TextInput


class NodeClickedState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self, nodePath):
    node = self.map.nodeManager.getNode(nodePath)
    self.setupControls()
    
    self.createTextInput(node)
  
  def exit(self):
    self.map.showBase.ignoreAll()
    self.map.showBase.taskMgr.remove("mouseMove")
    
    
  """ enter helper """
  def setupControls(self):
    map = self.map
    map.showBase.accept('escape', sys.exit)

    cameraManager = map.cameraManager
#     map.showBase.accept("wheel_up", self.zoomIn)
#     map.showBase.accept("wheel_down", self.zoomOut)
    map.showBase.accept("mouse1", self.mouse1Down)
    map.showBase.accept("mouse1-up", self.mouse1Up)
    
    
  def createTextInput(self, node):
    self.node = node
    textInput = TextInput(self.onEnterText)
    
  def onEnterText(self, text):
    self.node.textNode.setText(text)
  
  """ Events """
  def mouse1Down(self):
    print("NodeClickedState mouse1Down")
    clickedNode = self.map.cameraManager.getClickedNode()
    if clickedNode is not None:
      node = self.map.nodeManager.getNode(clickedNode)
      print(node.textNode.getText())
    else:
      self.goToScrollingState()
      self.map.state.mouse1Down()
    
  def mouse1Up(self):
    print("NodeClickedState mouse1Up")
    
    
    
  """ mouse1Down Helper """
  def goToScrollingState(self):
    from scenes.states.scrollingMapState import ScrollingMapState
    self.map.state.exit()
    self.map.state = ScrollingMapState(self.map)
    self.map.state.enter()
  