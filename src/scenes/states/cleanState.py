from .state import State
from .stateManager import StateManager

from scenes.map import Map
from utils.utils import Utils

from scenes.mapComponents.nodeDrawing import NodeDrawing

class CleanState(State):
  
  def __init__(self, showBase):
    State.__init__(self)
    self.map = Map(showBase, {}, {})
    
  # Refactor, should start from scratch
  def enter(self):
    map = self.map
    allData, allStatusData = map.createNodeData(None, "Main")

    # I don't know why the screen size is different when activating this
    # StateManager.switchToLoadMapState(self, allData, allStatusData)

    map.drawData()
    map.state = self
    self.initEvents()
    
    
  def exit(self):
    self.map.showBase.ignoreAll()
    
    
  """ enter() helpers """
  def initEvents(self):
    map = self.map
    map.showBase.accept("mouse1", self.mouse1Down)
    map.showBase.accept("mouse3", self.mouse3Down)

  def mouse1Down(self):
    map = self.map
    
    selectedNodeData = map.getSelectedNodeData()
    if selectedNodeData is None:
      # self.switchToScrollingState()
      StateManager.switchToScrollingState(self)
    else:
      self.switchToNodeClickedState(selectedNodeData)
        
  def mouse3Down(self):
    selectedNodeData = self.map.getSelectedNodeData()
    if selectedNodeData is None:
      print("None selected")
    else:
      StateManager.switchToEditTextState(self, selectedNodeData)
  
  """ mouse3Down Helper """
  
      
      
  def switchToNodeClickedState(self, selectedNodeData):
    print("Switch to node clicked mode")
    
    map = self.map
    self.exit()
    from scenes.states.nodeClickedState import NodeClickedState
    map.state = NodeClickedState(self.map)
    map.state.enter()
    
  # def switchToScrollingState(self):
  #   self.map.state.exit()
    
  #   from scenes.states.scrollingMapState import ScrollingMapState
  #   self.map.state = ScrollingMapState(self.map)
  #   self.map.state.enter()
  #   self.map.state.mouse1Down()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    