#region Imports
import copy

from scenes.cameramanager import CameraManager
from scenes.mapComponents.lineDrawings import LineDrawings
from scenes.mapComponents.nodeData import NodeData
from scenes.mapComponents.nodeDrawing import NodeDrawing
from scenes.mapComponents.nodeManager import NodeManager
from scenes.mapComponents.dataContainer import DataContainer

from scenes.states.components.dragNodeMove import DragNodeMove
from scenes.states.components.newParentVisualCue import NewParentVisualCue
from scenes.states.state import State
from scenes.states.stateManager import StateManager

from panda3d.core import LVecBase3f
from panda3d.core import NodePath

from utils.keyManager import KeyManager
from utils.utils import Utils
from utils.saveManager import SaveManager
from utils.reingoldTilford import ReingoldTilford
#endregion

class Map():
  
  FONT_UBUNTU = None

  def __init__(self, showBase, allData, allStateData, camDict):
    self.initializeComponents(showBase, allData, allStateData, camDict)

  #region Initialization
  def initializeComponents(self, showBase, allData, allStateData, camDict):
    self.showBase = showBase
    self.initCamera(showBase, camDict)
    self.initMapNode(showBase)
    self.initNodeManager(allData, allStateData)
    self.initLineDrawings()
    self.initReingoldTilford()

  def initCamera(self, showBase, camDict):
    self.cameraManager = CameraManager(showBase, camDict)

  def initMapNode(self, showBase):
    self.mapNode = NodePath("Map")
    self.mapNode.reparentTo(self.showBase.render)

  def initNodeManager(self, allData, allStateData):
    self.nodeManager = NodeManager(allData, allStateData)
  
  def initLineDrawings(self):
    self.lineDrawings = LineDrawings(self.mapNode)

  def initReingoldTilford(self):
    self.rTilford = ReingoldTilford()
  #endregion
  
  #region Interfaces for States

  def getCoordinates(self, filteredData):
    #Have to refactor rTilford.getCoordinates() to return copy of filteredData
    return copy.deepcopy(self.rTilford.getCoordinates(filteredData))
  #endregion
          
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

  #region Drawing
  def drawData(self):
    loader = self.showBase.loader
    mapNode = self.mapNode

    nm = self.nodeManager
    nm.allDrawingData = nm.clearAllDrawingData()
    filteredData = nm.getFilteredData(nm.allData, nm.allStateData)
    startingData = nm.getStartingData(filteredData, nm.allStateData)

    filteredDataWithCoords = self.rTilford.getCoordinates(startingData, 
      filteredData)

    nm.drawData(filteredDataWithCoords, nm.allStateData, 
      loader, mapNode, Utils.getNodePosition)

    self.lineDrawings.clear()
    self.lineDrawings.drawLine(filteredDataWithCoords)

  def getSelectedNodeDrawing(self):
    nodeData = self.getActivatedNodeData()
    return self.nodeManager.getNodeDrawing(nodeData)
  #endregion
  
  #region Data
  def createNodeData(self, parentId, name, recheckLastId = False):
    # Have to review the purpose of the recheckLastId
    # Need to implement it inside the nodeManager to simplify reading of code
    # return self.nodeManager.createNodeData(parentId, name, recheckLastId)
    nm = self.nodeManager
    allData, newData = nm.createNodeData(parentId, name, recheckLastId)

    nAllState = nm.removeAllLatestCreatedField()
    nm.allStateData = nm.setAsLatestCreatedData(newData.get(NodeManager.ID),
      nAllState)
    
    nm.allData = allData
    return nm.allData, nm.allStateData

  def setSelectedNodeData(self):
    selectedN = self.getSavedSelectedNodeData()
    allStateData = self.nodeManager.allStateData
    self.nodeManager.allStateData = self.nodeManager.removeAllSelectedField(allStateData)

  def removeData(self, data):
    if data.get(NodeManager.ID) == NodeManager.MAIN_ID:
      return None

    nm = self.nodeManager
    nm.allData = nm.removeData(data, nm.allData)
    return nm.allData
  
  def getActivatedNodeData(self):
    return self.nodeManager.getActivatedNodeData()
  
  def getSavedSelectedNodeData(self):
    # Should be refactored later on
    node = self.getSelectedNodeData()
    if node is None:
      node = self.getActivatedNodeData()
    return node

  def getSelectedNodeData(self):
    # Has to be refactored later
    # Requires interaction between camera and nodemanager, so it is put in map class
    nm = self.nodeManager

    clickedNodePath = self.cameraManager.getClickedNodePath()
    if clickedNodePath is not None:
      dDrawing = nm.allDrawingData
      filteredData = nm.allData
      return nm.getNodeDataByNodePath(clickedNodePath, dDrawing, filteredData)
    return None
  #endregion

  #region StateData
  def removeFoldedState(self, data):
    nm = self.nodeManager
    nm.allStateData = nm.removeFoldedStateWithValidity(data, nm.allStateData)
    return nm.allStateData

  def removeLatestCreateDataStateByData(self, data):
    nm = self.nodeManager
    nm.allStateData = nm.removeDataState(data, nm.allStateData,
      NodeManager.LATEST_CREATED_DATA)
    
  def getModifiedState(self, data, stateDataName):
    nm = self.nodeManager
    return nm.getModifiedState(data, stateDataName)

  def editNodeData(self, dataId, newText):
    nm = self.nodeManager
    nm.allData.get(dataId)[NodeManager.NAME] = newText

  def toggleFold(self, data):
    nm = self.nodeManager
    return copy.deepcopy(nm.allData), nm.toggleFoldState(
      data.get(NodeManager.ID), nm.allStateData)

  def setStatusAsSelected(self, data):
    self.setStatusAsSelectedById(data.get(NodeData.ID))

  def setStatusAsSelectedById(self, dataId):
    nm = self.nodeManager
    removedSelected = nm.removeAllFieldFromDataMap(nm.allStateData, NodeManager.SELECTED)
    nm.allStateData = nm.setStatusAsSelected(dataId, removedSelected)

  def getLatestCreatedData(self):
    nm = self.nodeManager
    return nm.getDataWithStatus(NodeManager.LATEST_CREATED_DATA,
      nm.allData, nm.allStateData)
  #endregion

  #region Others
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

  def dataHasChildren(self, data):
    return self.nodeManager.dataHasChildren(data)
  #endregion
  
  def dispose(self):
    self.nodeManager.clearAllDrawingData()
    self.lineDrawings.clear()

  #region DragNodeState
  def initDragNodeState(self):
    self.dragNodeMove = DragNodeMove.newInstance(self)
    self.newParentVisualCue = NewParentVisualCue.newInstance(self)

  def draggingNode(self):
    self.dragNodeMove.dragSelectedDrawing(self)
    self.newParentVisualCue.draw(self)

  def dragNodeMouseUp(self):
    self.dragNodeMove.mouseUp(self)

  def potentialNewParentNode(self, newParentDrawing):
    nm = self.nodeManager
    data = nm.getNodeDataByNodePath(newParentDrawing.mainNode, 
      nm.allDrawingData, nm.allData)
    dataId = data.get(NodeManager.ID)
    stateData = nm.allStateData.get(dataId)
    self.newParentVisualCue.setAsPotentialParent(stateData,
      newParentDrawing)
  #endregion

  #region Create Node and Edit Node States
  def startEditNode(self, selectedData, onKeyDownFn):
    dataId = selectedData.get(NodeManager.ID)
    KeyManager.setupKeyListener(self.showBase, onKeyDownFn, 
      dataId)

  def onKeyDown(self, keyname, onEnterDownFn, extraParams):
    self.nodeManager.onKeyDown(keyname, onEnterDownFn, extraParams)
  #endregion

  #region StaticMapState
  def toggleAncestorShowHide(self):
    selectedData = self.getActivatedNodeData()
    nm = self.nodeManager
    nm.toggleAncestorShowHide(selectedData)
    self.drawData()

  def toggleChildrenShowHide(self):
    selectedData = self.getActivatedNodeData()
    nm = self.nodeManager
    if nm.toggleChildrenShowHide(selectedData):
      self.drawData()
  #endregion

  #region CreateSibling
  def getParent(self, data):
    return self.nodeManager.getParent(data);
  #endregion
    
    
    
    
    

  

  

    