from .state import State
from scenes.mapComponents.nodeDataFilter import NodeDataFilter
from scenes.mapComponents.nodeData import NodeData
from scenes.states.components.dragNodeMove import DragNodeMove
from utils.utils import Utils

import copy

class DragNodeState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self):
    self.dragNodeMove = DragNodeMove(self.map, self.onRelease)

  def exit(self):
    print("exit DragNodeState")


  def onRelease(self, nearestDrawing):
    self.map.dragOnRelease(nearestDrawing, self)















