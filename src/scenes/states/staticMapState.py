

from .state import State
from .stateManager import StateManager

from .scrollingMapState import ScrollingMapState
from utils.saveManager import SaveManager
from utils.utils import Utils

import sys


class StaticMapState(State):

  def __init__(self, map):
    State.__init__(self)
    self.map = map

  def enter(self):
    self.setupControls()

  def exit(self):
    self.map.showBase.ignoreAll()
    

  """ enter helper """
  def setupControls(self):
    map = self.map
    map.showBase.accept('escape', sys.exit)

    cameraManager = map.cameraManager
    map.showBase.accept("wheel_up", self.zoomIn)
    map.showBase.accept("wheel_down", self.zoomOut)

    map.showBase.accept("mouse1", self.mouse1Down)
    map.showBase.accept("mouse1-up", self.mouse1Up)
    map.showBase.accept("mouse3", self.mouse3Down)
    
    map.showBase.accept("tab", self.onTab)
    
    map.showBase.accept("f1", self.onSave)
    map.showBase.accept("f2", self.onOpenFile)
    map.showBase.accept("f3", self.onFoldNode)

    # Temporary for fixing bug when folding
    map.showBase.accept("f5", self.clearAllDrawings)

    map.showBase.accept("delete", self.onDelete)

  def clearAllDrawings(self):
    map = self.map
    map.nodeManager.tmpClearNodeDrawings()
  
  """ Events """
  def zoomIn(self):
    self.goToScrollingState()
    self.map.cameraManager.zoomIn()

  def zoomOut(self):
    self.goToScrollingState()
    self.map.cameraManager.zoomOut()

  def mouse1Down(self):
    selectedNodeData = self.map.getSelectedNodeData()
    if selectedNodeData is None:
      self.goToScrollingState()
      self.map.state.mouse1Down()
    else:
      StateManager.switchToNodeClickedState(self, selectedNodeData)
      
  def mouse3Down(self):
    selectedNodeData = self.map.getSelectedNodeData()
    if selectedNodeData is None:
      print("None selected")
    else:
      StateManager.switchToEditTextState(self, selectedNodeData)
      
  def mouse1Up(self):
    print("static move up")
    
  def onTab(self):
    StateManager.switchToCreateNodeDataState(self)
    
  def onSave(self):
    nm = self.map.nodeManager
    SaveManager.saveData(nm.allData, nm.allStatusData)
    
  def onOpenFile(self):
    SaveManager.loadDataContainer(self.onNodeDataListLoaded)

  def onFoldNode(self):
    map = self.map
    data = map.getActivatedNodeData()
    allData, allStatusData = map.foldNode(data)

    StateManager.switchToLoadMapState(self, allData, allStatusData)

  def onDelete(self):
    nodeManager = self.map.nodeManager
    StateManager.switchToDeleteNodeDataState(self, nodeManager.selectedNodeData)
    
    
  def onNodeDataListLoaded(self, allData, allStatusData):
    StateManager.switchToLoadMapState(self, allData, allStatusData)
  
  
  """ mouse1Down Helper """
  def switchToClickedNodeState(self, clickedNode):
    self.exit()
    
    from scenes.states.nodeClickedState import NodeClickedState
    self.map.state = NodeClickedState(self.map)
    self.map.state.enter(clickedNode)
    
    
  """ mouse1Up Helper """
  def goToScrollingState(self):
    self.map.state.exit()
    self.map.state = ScrollingMapState(self.map)
    self.map.state.enter()
    
  """ mouse3Down Helper """
    
    
  
  
  
  
  
  
  
