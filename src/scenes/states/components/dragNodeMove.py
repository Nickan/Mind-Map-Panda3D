from scenes.states.components.newParentVisualCue import NewParentVisualCue
from direct.task.Task import Task
from utils.utils import Utils

class DragNodeMove():

  def __init__(self, map, onRelease):
    self.map = map
    self.onRelease = onRelease
    self.nodeDrawing = map.getSelectedNodeDrawing()

    self.defaultPos = self.nodeDrawing.mainNode.getPos()
    mPos = Utils.getMousePosition(map.showBase)
    self.posDiff = self.defaultPos - mPos

    self.newParentVisualCue = NewParentVisualCue(map)
    self.initListeners()

  def initListeners(self):
    showBase = self.map.showBase
    showBase.taskMgr.add(self.mouseMove, "mouseMove")
    showBase.accept("mouse1-up", self.mouse1Up)

  def mouseMove(self, task):
    self.setNodeDrawingPos()
    return Task.cont

  def mouse1Up(self):
    self.map.showBase.ignoreAll()
    self.map.showBase.taskMgr.remove("mouseMove")
    # self.resetPosToDefault()
    self.onRelease(self.newParentVisualCue.nearestNodeDrawing)

  def setNodeDrawingPos(self):
    pos = self.nodeDrawing.mainNode.getPos()

    mPos = Utils.getMousePosition(self.map.showBase)
    if mPos is not None:
      newNodePos = mPos + self.posDiff
      self.nodeDrawing.mainNode.setPos(newNodePos)
      self.newParentVisualCue.draw(self.map)

  def resetPosToDefault(self):
    self.nodeDrawing.mainNode.setPos(self.defaultPos)
  