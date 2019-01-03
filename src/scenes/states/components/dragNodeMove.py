from scenes.states.stateManager import StateManager
from scenes.mapComponents.nodeManager import NodeManager
from scenes.states.components.newParentVisualCue import NewParentVisualCue
from direct.task.Task import Task
from utils.utils import Utils

class DragNodeMove():

  def __init__(self, drawingPos, mPos):
    self.defaultPos = drawingPos
    self.posDiff = self.defaultPos - mPos

  def mouseUp(self, map):
    newParentDrawing = map.newParentVisualCue.getNearestNodeDrawing(map)
    selectedDrawing = map.getSelectedNodeDrawing()
    defaultPosBeforeDragging = self.defaultPos

    currentState = map.state
    if self.parentHasChanged(map, newParentDrawing, selectedDrawing) == False:
      self.restoreDraggedNodePosToDefault(selectedDrawing, 
        defaultPosBeforeDragging)
      self.setAsSelected(selectedDrawing, map)
      map.drawData()
      StateManager.switchToStaticMapState(currentState)
    else:
      self.changeParentAndLoadMap(map, newParentDrawing, currentState)
      
  def changeParentAndLoadMap(self, map, newParentDrawing, currentState):
    nm = map.nodeManager
    allData = nm.switchSelectedNodeDrawingParentTo(newParentDrawing)

    newParentData = nm.getNodeDataByNodePath(newParentDrawing.mainNode, 
      nm.allDrawingData, allData)
    allStateData = map.removeFoldedState(newParentData)
    camDict = map.cameraManager.camDict
    StateManager.switchToLoadMapState(currentState, 
      allData, allStateData, camDict)


  def restoreDraggedNodePosToDefault(self, selectedDrawing, 
    defaultPosBeforeDragging):
    selectedDrawing.mainNode.setPos(defaultPosBeforeDragging)

  def setAsSelected(self, drawing, map):
    nm = map.nodeManager
    data = nm.getNodeDataByNodePath(drawing.mainNode, nm.allDrawingData,
      nm.allData)
    map.setStatusAsSelected(data)


  def dragSelectedDrawing(self, map):
    drawing = map.getSelectedNodeDrawing()
    mPos = Utils.getMousePosition(map.showBase)
    self.dragSelectedDrawingImpl(drawing, mPos)

  def dragSelectedDrawingImpl(self, drawing, mPos):
    if mPos is not None:
      newNodePos = mPos + self.posDiff
      drawing.mainNode.setPos(newNodePos)

  def resetPosToDefault(self):
    self.nodeDrawing.mainNode.setPos(self.defaultPos)


  def parentHasChanged(self, map, newParentDrawing, selectedDrawing):
    return newParentDrawing != None

  @staticmethod
  def newInstance(map):
    drawing = map.getSelectedNodeDrawing()
    drawingPos = drawing.mainNode.getPos()
    mPos = Utils.getMousePosition(map.showBase)
    return DragNodeMove(drawingPos, mPos)
  