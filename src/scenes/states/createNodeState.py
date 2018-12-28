from .state import State
from .stateManager import StateManager

from scenes.mapComponents.nodeManager import NodeManager

from utils.keyManager import KeyManager
from utils.saveManager import SaveManager
from utils.utils import Utils



class CreateNodeState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self):
    self.setupControls()
    map = self.map
    nodeManager = map.nodeManager
    data = map.getSavedSelectedNodeData()
    map.createNodeData(data.get(NodeManager.ID), "")
    map.drawData()
    KeyManager.setupKeyListener(self.map.showBase, self.onKeyDown)

    
  def onKeyDown(self, keyname):
    nm = self.map.nodeManager
    dataDrawing, dataId = nm.getLatestDrawingNode(nm.allDrawingData,
      nm.allStatusData)

    # self.tmpNodeDrawing = nodeManager.getNodeDrawing(self.tmpNewNodeData)
    text = dataDrawing.textNode.getText()
    text = KeyManager.getModifiedKeyFromKeyInput(text, keyname, dataId, 
      self.onEnterDown)
        
    textNode = dataDrawing.textNode
    textNode.setText(text)
    nm.setNodeDrawingHeight(dataDrawing)
    
  def onEnterDown(self, dataId, text):
    self.map.editNodeData(dataId, text)
    StateManager.switchToStaticMapState(self)
    
    
    
  def setupControls(self):
    map = self.map
    map.showBase.accept("mouse1", self.mouse1Down)
    
  def exit(self):
    KeyManager.clear()
    self.map.showBase.ignoreAll()
    
    
  """ enter() Helpers """
  def onEnterText(self, text):
    if text is not None:
      self.map.editNodeData(self.tmpNewNodeData, text)
      
    StateManager.switchToStaticMapState(self)
    
  def mouse1Down(self):
    if self.map.clickedOnMapBg():
      self.onClickedOutsideTextInput()
    
    
  def onClickedOutsideTextInput(self):
    
    self.map.deleteNodeData(self.tmpNewNodeData)
    self.tmpNewNodeData = None
    StateManager.switchToStaticMapState(self)
    
    
  def tmpCreatePotentialNewNode(self, nodeManager, data):
    id = nodeManager.getNodeDataId(nodeManager.data)
    self.tmpNewNodeData = nodeManager.createNodeData(id, "", False)
    return self.tmpNewNodeData






