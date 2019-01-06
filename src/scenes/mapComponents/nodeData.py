
class NodeData():
  ID = 'id'
  NAME = 'name'
  PARENT_ID = 'parentId'
  CHILDREN_IDS = 'childrenIds'
  DEPTH = "depth"

  #Status field
  SELECTED = "selected"
  LATEST_CREATED_DATA = "latestCreatedData"
  FOLDED = 'folded'
  HIDE_ANCESTORS = 'hideAncestors'
  LATEST_HIDE_ANCESTORS = 'latestHideAncestors'

  @staticmethod
  def hasChildren(data):
    return data.get(NodeData.CHILDREN_IDS)


  @staticmethod
  def hasState(data, allStateData, stateName):
    dataId = data.get(NodeData.ID)
    return NodeData.hasStateById(dataId, allStateData, stateName)

  @staticmethod
  def hasStateById(dataId, allStateData, stateName):
    state = allStateData.get(dataId)
    return state is not None and state.get(stateName) is not None


  @staticmethod
  def hasField(data, fieldName):
    return data.get(fieldName) is not None

  

