
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
  STARTING_DATA = 'startingData'

  @staticmethod
  def hasChildren(data):
    return data.get(NodeData.CHILDREN_IDS)