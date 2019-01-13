from .state import State
from .stateManager import StateManager

from scenes.mapComponents.nodeManager import NodeManager
from utils.keyManager import KeyManager
from utils.saveManager import SaveManager
from utils.utils import Utils

class CreateSibling(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self):
    map = self.map
    data = map.getActivatedNodeData()
    parentData = map.getParent(data)
    map.removeFoldedState(parentData)
    map.createNodeData(parentData.get(NodeManager.ID), "")
    map.drawData()

    self.setupControls()

  def setupControls(self):
    map = self.map
    map.showBase.accept("enter-up", self.onEnterUp)
    map.showBase.accept("mouse1", self.mouse1Down)

  def onEnterUp(self):
    map = self.map
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






