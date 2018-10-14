from scenes.cameramanager import CameraManager
from scenes.mapComponents.lineDrawings import LineDrawings
from scenes.mapComponents.nodeManager import NodeManager
from scenes.mapComponents.dataContainer import DataContainer

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
    return newNodeData
    
  def editNodeData(self, nodeDataToEdit, newText):
    nodeManager = self.nodeManager
    nodeDataToEdit["name"] = newText
    

    self.drawNodeData(nodeManager.dataContainer)
    
  def deleteNodeData(self, nodeDataToDelete):
    nodeManager = self.nodeManager
    nodeManager.deleteNodeData(nodeDataToDelete)

    nodeDataList = nodeManager.dataContainer.nodeDataList
    SaveManager.clearNodeDataList(nodeDataList)
    nodeManager.tree.getCoordinates(nodeDataList)
    self.drawNodeData(nodeManager.dataContainer)
      
  def drawNodeData(self, dataContainer):
    nodeManager = self.nodeManager
    nodeManager.dataContainer = dataContainer
    nodeDataList = nodeManager.dataContainer.nodeDataList
    nodeDataSettings = dataContainer.nodeDataSettings
    
    nodeManager.tmpClearNodeDrawings()
    self.lineDrawings.clear()
    
    loader = self.showBase.loader
    mapNode = self.mapNode
    for key in nodeDataList:
      nodeData = nodeDataList[key]
      nodeSettings = nodeDataSettings.get(key)
      
      breadth = nodeData.get("x")
      depth = nodeData.get("depth")
      
      nodePos = Utils.getNodePosition(depth, breadth)
      
      nodeManager.renderNodeData(loader, mapNode, nodeData, nodeSettings, nodePos)
      self.lineDrawings.drawLine(nodeData, nodeDataList)

  def setCameraViewToSelectedNode(self):
    s = self.getSavedSelectedNodeData()
    if s != None:
      drawing = self.nodeManager.getNodeDrawing(s)
      pos = drawing.mainNode.getPos()
      self.cameraManager.setViewBasedOnNodePos(pos)


  def getSavedSelectedNodeData(self):
    s = self.getSelectedNodeData()
    if s != None:
      return s
      
    if s == None:
      return self.getActivatedNodeData()

    return s
    
    
  """ Getters and Setters """
  def setState(self, state):
    self.state = state
    self.state.enter()
  
  # Has to be refactored later
  def getSelectedNodeData(self):
    # Requires interaction between camera and nodemanager, so it is put in map class
    clickedNodePath = self.cameraManager.getClickedNodePath()
    if clickedNodePath is not None:
      return self.nodeManager.getNodeData(clickedNodePath)
    return None

  def getActivatedNodeData(self):
    s = self.nodeManager.dataContainer.nodeDataSettings
    for key in s:
      nodeSettings = s.get(key)
      if nodeSettings.get(DataContainer.SELECTED) != None:
        return self.nodeManager.dataContainer.nodeDataList.get(key)
    return None
  
  
  # Utils
  def clickedOnMapBg(self):
    camManager = self.cameraManager
    return (camManager.getMouseCollisionToPlane(camManager.plane) is None or
      camManager.getClickedNodePath() is None)
    
    
    
    
    
    

  

  

    