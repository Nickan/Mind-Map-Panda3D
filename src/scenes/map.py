from scenes.cameramanager import CameraManager
from scenes.mapComponents.lineDrawings import LineDrawings
from scenes.mapComponents.nodeManager import NodeManager

from panda3d.core import LVecBase3f
from panda3d.core import NodePath

from utils.utils import Utils
from utils.saveManager import SaveManager

class Map():
  
  FONT_UBUNTU = None

  def __init__(self, showBase):
    self.showBase = showBase
    
    self.initCamera()
    self.initMapNode(self.showBase)
    self.initNodeManager()
    self.initLineDrawings()    

  def initCamera(self):
    self.cameraManager = CameraManager(self.showBase)

  def initMapNode(self, showBase):
    self.mapNode = NodePath("Map")
    self.mapNode.reparentTo(self.showBase.render)

  def initNodeManager(self):
    self.nodeManager = NodeManager()
  
  def initLineDrawings(self):
    self.lineDrawings = LineDrawings(self.mapNode)
    
    
  def createNodeData(self, parentId, name, recheckLastId = False):
    nodeManager = self.nodeManager
    newNodeData = nodeManager.createNodeData(parentId, name, recheckLastId)
#     self.drawNodeDataList(nodeManager.nodeDataList)
    return newNodeData
    
  def editNodeData(self, nodeDataToEdit, newText):
    nodeManager = self.nodeManager
    nodeDataToEdit["name"] = newText
    
    self.drawNodeDataList(nodeManager.nodeDataList)
    
  def deleteNodeData(self, nodeDataToDelete):
    nodeManager = self.nodeManager
    nodeManager.deleteNodeData(nodeDataToDelete)

    SaveManager.clearNodeDataList(nodeManager.nodeDataList)
    nodeManager.tree.getCoordinates(nodeManager.nodeDataList)
    self.drawNodeDataList(nodeManager.nodeDataList)
      
  def drawNodeDataList(self, nodeDataList = None):
    nodeManager = self.nodeManager
    if nodeDataList is None:
      nodeDataList = nodeManager.nodeDataList
    
    nodeManager.tmpClearNodes()
    self.lineDrawings.clear()
    
    loader = self.showBase.loader
    mapNode = self.mapNode
    for key in nodeDataList:
      nodeData = nodeDataList[key]
      
      breadth = nodeData.get("x")
      depth = nodeData.get("depth")
      
      nodePos = Utils.getNodePosition(depth, breadth)
      
      nodeManager.renderNodeData(loader, mapNode, nodeData, nodePos)
      self.lineDrawings.drawLine(nodeData, nodeDataList)
    
    
  """ Getters and Setters """
  def setState(self, state):
    self.state = state
    self.state.enter()
  
  def getSelectedNodeData(self):
    # Requires interaction between camera and nodemanager, so it is put in map class
    clickedNodePath = self.cameraManager.getClickedNodePath()
    if clickedNodePath is not None:
      return self.nodeManager.getNodeData(clickedNodePath)
    return None
  
  
  # Utils
  def clickedOnMapBg(self):
    camManager = self.cameraManager
    return (camManager.getMouseCollisionToPlane(camManager.plane) is None or
      camManager.getClickedNodePath() is None)
    
    
    
    
    
    

  

  

    