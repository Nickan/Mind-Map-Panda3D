from utils.utils import Utils

import copy

#Have to refactor later on
class NewParentVisualCue():

  def __init__(self, map):
    self.potentialNewParentIds = None

  def draw(self, map):
    mPos = Utils.getMousePosition(map.showBase)
    draggedDrawing = map.getSelectedNodeDrawing()
    allDrawingData = map.nodeManager.allDrawingData

    aNode = map.getActivatedNodeData()
    if self.potentialNewParentIds is None:
      self.potentialNewParentIds = self.getPotentialNewParentIds(map, aNode)
    
    getDistSql2DFn = Utils.getDistSqr2D
    collidesRectFn = Utils.collidesRect
    getCoordsFn = map.cameraManager.getCoordinates
    self.drawImpl(mPos, draggedDrawing, allDrawingData, 
      self.potentialNewParentIds, getDistSql2DFn, collidesRectFn,
      getCoordsFn)

  def drawImpl(self, mPos, draggedDrawing, allDrawingData, 
    potentialNewParentIds, getDistSql2DFn, collidesRectFn, getCoordsFn):
    if mPos is not None:
      nearestNodeDrawing = self.getNearestNodeDrawing(draggedDrawing,
      allDrawingData, potentialNewParentIds, getDistSql2DFn, collidesRectFn,
        getCoordsFn)

    # nearestNodeDrawing = self.getNearestNodeDrawing(map)
    # self.setAllNodeDrawingsNormal(map, self.draggedNode)
    # if nearestNodeDrawing is not None:
    #   self.setAsPotentialParent(nearestNodeDrawing)

  def getPotentialNewParentIds(self, map, selectedNode):
    nm = map.nodeManager
    return nm.removeChildren(selectedNode, nm.allData)

  # Loops to all potential new parents
  def getNearestNodeDrawing(self, draggedDrawing, allDrawings, 
    potentialNewParentIds, getDistSql2DFn, collidesRectFn,
    getCoordsFn):

    width = 35
    height = 10
    nearest = None
    nearestDist = 99999
    for pId in potentialNewParentIds:
      node = allDrawings.get(pId)
      nPos = node.mainNode.getPos()
      dPos = draggedDrawing.mainNode.getPos()
      curDist = getDistSql2DFn(nPos, dPos)
      if ( (collidesRectFn(nPos, dPos, width, height) is True) and
        (curDist < nearestDist) ):
        nearestDist = curDist
        nearest = node

        # For debugging
        xd = nPos.x - dPos.x
        yd = nPos.y - dPos.y
        dist = (xd * xd) + (yd * yd)
        # print("xd: " + str(xd * xd) + " yd: " + str(yd * yd) + " dist: " + str(dist))

        mPos, nearPoint = getCoordsFn()
        # print("mPos: " + str(mPos) + " nearPoint: " + str(nearPoint))

    return nearest

  def removeDragNodeAndChildren(self, draggedNode, allData):
    return self.removeFromList(draggedNode, allData)
      
  def removeFromList(self, nodeData, allData):
    newList = copy.deepcopy(allData)

    children = Utils.getChildren(nodeData, newList)
    if children is not None:
      for child in children:
        self.removeFromList(child, newList)

    del newList[nodeData.get("id")]
    return newList


  def setAllNodeDrawingsNormal(self, map, draggedNode):
    drawings = map.nodeManager.allDrawingData
    for key, d in drawings.items():
      if draggedNode != d:
        d.setSelected(False)

  def setAsPotentialParent(self, nodeDrawing):
    nodeDrawing.setSelected(False, True)

  
  @staticmethod
  def newInstance(map):
    return NewParentVisualCue(map)
