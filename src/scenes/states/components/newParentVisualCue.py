from utils.utils import Utils

import copy

#Have to refactor later on
class NewParentVisualCue():

  def __init__(self, map):
    self.draggedNode = map.nodeManager.getSelectedNodeData()
    self.draggedDrawing = map.nodeManager.getNodeDrawing(self.draggedNode)
    self.potentialNewParentIds = self.getPotentialNewParentIds(map)

  def draw(self, map):
    nearestNodeDrawing = self.getNearestNodeDrawing(map)
    self.setAllNodeDrawingsNormal(map, self.draggedNode)
    if nearestNodeDrawing is not None:
      self.setAsPotentialParent(nearestNodeDrawing)

  # Loops to all potential new parents
  def getNearestNodeDrawing(self, map):
    width = 35
    height = 10
    nearest = None
    nearestDist = 99999
    for n in self.potentialNewParentIds:
      node = map.nodeManager.nodeDrawings.get(n)
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
        print("mPos: " + str(mPos) + " nearPoint: " + str(nearPoint))

    return nearest

    
  def getPotentialNewParentIds(self, map):
    nList = map.nodeManager.dataContainer.nodeDataList
    newList = {}
    for key in nList:
      newList[key] = nList.get(key)
    return self.removeDragNodeAndChildren(self.draggedNode, newList)


  def removeDragNodeAndChildren(self, draggedNode, nodeList):
    return self.removeFromList(draggedNode, nodeList)
      
  def removeFromList(self, nodeData, nodeList):
    children = Utils.getChildren(nodeData, nodeList)
    if children is not None:
      for child in children:
        self.removeFromList(child, nodeList)

    del nodeList[nodeData.get("id")]
    return nodeList


  def setAllNodeDrawingsNormal(self, map, draggedNode):
    drawings = map.nodeManager.nodeDrawings
    for key, d in drawings.iteritems():
      if draggedNode != d:
        d.setSelected(False)

  def setAsPotentialParent(self, nodeDrawing):
    nodeDrawing.setSelected(True)
