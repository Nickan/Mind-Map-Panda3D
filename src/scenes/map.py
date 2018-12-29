import copy

from scenes.cameramanager import CameraManager
from scenes.mapComponents.lineDrawings import LineDrawings
from scenes.mapComponents.nodeDrawing import NodeDrawing
from scenes.mapComponents.nodeManager import NodeManager
from scenes.mapComponents.dataContainer import DataContainer
from scenes.states.state import State

from panda3d.core import LVecBase3f
from panda3d.core import NodePath

from utils.utils import Utils
from utils.saveManager import SaveManager
from utils.reingoldTilford import ReingoldTilford

class Map():
  
  FONT_UBUNTU = None

  def __init__(self, showBase):
    self.initializeComponents(showBase)

#Initialization
  def initializeComponents(self, showBase):
    self.showBase = showBase
    self.initCamera()
    self.initMapNode(showBase)
    self.initNodeManager()
    self.initLineDrawings()
    self.initReingoldTilford()

  def initCamera(self):
    self.cameraManager = CameraManager(self.showBase)

  def initMapNode(self, showBase):
    self.mapNode = NodePath("Map")
    self.mapNode.reparentTo(self.showBase.render)

  def initNodeManager(self):
    self.nodeManager = NodeManager()
  
  def initLineDrawings(self):
    self.lineDrawings = LineDrawings(self.mapNode)

  def initReingoldTilford(self):
    self.rTilford = ReingoldTilford()

  
#Interfaces for States
  # Have to review the purpose of the recheckLastId
  def createNodeData(self, parentId, name, recheckLastId = False):
    nm = self.nodeManager
    newData = nm.createNodeData(parentId, name, recheckLastId, nm.allData,
      Utils.getUniqueId)
    id = newData['id']
    nm.allData[id] = newData

    modAllStatusData = nm.removeFieldFromDataMap(nm.allStatusData, 
      NodeManager.LATEST_CREATED_DATA)
    nm.allStatusData = nm.setAsLatestCreatedData(id, modAllStatusData)

  def drawData(self):
    loader = self.showBase.loader
    mapNode = self.mapNode

    nm = self.nodeManager
    nm.allDrawingData = nm.clearAllDrawingData()
    filteredData = nm.getFilteredData(nm.allData, nm.allStatusData)

    filteredDataWithCoords = self.rTilford.getCoordinates(filteredData)

    nm.drawData(filteredDataWithCoords, nm.allStatusData, 
      loader, mapNode, Utils.getNodePosition)

    self.lineDrawings.clear()
    self.lineDrawings.drawLine(filteredDataWithCoords)

  def setStatusAsSelected(self, data):
    nm = self.nodeManager
    removedSelected = nm.removeFieldFromDataMap(nm.allStatusData, NodeManager.SELECTED)
    nm.allStatusData = nm.setStatusAsSelected(data.get('id'), removedSelected)


  def getCoordinates(self, filteredData):
    #Have to refactor rTilford.getCoordinates() to return copy of filteredData
    return copy.deepcopy(self.rTilford.getCoordinates(filteredData))

  #Has to be refactored: Should be encapsulated
  def drawNodeData(self, filteredData, allStatusData):
    nodeManager = self.nodeManager   
    nodeManager.clearDataDrawings()
    self.lineDrawings.clear()
    
    loader = self.showBase.loader
    mapNode = self.mapNode
    nodeManager.drawData(filteredData, allStatusData, loader, mapNode)
    self.lineDrawings.drawLine(filteredData)

  def setNodeDrawingHeight(self, drawingNode):
    NodeDrawing.ONE_LINE_TEXT_HEIGHT = drawingNode.getActualTextHeight()
    drawingNode.keepTextCenter()

  def setSelectedNodeData(self):
    selectedN = self.getSavedSelectedNodeData()
    allStatusData = self.nodeManager.allStatusData
    self.nodeManager.allStatusData = self.nodeManager.removeAllSelectedField(allStatusData)

  # Has to be refactored later
  def getSelectedNodeData(self):
    # Requires interaction between camera and nodemanager, so it is put in map class
    clickedNodePath = self.cameraManager.getClickedNodePath()
    if clickedNodePath is not None:
      dDrawing = self.nodeManager.allDrawingData
      filteredData = self.nodeManager.allData
      return self.nodeManager.getNodeData(clickedNodePath, dDrawing, 
        filteredData)
    return None


#2nd Level interfaces
  # Should be refactored later on
  def getSavedSelectedNodeData(self):
    node = self.getSelectedNodeData()
    if node is None:
      node = self.getActivatedNodeData()
    return node

#3rd Level Interfaces
  
#Others

  
    
  def editNodeData(self, dataId, newText):
    nm = self.nodeManager
    nm.allData.get(dataId)[NodeManager.NAME] = newText
    

    # self.drawNodeData(nodeManager.dataContainer)
    
  def deleteNodeData(self, nodeDataToDelete):
    nodeManager = self.nodeManager
    nodeManager.deleteNodeData(nodeDataToDelete)

    nodeDataList = nodeManager.dataContainer.nodeDataList
    SaveManager.clearNodeDataList(nodeDataList)
    nodeManager.tree.getCoordinates(nodeDataList)
    self.drawNodeData(nodeManager.dataContainer)
      
  

  def setCameraViewToSelectedNode(self):
    s = self.getActivatedNodeData()
    if s != None:
      drawing = self.nodeManager.getNodeDrawing(s)
      pos = drawing.mainNode.getPos()
      self.cameraManager.setViewBasedOnNodePos(pos)
    
    
  """ Getters and Setters """
  def setState(self, state):
    self.state = state
    self.state.enter()


  def getSelectedNodeDrawing(self):
    nodeData = self.getSavedSelectedNodeData()
    return self.nodeManager.getNodeDrawing(nodeData)

  def getActivatedNodeData(self):
    s = self.nodeManager.allStatusData
    for key in s:
      statusData = s.get(key)
      if statusData.get(DataContainer.SELECTED) != None:
        return self.nodeManager.allData.get(key)
    return None

  
  # Utils
  def clickedOnMapBg(self):
    camManager = self.cameraManager
    return (camManager.getMouseCollisionToPlane(camManager.plane) is None or
      camManager.getClickedNodePath() is None)

  def changeState(self, state):
    self.state.exit()
    self.state = state
    self.state.enter()
    
    
    
    
    
    

  

  

    