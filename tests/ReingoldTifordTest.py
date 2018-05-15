import unittest

import sys
from __builtin__ import int
sys.path.append('../src')

from utils.reingoldTilford import ReingoldTilford
from utils.utils import Utils

class ReingoldTilfordTest(unittest.TestCase):
  
  def testLocalXRelativeToParentNode(self):
    Utils.LAST_ASSIGNED_ID = 1
    nodeList = Utils.convertToNodes(Utils.getJson("start.json"))
     
    reingold = ReingoldTilford()
    coords, checkedForConflictIds = reingold.setInitialX(nodeList[1], nodeList)
     
    name = "1"  # Main node
    node = coords[1]
    self.assertTrue(self.verifyNodeName(node, name),  name + " name is wrong")
    self.assertTrue(self.verifyNodeX(node, 2), name + " x is wrong")
     
    # Main node children
    name = "2"
    node = coords[2]
    self.assertTrue(self.verifyNodeName(node, name),  name + " name is wrong")
    self.assertTrue(self.verifyNodeX(node, 1), name + " x is wrong")
     
    name = "3"
    node = coords[3]
    self.assertTrue(self.verifyNodeName(node, name),  name + " name is wrong")
    self.assertTrue(self.verifyNodeX(node, 2), name + " x is wrong")
    self.assertTrue(self.verifyMod(node, 2), name + " mod is wrong")
     
    name = "4"
    node = coords[4]
    self.assertTrue(self.verifyNodeName(node, name),  name + " name is wrong")
    self.assertTrue(self.verifyNodeX(node, 3), name + " x is wrong")
    self.assertTrue(self.verifyMod(node, 2.5), name + " mod is wrong")
    # Main node children
     
    # Node 2 children
    name = "5"
    node = coords[5]
    self.assertTrue(self.verifyNodeName(node, name),  name + " name is wrong")
    self.assertTrue(self.verifyNodeX(node, 0), name + " x is wrong")
     
    name = "6"
    node = coords[6]
    self.assertTrue(self.verifyNodeName(node, name),  name + " name is wrong")
    self.assertTrue(self.verifyNodeX(node, 1), name + " x is wrong")
     
    name = "7"
    node = coords[7]
    self.assertTrue(self.verifyNodeName(node, name),  name + " name is wrong")
    self.assertTrue(self.verifyNodeX(node, 2), name + " x is wrong")
    # Node 2 children
     
    # Node 3 child
    name = "8"
    node = coords[8]
    self.assertTrue(self.verifyNodeName(node, name),  name + " name is wrong")
    self.assertTrue(self.verifyNodeX(node, 0), name + " x is wrong")
     
     
    # Node 4 childre
    name = "9"
    node = coords[9]
    self.assertTrue(self.verifyNodeName(node, name),  name + " name is wrong")
    self.assertTrue(self.verifyNodeX(node, 0), name + " x is wrong")
     
    name = "10"
    node = coords[10]
    self.assertTrue(self.verifyNodeName(node, name),  name + " name is wrong")
    self.assertTrue(self.verifyNodeX(node, 1), name + " x is wrong")
  
  
  def testNodesToCheckForConflictingX(self):
    Utils.LAST_ASSIGNED_ID = 1
    nodeList = Utils.convertToNodes(Utils.getJson("start.json"))
         
    reingold = ReingoldTilford()
    
    name = "3"
    node = nodeList[int(name)]
    self.assertTrue(reingold.checkForConflicts(node, nodeList, True), 
                    name + " is not being checked for conflict")
     
    name = "4"  # Main node
    node = nodeList[int(name)]
    self.assertTrue(reingold.checkForConflicts(node, nodeList, True), 
                    name + " is not being checked for conflict")
    
    
  
  def testContourList(self):
    Utils.LAST_ASSIGNED_ID = 1
    nodeList = Utils.convertToNodes(Utils.getJson("start.json"))
     
    reingold = ReingoldTilford()
    coords, checkedForConflictIds = reingold.setInitialX(nodeList[1], nodeList)
    
    name = "3"
    node = nodeList[int(name)]
    
    leftSibling = reingold.getLeftSibling(node, nodeList)
    rightContour = {}
    reingold.getRightContour(leftSibling, 0, rightContour)
    
    depth = 1
    self.assertTrue(rightContour[depth] == 1,  "node " + name + " " + 
                    str(depth) + " depth right contour is wrong ")
    
    depth = 2
    self.assertTrue(rightContour[depth] == 2, "node " + name + " " + 
                    str(depth) + " depth right contour is wrong ")
    
    leftContour = {}
    reingold.getLeftContour(node, 0, leftContour)
    
    depth = 1
    expectedXPlusNodeSize = 2 # Because of this.x + nodeSize (1 + 1) 
    self.assertTrue(leftContour[depth] == expectedXPlusNodeSize, "node " + name + " " + 
                    str(depth) + " depth left contour is wrong ")
    
    depth = 2
    expectedXPlusMod = 2 # Because of parent.x - this.x (2 - 0)
    self.assertTrue(leftContour[depth] == expectedXPlusMod, "node " + name + " " + 
                    str(depth) + " depth left contour is wrong ")
    
    
    name = "4"
    node = nodeList[int(name)]
    
    leftSibling = reingold.getLeftSibling(node, nodeList)
    rightContour = {}
    reingold.getRightContour(leftSibling, 0, rightContour)
    
    depth = 1
    self.assertTrue(rightContour[depth] == 2,  "node " + name + " " + 
                    str(depth) + " depth right contour is wrong ")
    
    depth = 2
    self.assertTrue(rightContour[depth] == 2, "node " + name + " " + 
                    str(depth) + " depth right contour is wrong ")
    
    leftContour = {}
    reingold.getLeftContour(node, 0, leftContour)
    
    depth = 1
    print("leftContour[depth] " + str(leftContour[depth]))
    expectedXPlusNodeSize = 2 # Because of this.x + nodeSize (1 + 1) 
    self.assertTrue(leftContour[depth] == 3, "node " + name + " " + 
                    str(depth) + " depth left contour is wrong ")
    
    depth = 2
    self.assertTrue(leftContour[depth] == 2.5, "node " + name + " " + 
                    str(depth) + " depth left contour is wrong ")
    
#     name = "4"  # Main node
#     node = nodeList[int(name)]
#     self.assertTrue(reingold.checkForConflicts(node, nodeList, True), 
#                     name + " is not being checked for conflict")
    
    
    
    
  
#   def testFixConflicts(self):
#     Utils.LAST_ASSIGNED_ID = 1
#     nodeList = Utils.convertToNodes(Utils.getJson("start.json"))
#     
#     reingold = ReingoldTilford()
#     coords, checkedForConflictIds = reingold.setInitialX(nodeList[1], nodeList, True)
#     
#     name = "3"
#     node = nodeList[int(name)]
#     self.assertTrue(node["x"] == 3, 
#                     name + " x is not set properly")
#     
#     node = nodeList[int(name)]
#     self.assertTrue(node["mod"] == 3, 
#                     name + " mod is not set properly")
#      
#     name = "4"
#     node = nodeList[int(name)]
#     self.assertTrue(node["x"] == 4, 
#                     name + " mod is not set properly")
#     
#     node = nodeList[int(name)]
#     self.assertTrue(node["mod"] == 2.5, 
#                     name + " mod is not set properly")
    # Expected result?
    # Node 3 and 4 will be checked
    # Application of modification is from top to bottom
    
    
    
  def verifyNodeName(self, node, name):
    return node["name"] == name
  
  def verifyNodeX(self, node, x):
    return node["x"] == x
  
  def verifyMod(self, node, mod):
    return node["mod"] == mod
  
  
    
if __name__ == '__main__':
  unittest.main()