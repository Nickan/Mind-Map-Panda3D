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
    data = map.getActivatedNodeData()
    map.removeFoldedState(data)
    map.createNodeData(data.get(NodeManager.ID), "")
    map.drawData()
    KeyManager.setupKeyListener(self.map.showBase, self.onKeyDown)

    
  def onKeyDown(self, keyname):
    nm = self.map.nodeManager
    dataDrawing, dataId = nm.getLatestDrawingNode(nm.allDrawingData,
      nm.allStateData)

    text = dataDrawing.textNode.getText()
    text = KeyManager.getModifiedKeyFromKeyInput(text, keyname, dataId, 
      self.onEnterDown)
        
    textNode = dataDrawing.textNode
    textNode.setText(text)
    data = nm.allData.get(dataId)
    nm.setNodeDrawingHeight(data, dataDrawing)
    
  def onEnterDown(self, dataId, text):
    self.map.editNodeData(dataId, text)
    StateManager.switchToStaticMapState(self)
    
  
  def setupControls(self):
    map = self.map
    map.showBase.accept("mouse1", self.mouse1Down)
    
  def exit(self):
    KeyManager.clear()
    self.map.showBase.ignoreAll()
    
  def mouse1Down(self):
    if self.map.clickedOnMapBg():
      self.onClickedOutsideTextInput()
    
  def onClickedOutsideTextInput(self):
    map = self.map
    lastCreatedData = map.getLatestCreatedData()
    map.removeData(lastCreatedData)
    map.drawData()
    StateManager.switchToStaticMapState(self)






