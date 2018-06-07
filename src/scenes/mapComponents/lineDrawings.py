
from panda3d.core import NodePath
from panda3d.core import LVecBase3f
from panda3d.core import LineSegs

from utils.utils import Utils

class LineDrawings():
  
  def __init__(self, parentNodePath):
    self.mainNodePath = NodePath("Lines")
    self.mainNodePath.reparentTo(parentNodePath)
    
    self.lineSegs = LineSegs()
    self.lineNodePaths = []
    self.points = []

  def drawLine(self, nodeData, nodeDataList):
    childrenIds = nodeData.get("childrenIds")
     
    if childrenIds is not None:
      self.setParentPoint(nodeData)
      self.setChildrenPoints(nodeData, childrenIds, nodeDataList)
      
  def setParentPoint(self, nodeData):
    parentPos = Utils.getNodeDataPoint(nodeData)
    self.startingPoint(parentPos)
        
  def setChildrenPoints(self, parentNode, childrenIds, nodeDataList):
    for childId in childrenIds:
      childNode = nodeDataList[childId]
      childPos = Utils.getNodeDataPoint(childNode)
      self.endingPoint(childPos)
      self.setParentPoint(parentNode)
      

  def startingPoint(self, point):
    self.lineSegs.moveTo(point)
  
  def endingPoint(self, point):
    self.lineSegs.drawTo(point)
    
    node = self.lineSegs.create()
    lineNodePath = NodePath(node)
    lineNodePath.reparentTo(self.mainNodePath)
    self.lineNodePaths.append(lineNodePath)
    
      
  def clear(self):
    for lineNodePath in self.lineNodePaths:
      lineNodePath.removeNode()
    
    self.lineNodePaths = []
    self.points = []
    
    
    
    
    
    
    
    
    
    
    
    