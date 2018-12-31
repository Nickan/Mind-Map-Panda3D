from utils.utils import Utils

import copy

#Have to refactor later on
class NewParentVisualCue():

  # def __init__(self, map):
    # self.draggedNode = map.nodeManager.getSelectedNodeData()
    # self.draggedDrawing = map.nodeManager.getNodeDrawing(self.draggedNode)
    # self.potentialNewParentIds = self.getPotentialNewParentIds(map)

  def draw(self, mPos, allDrawingData):
    if mPos is not None:
      print('in progress')
      
    # nearestNodeDrawing = self.getNearestNodeDrawing(map)
    # self.setAllNodeDrawingsNormal(map, self.draggedNode)
    # if nearestNodeDrawing is not None:
    #   self.setAsPotentialParent(nearestNodeDrawing)

  # Loops to all potential new parents
  def getNearestNodeDrawing(self, map):
    allDrawings = map.nodeManager.allDrawingData

    width = 35
    height = 10
    nearest = None
    nearestDist = 99999
    for n in self.potentialNewParentIds:
      node = allDrawings.get(n)
      nPos = node.mainNode.getPos()
      dPos = self.draggedDrawing.mainNode.getPos()
      curDist = Utils.getDistSqr2D(nPos, dPos)
      if ( (Utils.collidesRect(nPos, dPos, width, height) is True) and
        (curDist < nearestDist) ):
        nearestDist = curDist
        nearest = node

        # For debugging
        xd = nPos.x - dPos.x
        yd = nPos.y - dPos.y
        dist = (xd * xd) + (yd * yd)
        # print("xd: " + str(xd * xd) + " yd: " + str(yd * yd) + " dist: " + str(dist))

        mPos, nearPoint = map.cameraManager.getCoordinates()
        # print("mPos: " + str(mPos) + " nearPoint: " + str(nearPoint))

    return nearest

    
  def getPotentialNewParentIds(self, map):
    # return self.removeDragNodeAndChildren(self.draggedNode,
    #   map.nodeManager.allData)
    nm = map.nodeManager
    return nm.removeChildren(self.draggedNode, nm.allData)

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
