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

  def __init__(self, showBase, allData, allStateData):
    self.initializeComponents(showBase, allData, allStateData)

#Initialization
  def initializeComponents(self, showBase, allData, allStateData):
    self.showBase = showBase
    self.initCamera(showBase)
    self.initMapNode(showBase)
    self.initNodeManager(allData, allStateData)
    self.initLineDrawings()
    self.initReingoldTilford()

  def initCamera(self, showBase):
    self.cameraManager = CameraManager(showBase)

  def initMapNode(self, showBase):
    self.mapNode = NodePath("Map")
    self.mapNode.reparentTo(self.showBase.render)

  def initNodeManager(self, allData, allStateData):
    self.nodeManager = NodeManager(allData, allStateData)
  
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

    modAllStatusData = nm.removeAllFieldFromDataMap(nm.allStateData, 
      NodeManager.LATEST_CREATED_DATA)
    nm.allStateData = nm.setAsLatestCreatedData(id, modAllStatusData)
    return nm.allData, nm.allStateData

  def drawData(self):
    loader = self.showBase.loader
    mapNode = self.mapNode

    nm = self.nodeManager
    nm.allDrawingData = nm.clearAllDrawingData()
    filteredData = nm.getFilteredData(nm.allData, nm.allStateData)

    filteredDataWithCoords = self.rTilford.getCoordinates(filteredData)

    nm.drawData(filteredDataWithCoords, nm.allStateData, 
      loader, mapNode, Utils.getNodePosition)

    self.lineDrawings.clear()
    self.lineDrawings.drawLine(filteredDataWithCoords)

  def setStatusAsSelected(self, data):
    nm = self.nodeManager
    removedSelected = nm.removeAllFieldFromDataMap(nm.allStateData, NodeManager.SELECTED)
    nm.allStateData = nm.setStatusAsSelected(data.get('id'), removedSelected)


  def getCoordinates(self, filteredData):
    #Have to refactor rTilford.getCoordinates() to return copy of filteredData
    return copy.deepcopy(self.rTilford.getCoordinates(filteredData))

  def toggleFold(self, data):
    nm = self.nodeManager
    return copy.deepcopy(nm.allData), nm.toggleFoldState(
      data.get(NodeManager.ID), nm.allStateData),

  def removeFoldedState(self, data):
    nm = self.nodeManager
    newState = nm.removeFoldedState(data, nm.allStateData)
    nm.allStateData[data.get(NodeManager.ID)] = newState
      

  #Has to be refactored: Should be encapsulated
  def drawNodeData(self, filteredData, allStateData):
    nodeManager = self.nodeManager   
    nodeManager.clearDataDrawings()
    self.lineDrawings.clear()
    
    loader = self.showBase.loader
    mapNode = self.mapNode
    nodeManager.drawData(filteredData, allStateData, loader, mapNode)
    self.lineDrawings.drawLine(filteredData)

  def setNodeDrawingHeight(self, drawingNode):
    NodeDrawing.ONE_LINE_TEXT_HEIGHT = drawingNode.getActualTextHeight()
    drawingNode.keepTextCenter()

  def setSelectedNodeData(self):
    selectedN = self.getSavedSelectedNodeData()
    allStateData = self.nodeManager.allStateData
    self.nodeManager.allStateData = self.nodeManager.removeAllSelectedField(allStateData)

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

  def getLatestCreatedData(self):
    nm = self.nodeManager
    return nm.getDataWithStatus(NodeManager.LATEST_CREATED_DATA,
      nm.allData, nm.allStateData)

  def removeData(self, data):
    nm = self.nodeManager
    nm.allData = nm.removeData(data, nm.allData)


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
    nm = self.nodeManager
    for key in nm.allStateData:
      statusData = nm.allStateData.get(key)
      if statusData.get(DataContainer.SELECTED) != None:
        return nm.allData.get(key)
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

  def getAllData(self):
    nm = self.nodeManager
    return copy.deepcopy(nm.allData), copy.deepcopy(nm.allStateData)


  def dispose(self):
    self.nodeManager.clearAllDrawingData()
    self.lineDrawings.clear()
    
    
    
    
    
    

  

  

    