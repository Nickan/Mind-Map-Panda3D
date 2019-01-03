from scenes.states.components.dragNodeStartDetector import DragNodeStartDetector
from .state import State
from .dragNodeState import DragNodeState
from .stateManager import StateManager
from utils.utils import Utils

import sys


class NodeClickedState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self):
    map = self.map
    data = map.getSelectedNodeData()
    map.setStatusAsSelected(data)
    map.drawData()
    self.setupControls(data)

  def exit(self):
    self.map.showBase.ignoreAll()
    self.map.showBase.taskMgr.remove("mouseMove")
    
  """ enter helper """
  def setupControls(self, data):
    self.map.showBase.accept("mouse1-up", self.mouse1Up)
    self.setupDragNodeDetector(data)

  """ Events """
  def mouse1Up(self):
    from scenes.states.staticMapState import StaticMapState
    self.map.changeState(StaticMapState(self.map))

  def onNodeDrag(self):
    self.map.changeState(DragNodeState(self.map))

  def setupDragNodeDetector(self, data):
    nodeDrawing = self.map.nodeManager.getNodeDrawing(data)
    DragNodeStartDetector(nodeDrawing, self.map, self.onNodeDrag)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
  