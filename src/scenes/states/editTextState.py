from .state import State
from .stateManager import StateManager

from utils.keyManager import KeyManager
from utils.utils import Utils


class EditTextState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self, selectedData):
    self.setupControls()
    map = self.map
    map.setStatusAsSelected(selectedData)
    map.drawData()
    map.startEditNode(selectedData, self.onKeyDown)
    
  def onKeyDown(self, keyname, extraParams):
    self.map.onKeyDown(keyname, self.onEnterDown, extraParams)
    
  def onEnterDown(self, dataId, text):
    self.map.editNodeData(dataId, text)
    StateManager.switchToStaticMapState(self)
    
  def setupControls(self):
    map = self.map
    map.showBase.accept("mouse1", self.mouse1Down)
    
  def exit(self):
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
    StateManager.switchToStaticMapState(self)
