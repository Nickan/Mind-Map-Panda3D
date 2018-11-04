from state import State
from scenes.mapComponents.nodeDataFilter import NodeDataFilter
from scenes.mapComponents.nodeData import NodeData
from scenes.states.components.dragNodeMove import DragNodeMove
from utils.utils import Utils

import copy

class DragNodeState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self):
    self.dragNodeMove = DragNodeMove(self.map, self.onRelease)

  def exit(self):
    print("exit DragNodeState")


  def onRelease(self, nearestNodeDrawing):
    if nearestNodeDrawing is None:
      self.switchToStaticMapState()
    else:
      self.attachDraggedNodeToNearestNode(nearestNodeDrawing)
      self.switchToLoadMapState()

  def setDepth(self, parentDepth, nodeData, nodeList):
    currentDepth = parentDepth + 1
    nodeData[NodeData.DEPTH] = currentDepth
    children = Utils.getChildren(nodeData, nodeList)
    if children is not None:
      for child in children:
        self.setDepth(currentDepth, child, nodeList)


  def switchToStaticMapState(self):
    from scenes.states.staticMapState import StaticMapState
    self.map.changeState(StaticMapState(self.map))


  def switchToLoadMapState(self):
    from scenes.states.loadMapState import LoadMapState
    self.map.changeState(LoadMapState(self.map))

  def attachDraggedNodeTo(self, nodeDrawing):
    nodeList = self.map.nodeManager.dataContainer.nodeDataList

    selectedNode = self.map.getActivatedNodeData()
    parentNode = nodeList.get(selectedNode.get("parentId"))
    newParent = nodeList.get(nearestNodeDrawing.id)

    pIds = parentNode.get(NodeData.CHILDREN_IDS)
    pIds.remove(selectedNode.get(NodeData.ID))
    selectedNode[NodeData.PARENT_ID] = newParent.get("id")
    self.setDepth(newParent.get("depth"), selectedNode, nodeList)

    if newParent.get(NodeData.CHILDREN_IDS) is None:
      newParent[NodeData.CHILDREN_IDS] = [selectedNode.get(NodeData.ID)]
    else:
      nIds = newParent.get(NodeData.CHILDREN_IDS)
      nIds.append(selectedNode.get(NodeData.ID))

    self.map.nodeManager.dataContainer.nodeDataList = nodeList













