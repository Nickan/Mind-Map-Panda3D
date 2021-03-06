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
    data = map.getActivatedNodeData()
    map.removeFoldedState(data)
    map.createNodeData(data.get(NodeManager.ID), "")
    map.drawData()

    lastCreatedData = map.getLatestCreatedData()
    map.startEditNode(lastCreatedData, self.onKeyDown)

    
  def onKeyDown(self, keyname, extraParams):
    self.map.onKeyDown(keyname, self.onEnterDown, extraParams)
    
  def onEnterDown(self, dataId, text):
    map = self.map
    map.editNodeData(dataId, text)
    map.setStatusAsSelectedById(dataId)
    map.drawData()
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
    map.removeLatestCreateDataStateByData(lastCreatedData)
    map.drawData()
    StateManager.switchToStaticMapState(self)






