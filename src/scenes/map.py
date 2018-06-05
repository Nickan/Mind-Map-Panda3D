from scenes.cameramanager import CameraManager
from scenes.mapComponents.lineDrawings import LineDrawings
from scenes.mapComponents.nodeManager import NodeManager
from scenes.states.state import State
from scenes.states.cleanState import CleanState

from panda3d.core import LVecBase3f
from panda3d.core import NodePath

from utils.utils import Utils
from utils.saveManager import SaveManager

class Map():
  
  FONT_UBUNTU = None

  def __init__(self, showBase, jsonData):
    self.showBase = showBase
    self.jsonData = jsonData
    
    self.initCamera()
    self.initMapNode(self.showBase)
    self.initNodeManager()
    self.initLineDrawings()
    
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
  
  def initLineDrawings(self):
    self.lineDrawings = LineDrawings(self.mapNode)
    
    
  def createNodeData(self, parentId, name, recheckLastId = False):
    nodeManager = self.nodeManager
    nodeManager.createNodeData(parentId, name, recheckLastId)
    self.loadNodeDataList(nodeManager.nodeDataList)
    
  def editNodeData(self, nodeDataToEdit, newText):
    nodeManager = self.nodeManager
    nodeDataToEdit["name"] = newText
    self.loadNodeDataList(nodeManager.nodeDataList)
    
  def deleteNodeData(self, nodeDataToDelete):
    nodeManager = self.nodeManager
    nodeManager.deleteNodeData(nodeDataToDelete)
    SaveManager.clearNodeDataList(nodeManager.nodeDataList)
    
    self.loadNodeDataList(nodeManager.nodeDataList)
      
  def loadNodeDataList(self, nodeDataList):
    nodeManager = self.nodeManager
    nodeManager.tree.getCoordinates(nodeDataList)
    
    nodeManager.tmpClearNodes()
    self.lineDrawings.clear()
    
    loader = self.showBase.loader
    mapNode = self.mapNode
    for key in nodeDataList:
      nodeData = nodeDataList[key]
      
      breadth = nodeData.get("x")
      depth = nodeData.get("depth")
      
      nodePos = Utils.getPosition(depth, breadth)
      
      nodeManager.renderNodeData(loader, mapNode, nodeData, nodePos)
      self.lineDrawings.drawLine(nodeData, nodeDataList)
    
    

  def getSelectedNodeData(self):
    clickedNodePath = self.cameraManager.getClickedNodePath()
    if clickedNodePath is not None:
      return self.nodeManager.getNodeData(clickedNodePath)
    return None
    

  

  

    