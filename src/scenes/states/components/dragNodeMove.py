from scenes.states.stateManager import StateManager
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
    if newParentDrawing is None:
      self.restoreDraggedNodePosToDefault(selectedDrawing, 
        defaultPosBeforeDragging)
      StateManager.switchToStaticMapState(currentState)
    else:
      self.changeParentAndLoadMap(map, newParentDrawing, currentState)
      
  def changeParentAndLoadMap(self, map, newParentDrawing, currentState):
    nm = map.nodeManager
    allData = nm.switchSelectedNodeDrawingParentTo(newParentDrawing)

    newParentData = nm.getNodeDataByNodePath(newParentDrawing.mainNode, 
      nm.allDrawingData, allData)
    allStateData = nm.removeFoldedState(newParentData, nm.allStateData)

    StateManager.switchToLoadMapState(currentState, allData, allStateData)


  def restoreDraggedNodePosToDefault(self, selectedDrawing, 
    defaultPosBeforeDragging):
    selectedDrawing.mainNode.setPos(defaultPosBeforeDragging)


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



  @staticmethod
  def newInstance(map):
    drawing = map.getSelectedNodeDrawing()
    drawingPos = drawing.mainNode.getPos()
    mPos = Utils.getMousePosition(map.showBase)
    return DragNodeMove(drawingPos, mPos)
  