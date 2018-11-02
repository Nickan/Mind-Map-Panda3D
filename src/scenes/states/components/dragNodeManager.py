from direct.task.Task import Task
from direct.task.Task import TaskManager
from direct.showbase.ShowBase import ShowBase
from panda3d.core import LPoint3
from scenes.mapComponents.nodeDrawing import NodeDrawing
from utils.utils import Utils

class DragNodeManager():

  def __init__(self, nodeDrawing, showBase, onNodeDrag, onNodeRelease = None):
    showBase.taskMgr.add(self.mouseMove, "mouseMove")
    self.showBase = showBase
    self.nodeDrawing = nodeDrawing
    self.defaultPos = self.nodeDrawing.mainNode.getPos()
    

  def mouseMove(self, task):
    # print("On mouse move")
    pos = self.nodeDrawing.mainNode.getPos()
    # print(str(pos.x) + ": " + str(pos.y))

    mPos = Utils.getMousePosition(self.showBase)
    print("mPos " + str(mPos))
    return Task.cont