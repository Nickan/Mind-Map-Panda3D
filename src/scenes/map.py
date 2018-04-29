from scenes.cameramanager import CameraManager
from scenes.mapComponents.nodeManager import NodeManager
from scenes.states.state import State
from scenes.states.staticMapState import StaticMapState

from panda3d.core import NodePath

class Map():

  def __init__(self, showBase):
    self.showBase = showBase

    self.initCamera()

    self.initMapNode(showBase)
    self.initNodeManager()
    self.state = StaticMapState()
    self.state.enter(self)

  def initCamera(self):
    self.cameraManager = CameraManager(self.showBase)

  def initMapNode(self, showBase):
    self.mapNode = NodePath("Map")
    self.mapNode.reparentTo(self.showBase.render)

  def initNodeManager(self):
    self.nodeManager = NodeManager()
    self.nodeManager.addNode(self.showBase.loader, self.mapNode)

  

  

    