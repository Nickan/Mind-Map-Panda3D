from direct.task.Task import Task
from direct.task.Task import TaskManager
from direct.showbase.ShowBase import ShowBase
from panda3d.core import LPoint3
from scenes.mapComponents.nodeDrawing import NodeDrawing
from utils.utils import Utils


# This class assumes that when instantiated, the mouse is down
class DragNodeStartDetector():

  DIST_TO_START = 2

  def __init__(self, nodeDrawing, map, onNodeDrag):
    
    self.nodeDrawing = nodeDrawing
    self.map = map
    self.onNodeDrag = onNodeDrag
    self.initEListener()
    self.defaultMousePos = Utils.getMousePosition(map.showBase)
    

  def initEListener(self):
    showBase = self.map.showBase
    showBase.taskMgr.add(self.mouseMove, "mouseMove")

  def mouseMove(self, task):
    self.checkIfNodeIsDragged()
    return Task.cont

  def checkIfNodeIsDragged(self):
    if self.nodeDrawing is not None and self.mouseHasMoved() is True:
      self.map.showBase.ignoreAll()
      self.map.showBase.taskMgr.remove("mouseMove")
      self.onNodeDrag()

  def mouseHasMoved(self):
    curMousePos = Utils.getMousePosition(self.map.showBase)
    distSqr = Utils.getDistSqr2D(self.defaultMousePos, curMousePos)
    return not Utils.isInRange(distSqr, DragNodeStartDetector.DIST_TO_START)


  