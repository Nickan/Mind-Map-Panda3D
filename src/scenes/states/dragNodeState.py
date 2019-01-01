
from .state import State
from direct.task.Task import Task
from scenes.mapComponents.nodeDataFilter import NodeDataFilter
from scenes.mapComponents.nodeData import NodeData
from scenes.states.components.dragNodeMove import DragNodeMove
from scenes.states.components.newParentVisualCue import NewParentVisualCue
from utils.utils import Utils

import copy

class DragNodeState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self):
    self.map.initDragNodeState()
    self.initControls()

  def initControls(self):
    showBase = self.map.showBase
    showBase.taskMgr.add(self.mouseMove, "mouseMove")
    showBase.accept("mouse1-up", self.mouse1Up)

  def mouseMove(self, task):
    self.map.dragNode()
    return Task.cont

  def mouse1Up(self):
    self.map.dragNodeMouseUp()

  def exit(self):
    self.map.showBase.ignoreAll()
    self.map.showBase.taskMgr.remove("mouseMove")
















