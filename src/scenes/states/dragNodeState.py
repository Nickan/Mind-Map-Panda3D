
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
    self.newParentVisualCue = NewParentVisualCue()

    self.initDragNodeMove()
    self.initControls()

  def initDragNodeMove(self):
    map = self.map
    drawing = map.getSelectedNodeDrawing()
    drawingPos = drawing.mainNode.getPos()
    mPos = Utils.getMousePosition(map.showBase)
    self.dragNodeMove = DragNodeMove(drawingPos, mPos)

  def initControls(self):
    showBase = self.map.showBase
    showBase.taskMgr.add(self.mouseMove, "mouseMove")
    showBase.accept("mouse1-up", self.mouse1Up)

  def mouseMove(self, task):
    map = self.map
    drawing = map.getSelectedNodeDrawing()

    mPos = Utils.getMousePosition(map.showBase)
    self.dragNodeMove.setNodeDrawingPos(drawing, mPos)

    nm = map.nodeManager
    # self.newParentVisualCue.draw(mPos, nm.allDrawingData)
    return Task.cont

  def mouse1Up(self):
    self.map.dragOnRelease(nearestDrawing, self)

  def exit(self):
    self.map.showBase.ignoreAll()
    self.map.showBase.taskMgr.remove("mouseMove")















