import json
import os.path as path

import copy

class Utils():
  LAST_ASSIGNED_ID = 0
  
  STARTJSON = None
  
  # Node
  NODE_SCALE = (6, 6, 1)
  
  DEPTH_DIST = 20
  BREADTH_DIST = 30

  def __init__(self):
    print("Init Utils")
  
  @staticmethod
  def convertToNodes(jsonData): # Needed to be able to assign parentId(Proof?)
#     Utils.test(jsonData)
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
  def getUniqueId():
    Utils.LAST_ASSIGNED_ID += 1
    return Utils.LAST_ASSIGNED_ID
  


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
  def getJson(name):
    jsonPath = path.abspath(path.join(__file__ , "../../../assets/" + name))
    return json.load(open(jsonPath))
  
  
  @staticmethod
  def getChildren(node, nodeList):
    childrenIds = node.get("childrenIds")
    if childrenIds is None:
      return None
    
    children = []
    for id in childrenIds:
      children.append(nodeList[int(id)])
    return children
  
  
  
  
  
  
  
  
  
  



  