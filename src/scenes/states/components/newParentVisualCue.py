from utils.utils import Utils

import copy

#Have to refactor later on
class NewParentVisualCue():

  def __init__(self, map):
    self.potentialNewParentData = None

  def draw(self, map):
    mPos = Utils.getMousePosition(map.showBase)
    draggedNode = map.getActivatedNodeData()
    draggedDrawing = map.getSelectedNodeDrawing()
    allDrawingData = map.nodeManager.allDrawingData

    aNode = map.getActivatedNodeData()
    if self.potentialNewParentData is None:
      self.potentialNewParentData = self.getPotentialNewParentData(map, aNode)
    
    getDistSql2DFn = Utils.getDistSqr2D
    collidesRectFn = Utils.collidesRect
    getCoordsFn = map.cameraManager.getCoordinates

    pNewParentFn = map.potentialNewParentNode

    self.drawImpl(mPos, draggedNode, draggedDrawing, allDrawingData, 
      self.potentialNewParentData, getDistSql2DFn, collidesRectFn,
      getCoordsFn, pNewParentFn)

  def drawImpl(self, mPos, draggedNode, draggedDrawing, allDrawingData, 
    potentialNewParentData, getDistSql2DFn, collidesRectFn, getCoordsFn,
    pNewParentFn):
    if mPos is not None:
      nearestNodeDrawing = self.getNearestNodeDrawingImpl(draggedNode, 
        draggedDrawing, allDrawingData, potentialNewParentData, getDistSql2DFn,
        collidesRectFn, getCoordsFn)
      self.setAllNodeDrawingsNormal(allDrawingData, draggedNode)
      if nearestNodeDrawing is not None:
        pNewParentFn(nearestNodeDrawing)

  def getPotentialNewParentData(self, map, selectedNode):
    nm = map.nodeManager
    removedChildren = nm.removeChildren(selectedNode, nm.allData)
    hiddenData = nm.removeHiddenDataByFoldedState(nm.allData, nm.allStateData)
    return hiddenData
    


  # Loops to all potential new parents
  def getNearestNodeDrawing(self, map):
    mPos = Utils.getMousePosition(map.showBase)
    draggedNode = map.getActivatedNodeData()
    draggedDrawing = map.getSelectedNodeDrawing()
    allDrawingData = map.nodeManager.allDrawingData

    aNode = map.getActivatedNodeData()
    potentialNewParentData = self.getPotentialNewParentData(map, aNode)
    
    getDistSql2DFn = Utils.getDistSqr2D
    collidesRectFn = Utils.collidesRect
    getCoordsFn = map.cameraManager.getCoordinates
    return self.getNearestNodeDrawingImpl(draggedNode, 
      draggedDrawing, allDrawingData, potentialNewParentData, getDistSql2DFn,
      collidesRectFn, getCoordsFn)


  def getNearestNodeDrawingImpl(self, draggedNode, draggedDrawing, allDrawings, 
    potentialNewParentData, getDistSql2DFn, collidesRectFn,
    getCoordsFn):

    width = 35
    height = 10
    nearest = None
    nearestDist = 99999
    for pId in potentialNewParentData:
      node = allDrawings.get(pId)
      if node is None:
        print("pId " + str(pId))
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

  def setAllNodeDrawingsNormal(self, drawingsData, draggedNode):
    for key, d in drawingsData.items():
      if draggedNode != d:
        d.setSelected(False)

  def setAsPotentialParent(self, nodeDrawing):
    nodeDrawing.setSelected(False, True)

  
  @staticmethod
  def newInstance(map):
    return NewParentVisualCue(map)
