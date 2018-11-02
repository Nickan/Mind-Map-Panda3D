from direct.showbase.ShowBase import Plane, ShowBase, Vec3, Point3
from gui.textinput import TextInput
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
from panda3d.core import LVecBase3f, BitMask32, LPoint3

import copy
import json
import os.path as path

class Utils():
  LAST_ASSIGNED_ID = 0
  
  STARTJSON = None
  
  # Node
  NODE_SCALE = LVecBase3f(7, 9, 1)
  
  VERT_DEPTH_DIST = 20
  VERT_BREADTH_DIST = 30
  HORT_DEPTH_DIST = 25
  HORT_BREADTH_DIST = 10
  VERTICAL_DEPTH = False
  
  CURRENT_NODE_DATA_LIST = None
  
  TEXT_INPUT = None
  
  @staticmethod
  def convertToNodes(jsonData): # Needed to be able to assign parentId(Proof?)
    # Utils.test(jsonData)
    nodeList = {}
 
    allNodeJsons = [copy.deepcopy(jsonData)]
     
    depth = 0
    while len(allNodeJsons) > 0:
      nodeJsonsInCurrentDepth = allNodeJsons
      allNodeJsons = []
 
       
      while len(nodeJsonsInCurrentDepth) > 0:
        currentJson = nodeJsonsInCurrentDepth[0]
        nodeJsonsInCurrentDepth.remove(currentJson)
 
        id = Utils.getIdOrAssignUnique(currentJson)
        node = Utils.getNode(currentJson, depth)
        nodeList[id] = node
 
        Utils.placeToParentsChildrenList(node, nodeList)
 
        nodeChildren = node.get('children')
        if nodeChildren is not None:
          allNodeJsons.extend(nodeChildren)
          for child in nodeChildren:
            child['parentId'] = id
 
      depth += 1
    return nodeList

  @staticmethod
  def placeToParentsChildrenList(node, nodeList):
    parentId = node.get("parentId")
    if parentId is not None:
      nodeJsonSiblings = nodeList[parentId].get("children")
      for index, sibling in enumerate(nodeJsonSiblings):
        if sibling.get("x") is None:
          nodeJsonSiblings.remove(sibling)
          nodeJsonSiblings.insert(index, node)
          nodeList[parentId]["children"] = nodeJsonSiblings
          break
        
  @staticmethod
  def getNode(nodeJson, y):
    name = nodeJson.get('name')
    nodeId = nodeJson.get('id')
    parentId = nodeJson.get('parentId')
    children = nodeJson.get('children')
    node = { 
      "name": name, "id": nodeId, "parentId": parentId, 
      "children": children, "x": -1.0, "y": y, "mod": 0
    }
    return node

  @staticmethod
  def showNodes(nodeList):
    for key in nodeList:
      node = nodeList[key]
      print(node.get('name') 
      + " id " + str(node.get('id')) + " parentId " + str(node.get('parentId'))
      + " x " + str(node.get("x")) + " y " + str(node.get("y")))

  @staticmethod
  def getIdOrAssignUnique(nodeJson):
    id = nodeJson.get('id')
    if id is None:
      Utils.LAST_ASSIGNED_ID += 1
      id = Utils.LAST_ASSIGNED_ID
      nodeJson['id'] = id
    return id
  
  
  @staticmethod
  def getUniqueId(nodeDataList, recheckLastId = False):
    Utils.LAST_ASSIGNED_ID = Utils.getLastAssignedId(nodeDataList, recheckLastId)
    Utils.LAST_ASSIGNED_ID += 1
    return Utils.LAST_ASSIGNED_ID
  
  @staticmethod
  def getLastAssignedId(nodeDataList, recheckLastId):
    highestIdAssigned = Utils.LAST_ASSIGNED_ID
    if Utils.CURRENT_NODE_DATA_LIST != nodeDataList or recheckLastId:
      Utils.CURRENT_NODE_DATA_LIST = nodeDataList
      for key in nodeDataList:
        if key >= highestIdAssigned:
          highestIdAssigned = key
      
    return highestIdAssigned

  @staticmethod
  def showNode(node):
    print("name " + str(node.get("name")) + " x " + 
    str(node.get("x")) + " y " + str(node.get("y")))

  @staticmethod
  def showDict(argDict):
    for key in argDict:
      print(str(key) + " " + str(argDict[key]))
      
  @staticmethod
  def dictLen(argDict):
    if argDict is None:
      return 0
    return len(argDict)
  
  
  @staticmethod
  def getJson(name):  # Deprecated
    jsonPath = path.abspath(path.join(__file__ , "../../../assets/" + name))
    return json.load(open(jsonPath))
  
  @staticmethod
  def getAssetPath(fileName):
    return path.abspath(path.join(__file__ , "../../../assets/" + fileName))
  
  
  @staticmethod
  def getChildren(node, nodeList):
    childrenIds = node.get("childrenIds")
    if childrenIds is None:
      return None
    
    children = []
    for id in childrenIds:
      children.append(nodeList[id])
    return children
  
  
  @staticmethod
  def createTextInput(pos, onEnterTextCb):
    Utils.TEXT_INPUT = TextInput(pos, onEnterTextCb)
    
  @staticmethod
  def closeTextInput():
    if Utils.TEXT_INPUT is not None:
      Utils.TEXT_INPUT.entry.destroy()
      Utils.TEXT_INPUT = None
    
  
  @staticmethod
  def getNodePosition(depth, breadth):
    if Utils.VERTICAL_DEPTH:
      x = breadth * Utils.VERT_BREADTH_DIST
      y = float(depth) * Utils.VERT_DEPTH_DIST
    else:
      y = breadth * Utils.HORT_BREADTH_DIST
      x = float(depth) * Utils.HORT_DEPTH_DIST
    z = 0 # Should be addressed later on
    
    return LVecBase3f(x, y, z)
  
  @staticmethod
  def getNodeDataPointt(nodeData):
    depth = nodeData.get("depth")
    breadth = nodeData.get("x")
    return Utils.getNodePosition(depth, breadth)


  # Have to find another way to organize functions
  @staticmethod
  def removeSelectedField(nodeId, nodeDataSettings):
    nodeSettings = nodeDataSettings.get(nodeId)
    if nodeSettings is not None:
      nodeDataSettings.pop(nodeId, None)
    return nodeDataSettings


  # Mouse helpers
  PLANE = Plane(Vec3(0, 0, 1), Point3(0, 0, 0))
  CT = CollisionTraverser()
  CHQ = CollisionHandlerQueue()
  CN = CollisionNode('mouseRay')

  NEW_CN = None
  CR = CollisionRay()

  @staticmethod
  def getMousePosition(showBase):
    Utils.initMouseFields(showBase)
    return Utils.getMouseCollisionToPlane(showBase, Utils.PLANE)

  @staticmethod
  def initMouseFields(showBase):
    if Utils.NEW_CN is None:
      Utils.NEW_CN = showBase.camera.attachNewNode(Utils.CN)
      Utils.CN.setFromCollideMask(BitMask32.bit(1))

      Utils.CN.addSolid(Utils.CR)
      Utils.CT.addCollider(Utils.NEW_CN, Utils.CHQ)
    

  @staticmethod
  def getMouseCollisionToPlane(showBase, plane):
    mouseWatcherNode = showBase.mouseWatcherNode
    if mouseWatcherNode.hasMouse():
      mpos = mouseWatcherNode.getMouse()

      pos3d = LPoint3()
      nearPoint = LPoint3()
      farPoint = LPoint3()
      showBase.camLens.extrude(mpos, nearPoint, farPoint)

      render = showBase.render
      camera = showBase.camera
      if plane.intersectsLine(pos3d,
        render.getRelativePoint(camera, nearPoint),
        render.getRelativePoint(camera, farPoint)):
        return pos3d
    return None

  
  
  
  
  
  
  
  
  
  



  