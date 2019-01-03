
class NodeData():
  ID = "id"
  PARENT_ID = "parentId"
  CHILDREN_IDS = "childrenIds"
  DEPTH = "depth"

  @staticmethod
  def hasChildren(data):
    return data.get(NodeData.CHILDREN_IDS)