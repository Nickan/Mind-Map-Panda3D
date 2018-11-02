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
    # self.firstUpdate = True
    

  def initEListener(self):
    showBase = self.map.showBase
    showBase.taskMgr.add(self.mouseMove, "mouseMove")

  def mouseMove(self, task):
    # if self.firstUpdate:
    #   self.firstUpdate = False
    #   return Task.cont

    self.checkIfNodeIsDragged()
    return Task.cont

  def checkIfNodeIsDragged(self):
    nodeDrawingUnderMouse = self.map.cameraManager.getClickedNodePath()
    if nodeDrawingUnderMouse is not None:
      self.map.showBase.ignoreAll()
      self.map.showBase.taskMgr.remove("mouseMove")
      self.onNodeDrag()


  