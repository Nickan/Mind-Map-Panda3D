
import sys
sys.path.append('../../src')

import json
import copy

from scenes.states.state import State
from scenes.states.stateManager import StateManager

from utils.saveManager import SaveManager
from utils.utils import Utils

from utils.reingoldTilford import ReingoldTilford

class DebuggingState(State):
  
  def __init__(self, map):
    State.__init__(self)
    self.map = map
    
  def enter(self):
    map = self.map
    map.showBase.camera.setPos(150, 70, -280)
    
    fileName = "../assets/test/veryFarConflictBug.json"
    nodeList = SaveManager.loadNodeDataListKeyConvertedToInt(fileName)
    
    self.cloneNodeList1 = copy.deepcopy(nodeList)
    
    self.rein = ReingoldTilford(self.onNodePosAssigned)
    self.rein.getCoordinates(self.cloneNodeList1)
    
#     map.drawNodeDataList(cloneNodeList1)
    
    
    
  def onNodePosAssigned(self, nodeData, msg):
    nodeManager = self.map.nodeManager
    cloneNodeList = copy.deepcopy(self.cloneNodeList1)
    
    self.rein.calcFinalPos(nodeData, cloneNodeList, 0)
    self.map.drawNodeDataList(cloneNodeList)
    nodeManager.setNodeSelected(nodeData, cloneNodeList)
    
    self.map.showBase.graphicsEngine.renderFrame()
    
    print("id: " + str(nodeData['id']) + " msg " + msg)
    
  def exit(self):
    map = self.map
    
    
    
    
    
    
    
    
  