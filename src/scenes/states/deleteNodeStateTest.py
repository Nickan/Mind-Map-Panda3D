import unittest

class DeleteNodeState(unittest.TestCase):
  
  def __init__(self, methodName='runTest'):
    unittest.TestCase.__init__(self, methodName=methodName)
    
  
  def testDeleteNodeCancelling(self):
    filePath = Utils.getAssetPath("test/setRelativeXToParent.json")
    nodeList = SaveManager.loadNodeDataListKeyConvertedToInt(filePath)
  
    
    
if __name__ == '__main__':
  unittest.main()
  
  