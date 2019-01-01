from scenes.states.components.newParentVisualCue import NewParentVisualCue
from direct.task.Task import Task
from utils.utils import Utils

class DragNodeMove():

  def __init__(self, drawingPos, mPos):
    self.defaultPos = drawingPos
    self.posDiff = self.defaultPos - mPos

  def mouse1Up(self):
    nearestNodeDrawing = self.newParentVisualCue.getNearestNodeDrawing(self.map)
    self.onRelease(nearestNodeDrawing)
    if nearestNodeDrawing is None:
      self.nodeDrawing.mainNode.setPos(self.defaultPos)

  def dragSelectedDrawing(self, map):
    drawing = map.getSelectedNodeDrawing()
    mPos = Utils.getMousePosition(map.showBase)
    self.dragSelectedDrawingImpl(drawing, mPos)

  def dragSelectedDrawingImpl(self, drawing, mPos):
    if mPos is not None:
      newNodePos = mPos + self.posDiff
      drawing.mainNode.setPos(newNodePos)

  def resetPosToDefault(self):
    self.nodeDrawing.mainNode.setPos(self.defaultPos)



  @staticmethod
  def newInstance(map):
    drawing = map.getSelectedNodeDrawing()
    drawingPos = drawing.mainNode.getPos()
    mPos = Utils.getMousePosition(map.showBase)
    return DragNodeMove(drawingPos, mPos)
  