from scenes.states.components.newParentVisualCue import NewParentVisualCue
from direct.task.Task import Task
from utils.utils import Utils

class DragNodeMove():

  def __init__(self, drawingPos, mPos):
    self.defaultPos = drawingPos
    self.posDiff = self.defaultPos - mPos

  def mouse1Up(self):
    self.map.showBase.ignoreAll()
    self.map.showBase.taskMgr.remove("mouseMove")
    # self.resetPosToDefault()
    nearestNodeDrawing = self.newParentVisualCue.getNearestNodeDrawing(self.map)
    self.onRelease(nearestNodeDrawing)
    if nearestNodeDrawing is None:
      self.nodeDrawing.mainNode.setPos(self.defaultPos)

  def setNodeDrawingPos(self, drawing, mPos):
    if mPos is not None:
      newNodePos = mPos + self.posDiff
      drawing.mainNode.setPos(newNodePos)

  def resetPosToDefault(self):
    self.nodeDrawing.mainNode.setPos(self.defaultPos)
  