from utils import Utils
import copy

class ReingoldTilford():
  NODE_SIZE = 1.0

  def __init__(self):
    self.checkedConflictedIds = {}

  # Returns points to represent tree
    # 2D jagged list of points?
  def getCoordinates(self, nodeList, enableCheckForConflicts = True):
    mainNode = nodeList["1"]
    self.firstTraversal(mainNode, nodeList, enableCheckForConflicts)
    self.calcFinalPos(mainNode, nodeList, 0)

  def firstTraversal(self, mainNode, nodeList, enableCheckForConflicts = False):
    self.setInitialX(mainNode, nodeList, enableCheckForConflicts)
    

  def calcFinalPos(self, node, nodeList, modSum):
    name = node.get("name")
    node["x"] += modSum
    if node.has_key("mod") is False:
      node["mod"] = 0
    modSum += node.get("mod")

    children = Utils.getChildren(node, nodeList)
    if children is not None:
      for child in children:
        self.calcFinalPos(child, nodeList, modSum)

  def setInitialX(self, node, nodeList, enableCheckForConflicts = False):
    self.setInitialXRelativeToChildren(node, nodeList, enableCheckForConflicts)
    self.solveConflictingX(node, nodeList, enableCheckForConflicts)
    return nodeList, self.checkedConflictedIds
  
  
      
  def setInitialXRelativeToChildren(self, node, nodeList, enableCheckForConflicts = False):
    children = Utils.getChildren(node, nodeList)
    if children is not None:
      for child in children:
        self.setInitialX(child, nodeList, enableCheckForConflicts)
     
    self.setLeafInitialX(children, node, nodeList)
    self.setOneChildNodeInitialX(children, node, nodeList)
    self.setManyChidrenNodeInitialX(children, node, nodeList)
    
  def solveConflictingX(self, node, nodeList, enableCheckForConflicts):
    if self.checkForConflicts(node, nodeList, enableCheckForConflicts) is True:
      self.checkedConflictedIds[node["id"]] = True
      self.fixConflictingX(node, nodeList)
  
  
        
  def setLeafInitialX(self, children, node, nodeList):
    if children is not None:  # Leaf node
      return
      
    if self.isLeftMost(node, nodeList):
      node["x"] = 0.0
    else:
      leftSibling = self.getLeftSibling(node, nodeList)
      node["x"] = leftSibling.get("x") + ReingoldTilford.NODE_SIZE
      
  def setOneChildNodeInitialX(self, children, node, nodeList):
    if Utils.dictLen(children) is not 1:
      return
    
    if self.isLeftMost(node, nodeList):
      node["x"] = children[0].get("x")
    else:
      leftSibling = self.getLeftSibling(node, nodeList)
      node["x"] = leftSibling.get("x") + ReingoldTilford.NODE_SIZE
      firstChild = Utils.getChildren(node, nodeList)
      node["mod"] = node["x"] - firstChild[0]["x"]
        
  def setManyChidrenNodeInitialX(self, children, node, nodeList):
    if Utils.dictLen(children) <= 1:
      return
    
    midX = self.getMidX(node, nodeList)
    if self.isLeftMost(node, nodeList):
      node["x"] = midX
    else:
      leftSibling = self.getLeftSibling(node, nodeList)
      node["x"] = leftSibling.get("x") + ReingoldTilford.NODE_SIZE
      node["mod"] = node["x"] - midX


  def fixConflictingX(self, node, nodeList):
    leftContour = {}
    self.getLeftContour(node, nodeList, 0, leftContour)

    startingDepth = int(node["depth"])
    leftSibling = self.getLeftMostSibling(node, nodeList)
    
    while leftSibling is not None and leftSibling != node:
      rightContour = {}
      self.getRightContour(leftSibling, nodeList, 0, rightContour)
      
      endingDepth = int(self.getSameDepthThatHasContourValue(rightContour, leftContour))
      
      shiftValue = 0.0
      for depth in range(startingDepth, endingDepth + 1):
        rValue = rightContour[str(depth)]
        lValue = leftContour[str(depth)]
        
        minX = rValue + ReingoldTilford.NODE_SIZE
        if lValue < minX:
          tmpShiftValue = minX - lValue
          
          if tmpShiftValue > shiftValue:
            shiftValue = tmpShiftValue
      
      if shiftValue > 0:
        node["x"] += shiftValue
        node["mod"] += shiftValue
#       self.centerNodesBetween(node, leftSibling, nodeList)
      
      leftSibling = self.getRightSibling(leftSibling, nodeList)
        
      
  def checkForConflicts(self, node, nodeList, enableCheckForConflicts):
    children = Utils.getChildren(node, nodeList)
    return (self.isLeftMost(node, nodeList) is False and children is not None
            and enableCheckForConflicts)

  
  def getSameDepthThatHasContourValue(self, rightContour, leftContour):
    rightMax = max(rightContour, key=int)
    leftMax = max(leftContour, key=int)
    return min(rightMax, leftMax)

  def getNextSibling(self, node, nodeList):
    parentId = node.get("parentId")
    if parentId is None or nodeList[parentId] is None or self.isRightMost(node, nodeList):
      return None

    parent = nodeList[parentId]
    children = Utils.getChildren(parent, nodeList)
    return children[children.index(node) + 1]


  def centerNodesBetween(self, leftNode, rightNode, nodeList):
    parentId = leftNode.get("parentId")
    parent = nodeList[parentId]
    children = Utils.getChildren(parent, nodeList)
    leftIndex = children.index(rightNode)
    rightIndex = children.index(leftNode)

    numNodesBetween = (rightIndex - leftIndex) - 1
#     print("numNodesBetween " + str(leftIndex))
    if numNodesBetween > 0:
#       print("numNodesBetween")
      leftX = leftNode.get("x")
      rightX = rightNode.get("x")
      distBetweenNodes = (leftX - rightX) / (numNodesBetween + 1)

      count = 1
      startingIndex = leftIndex + 1
      endingIndex = rightIndex - 1
      for index in range(startingIndex, endingIndex):
        middleNode = children[index]

        desiredX = rightX + (distBetweenNodes * count)
        offset = desiredX - middleNode.get("x")
        middleNode["x"] += offset
        middleNode["mod"] += offset

        count += 1

      self.fixConflictingX(rightNode, nodeList)

  def getLeftContour(self, node, nodeList, modSum, contour):
    y = node.get("depth")
    x = node.get("x")
    # print("y " + str(y))
    if contour.has_key(y):
      contour[y] = min(contour[y], x + modSum)
    else:
      contour[y] = x + modSum
    
    if node.get("mod") is None:
      node["mod"] = 0
    modSum += node.get("mod")
    children = Utils.getChildren(node, nodeList)
    if children is not None:
      for child in children:
        self.getLeftContour(child, nodeList, modSum, contour)

  def getRightContour(self, node, nodeList, modSum, contour):
    y = node.get("depth")
    x = node.get("x")
    if contour.has_key(y):
      contour[y] = max(contour[y], x + modSum)
    else:
      contour[y] = x + modSum
    
    if node.get("mod") is None:
      node["mod"] = 0
    modSum += node.get("mod")
    children = Utils.getChildren(node, nodeList)
    if children is not None:
      for child in children:
        self.getRightContour(child, nodeList, modSum, contour)

  def getLeftMostSibling(self, node, nodeList):
    parentId = node.get("parentId")
    if parentId is None or nodeList[parentId] is None:
      return None
    
    parent = nodeList[parentId]
    children = Utils.getChildren(parent, nodeList)
    return children[0]

  def isLeftMost(self, node, nodeList):
    parentId = node.get("parentId")
    if parentId is None or nodeList[parentId] is None:
      return True

    parent = nodeList[parentId]
    children = Utils.getChildren(parent, nodeList)

    return children[0] == node

  def isRightMost(self, node, nodeList):
    parentId = node.get("parentId")
    if parentId is None or nodeList[parentId] is None:
      return True

    parent = nodeList[parentId]
    children = Utils.getChildren(parent, nodeList)

    return children[len(children) - 1] == node

  def getLeftSibling(self, node, nodeList):
    parent = nodeList[node.get("parentId")]
    children = Utils.getChildren(parent, nodeList)

    return children[children.index(node) - 1]
  
  def getRightSibling(self, node, nodeList):
    parent = nodeList[node.get("parentId")]
    children = Utils.getChildren(parent, nodeList)
    
    rightSiblingIndex = children.index(node) + 1
    if rightSiblingIndex < len(children):
      return children[rightSiblingIndex]
    return None
  
  def getMidX(self, node, nodeList):
    children = Utils.getChildren(node, nodeList)
    leftMostChild = children[0]
    rightMostChild = children[len(children) - 1]
    leftX = leftMostChild.get("x")
    rightX = rightMostChild.get("x")
    midX = (leftX + rightX) / 2
    return midX
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
