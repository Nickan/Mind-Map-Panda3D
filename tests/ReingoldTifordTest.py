import unittest

import sys
from __builtin__ import int
sys.path.append('../src')

from utils.reingoldTilford import ReingoldTilford
from utils.utils import Utils

class ReingoldTilfordTest(unittest.TestCase):
  
  def __init__(self, methodName='runTest'):
    unittest.TestCase.__init__(self, methodName=methodName)
  
  def testLocalXRelativeToParentNode(self):
    nodeList = Utils.getJson("setRelativeXToParent.json")
    
    reingold = ReingoldTilford()
    coords, checkedForConflictIds = reingold.setInitialX(nodeList["1"], nodeList)
      
    name = "1"  # Main node
    node = coords[name]
    self.assertTrue(self.verifyNodeName(node, name),  name + " name is wrong")
    self.assertTrue(self.verifyNodeX(node, 2), name + " x is wrong")
      
    # Main node children
    name = "2"
    node = coords[name]
    self.assertTrue(self.verifyNodeName(node, name),  name + " name is wrong")
    self.assertTrue(self.verifyNodeX(node, 1), name + " x is wrong")
      
    name = "3"
    node = coords[name]
    self.assertTrue(self.verifyNodeName(node, name),  name + " name is wrong")
    self.assertTrue(self.verifyNodeX(node, 2), name + " x is wrong")
    self.assertTrue(self.verifyMod(node, 2), name + " mod is wrong")
      
    name = "4"
    node = coords[name]
    self.assertTrue(self.verifyNodeName(node, name),  name + " name is wrong")
    self.assertTrue(self.verifyNodeX(node, 3), name + " x is wrong")
    self.assertTrue(self.verifyMod(node, 2.5), name + " mod is wrong")
    # Main node children
      
    # Node 2 children
    name = "5"
    node = coords[name]
    self.assertTrue(self.verifyNodeName(node, name),  name + " name is wrong")
    self.assertTrue(self.verifyNodeX(node, 0), name + " x is wrong")
      
    name = "6"
    node = coords[name]
    self.assertTrue(self.verifyNodeName(node, name),  name + " name is wrong")
    self.assertTrue(self.verifyNodeX(node, 1), name + " x is wrong")
      
    name = "7"
    node = coords[name]
    self.assertTrue(self.verifyNodeName(node, name),  name + " name is wrong")
    self.assertTrue(self.verifyNodeX(node, 2), name + " x is wrong")
    # Node 2 children
      
    # Node 3 child
    name = "8"
    node = coords[name]
    self.assertTrue(self.verifyNodeName(node, name),  name + " name is wrong")
    self.assertTrue(self.verifyNodeX(node, 0), name + " x is wrong")
      
      
    # Node 4 childre
    name = "9"
    node = coords[name]
    self.assertTrue(self.verifyNodeName(node, name),  name + " name is wrong")
    self.assertTrue(self.verifyNodeX(node, 0), name + " x is wrong")
      
    name = "10"
    node = coords[name]
    self.assertTrue(self.verifyNodeName(node, name),  name + " name is wrong")
    self.assertTrue(self.verifyNodeX(node, 1), name + " x is wrong")
  
  def testNodesToCheckForConflictingX(self):
    nodeList = Utils.getJson("setRelativeXToParent.json")

    reingold = ReingoldTilford()
     
    name = "3"
    node = nodeList[name]
    self.assertTrue(reingold.checkForConflicts(node, nodeList, True), 
                    name + " is not being checked for conflict")
      
    name = "4"  # Main node
    node = nodeList[name]
    self.assertTrue(reingold.checkForConflicts(node, nodeList, True), 
                    name + " is not being checked for conflict")
     
  
  def testContourList(self):
    nodeList = Utils.getJson("setRelativeXToParent.json")
      
    reingold = ReingoldTilford()
    coords, checkedForConflictIds = reingold.setInitialX(nodeList["1"], nodeList)
     
    self.checkContourNode3(reingold, coords)
    self.checkContourNode4(reingold, coords)
     
  def checkContourNode3(self, reingold, coords):
    # Node 2 (Left node)
    # Right contour
    # Depth 2 == 1(Node 3)
    # Depth 3 == 2(Node 7)
    
    # Node 3 (Current Node)
    # Left contour
    # Depth 2 == 2(Node 4)
    # Depth 3 == 2(Node 8)
    
    name = "3"
    node = coords[name]
      
    leftSibling = reingold.getLeftSibling(node, coords)
    rightContour = {}
    reingold.getRightContour(leftSibling, coords, 0, rightContour)
      
    depth = "2"
    self.assertTrue(rightContour.get(depth) == 1,  "node " + name + " " + 
                    str(depth) + " depth right contour is wrong ")
      
    depth = "3"
    self.assertTrue(rightContour[depth] == 2, "node " + name + " " + 
                    str(depth) + " depth right contour is wrong ")
      
    leftContour = {}
    reingold.getLeftContour(node, coords, 0, leftContour)
      
    depth = "2"
    expectedXPlusNodeSize = 2 # Because of this.x + nodeSize (1 + 1) 
    self.assertTrue(leftContour[depth] == expectedXPlusNodeSize, "node " + name + " " + 
                    str(depth) + " depth left contour is wrong ")
      
    depth = "3"
    expectedXPlusMod = 2 # Because of parent.x - this.x (2 - 0)
    self.assertTrue(leftContour[depth] == expectedXPlusMod, "node " + name + " " + 
                    str(depth) + " depth left contour is wrong ")
     
  def checkContourNode4(self, reingold, coords):
    # Node 3 (Left node)
    # Right contour
    # Depth 2 == 2(Node 3)
    # Depth 3 == 2(Node 8) (0 + Mod(2))
    
    # Node 4 (Current Node)
    # Left contour
    # Depth 2 == 3(Node 4)
    # Depth 3 == 2.5(Node 9)(0 + Mod(2.5))
    
    name = "4"
    node = coords[name]
      
    leftSibling = reingold.getLeftSibling(node, coords)
    rightContour = {}
    reingold.getRightContour(leftSibling, coords, 0, rightContour)
      
    depth = "2"
    self.assertTrue(rightContour[depth] == 2,  "node " + name + " " + 
                    str(depth) + " depth right contour is wrong ")
      
    depth = "3"
    self.assertTrue(rightContour[depth] == 2, "node " + name + " " + 
                    str(depth) + " depth right contour is wrong ")
      
    leftContour = {}
    reingold.getLeftContour(node, coords, 0, leftContour)
      
    depth = "2"
    expectedXPlusNodeSize = 2 # Because of this.x + nodeSize (1 + 1) 
    self.assertTrue(leftContour[depth] == 3, "node " + name + " " + 
                    str(depth) + " depth left contour is wrong ")
      
    depth = "3"
    self.assertTrue(leftContour[depth] == 2.5, "node " + name + " " + 
                    str(depth) + " depth left contour is wrong ")
    
  
  def testFixConflictingX(self):
    nodeList = Utils.getJson("setRelativeXToParent.json")
      
    reingold = ReingoldTilford()
    coords, checkedForConflictIds = reingold.setInitialX(nodeList["1"], nodeList)
    
    id = "3"
    node3 = coords[id]
    reingold.fixConflictingX(node3, coords)
    
    self.assertTrue(self.verifyNodeX(node3, 3), "Error")
    self.assertTrue(self.verifyMod(node3, 3), "Error")
    
    id = "4"
    node4 = coords[id]
    reingold.fixConflictingX(node4, coords)
    
    self.assertTrue(self.verifyNodeX(node4, 4.5), "Error")
    self.assertTrue(self.verifyMod(node4, 4), "Error")
  
    
  def verifyNodeName(self, node, name):
    return node["name"] == name
  
  def verifyNodeX(self, node, x):
    if node["x"] == x:
      return True
    
    print("Error: expected x: " + str(x) + " Actual result: " + str(node["x"]))
    return False
  
  def verifyMod(self, node, mod):
    if node["mod"] == mod:
      return True
  
    print("Error: expected mod: " + str(mod) + " Actual result: " + str(node["mod"]))
    return False
    
if __name__ == '__main__':
  unittest.main()
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  