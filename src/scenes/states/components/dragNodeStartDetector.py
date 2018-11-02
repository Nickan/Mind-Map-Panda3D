from direct.task.Task import Task
from direct.task.Task import TaskManager
from direct.showbase.ShowBase import ShowBase
from panda3d.core import LPoint3
from scenes.mapComponents.nodeDrawing import NodeDrawing
from utils.utils import Utils


# This class assumes that when instantiated, the mouse is down
class DragNodeStartDetector():

  def __init__(self, nodeDrawing, map, onNodeDrag):
    
    self.nodeDrawing = nodeDrawing
    self.map = map
    self.onNodeDrag = onNodeDrag
    self.initEListener()
    

  def initEListener(self):
    showBase = self.map.showBase
    showBase.taskMgr.add(self.mouseMove, "mouseMove")

  def mouseMove(self, task):
    self.checkIfNodeIsDragged()
    return Task.cont

  def checkIfNodeIsDragged(self):
    nodeDrawingUnderMouse = self.map.cameraManager.getClickedNodePath()
    if nodeDrawingUnderMouse is not None:
      self.removeEListener()
      self.onNodeDrag()

  def removeEListener(self):
    taskMgr = self.map.showBase.taskMgr
    taskMgr.remove("mouse1-up")
    taskMgr.remove("mouseMove")


  