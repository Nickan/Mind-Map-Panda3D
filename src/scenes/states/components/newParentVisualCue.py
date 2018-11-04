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
    maxDist = 25
    nearestDist = 999999
    nearest = None
    for n in self.potentialNewParentIds:
      node = map.nodeManager.nodeDrawings.get(n)
      nPos = node.mainNode.getPos()
      dPos = self.draggedDrawing.mainNode.getPos()
      curDist = Utils.getDistSqr2D(nPos, dPos)
      if Utils.isInRange(curDist, maxDist) is True and curDist < nearestDist:
        nearestDist = curDist
        nearest = node
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
