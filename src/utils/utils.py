

class Utils():
  LAST_ASSIGNED_ID = 0

  def __init__(self):
    print("Init Utils")

  
  @staticmethod
  def convertToNodes(jsonData):
    nodeList = []

    allNodeJsons = [jsonData]
    
    while len(allNodeJsons) > 0:
      nodeJsonsInCurrentDepth = allNodeJsons
      allNodeJsons = []

      nodes = []
      while len(nodeJsonsInCurrentDepth) > 0:
        nodeJson = nodeJsonsInCurrentDepth[0]
        nodeJsonsInCurrentDepth.remove(nodeJson)

        id = Utils.getIdOrAssignUnique(nodeJson)
        nodes.append(Utils.getNode(nodeJson))

        nodeChildren = nodeJson.get('children')
        if nodeChildren is not None:
          allNodeJsons.extend(nodeChildren)
          for child in nodeChildren:
            child['parentId'] = id
            
      nodeList.append(nodes)

    return nodeList

  @staticmethod
  def getNode(nodeJson):
    name = nodeJson.get('name')
    nodeId = nodeJson.get('id')
    parentId = nodeJson.get('parentId')
    node = { "name": name, "id": nodeId, "parentId": parentId }
    return node


  @staticmethod
  def showNodes(nodeList):
    for depth, nodes in enumerate(nodeList):
      print("depth: " + str(depth))
      for breadth, node in enumerate(nodes):
        print("breadth " + str(breadth) + " " + node.get('name') 
        + " id " + str(node.get('id')) + " parentId " + str(node.get('parentId')))


  @staticmethod
  def getIdOrAssignUnique(nodeJson):
    id = nodeJson.get('id')
    if id is None:
      id = Utils.LAST_ASSIGNED_ID
      nodeJson['id'] = id
      Utils.LAST_ASSIGNED_ID += 1
    return id

  