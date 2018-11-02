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

    self.initListeners()


  def initListeners(self):
    print("init")
    showBase = self.map.showBase
    showBase.taskMgr.add(self.mouseMove, "mouseMove")
    showBase.accept("mouse1-up", self.mouse1Up)

  def mouseMove(self, task):
    self.setNodeDrawingPos()
    # print("Updating")
    return Task.cont

  def mouse1Up(self):
    #Temp
    self.map.showBase.ignoreAll()
    self.map.showBase.taskMgr.remove("mouseMove")
    self.resetPosToDefault()
    self.onRelease()

  def setNodeDrawingPos(self):
    pos = self.nodeDrawing.mainNode.getPos()

    mPos = Utils.getMousePosition(self.map.showBase)
    if mPos is not None:
      newNodePos = mPos + self.posDiff
      self.nodeDrawing.mainNode.setPos(newNodePos)

  def resetPosToDefault(self):
    self.nodeDrawing.mainNode.setPos(self.defaultPos)
  