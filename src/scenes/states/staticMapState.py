

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

    map.showBase.accept("wheel_up", self.zoomIn)
    map.showBase.accept("wheel_down", self.zoomOut)

    map.showBase.accept("mouse1", self.mouse1Down)
    map.showBase.accept("mouse1-up", self.mouse1Up)
    map.showBase.accept("tab", self.onTab)
    map.showBase.accept("enter", self.onEnter)
    
    map.showBase.accept("control-s", self.onSave)
    map.showBase.accept("f1", self.onOpenFile)
    map.showBase.accept("f2", self.onEdit)
    map.showBase.accept("f3", self.onFoldAncestors)
    map.showBase.accept("f4", self.onFoldChildren)
    
    map.showBase.accept("delete", self.onDelete)
  
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
      
  def onEdit(self):
    selectedData = self.map.getActivatedNodeData()
    if selectedData is None:
      print("None selected")
    else:
      StateManager.switchToEditTextState(self, selectedData)
      
  def mouse1Up(self):
    print("static move up")
    
  def onTab(self):
    StateManager.switchToCreateNodeDataState(self)

  def onEnter(self):
    StateManager.switchToCreateSiblingState(self)
    
  def onSave(self):
    nm = self.map.nodeManager
    cam = self.map.cameraManager
    SaveManager.saveData(nm.allData, nm.allStateData, cam.camDict)
    
  def onOpenFile(self):
    SaveManager.loadDataContainer(self.onNodeDataListLoaded)

  def onFoldChildren(self):
    self.map.toggleChildrenShowHide()
    self.map.focusOnActivatedData()

  def onFoldAncestors(self):
    self.map.toggleAncestorShowHide()
    self.map.focusOnActivatedData()
    
  def onDelete(self):
    map = self.map
    data = map.getActivatedNodeData()
    allData = map.removeData(data)
    if allData is None:
      return
    allStateData = map.nodeManager.allStateData
    camDict = map.cameraManager.camDict
    StateManager.switchToLoadMapState(self, allData, allStateData, camDict)
    
  def onNodeDataListLoaded(self, allData, allStateData, camDict):
    StateManager.switchToLoadMapState(self, allData, allStateData, camDict)
  
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
    
    
  
  
  
  
  
  
  
