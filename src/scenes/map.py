from scenes.cameramanager import CameraManager
from scenes.mapComponents.nodeManager import NodeManager
from scenes.states.state import State
from scenes.states.cleanState import CleanState

from panda3d.core import NodePath



class Map():
  
  FONT_UBUNTU = None

  def __init__(self, showBase, jsonData):
    self.showBase = showBase
    self.jsonData = jsonData
    
    self.state = CleanState(self)
    self.state.enter()

  def initCamera(self):
    self.cameraManager = CameraManager(self.showBase)

  def initMapNode(self, showBase):
    self.mapNode = NodePath("Map")
    self.mapNode.reparentTo(self.showBase.render)

  def initNodeManager(self):
    self.nodeManager = NodeManager()
#     self.nodeManager.loadJson(self.showBase.loader, self.mapNode, jsonData)

  def getSelectedNodeData(self):
    clickedNodePath = self.cameraManager.getClickedNodePath()
    if clickedNodePath is not None:
      return self.nodeManager.getNodeData(clickedNodePath)
    return None
    

  

  

    