

import json
from __builtin__ import staticmethod

from Tkinter import Tk
from tkFileDialog import askopenfilename
from tkFileDialog import asksaveasfilename

class SaveManager():
  
  @staticmethod
  def saveNodeDataList(nodeDataList):
    SaveManager.clearNodeDataList(nodeDataList)
    
    Tk().withdraw()
    filename = asksaveasfilename()
    
    if len(filename) < 1:
      return
    with open(filename, 'w') as fp:
      json.dump(nodeDataList, fp)
      
  @staticmethod
  def loadNodeDataList(onLoadFilePathCb):
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    print(filename)
    
    if len(filename) < 1:
      return
    nodeDataList = json.load(open(filename))
  
    nodeDataList = SaveManager.setKeyAsInt(nodeDataList)
    onLoadFilePathCb(nodeDataList)
    
  @staticmethod
  def setKeyAsInt(nodeDataList):
    for key in nodeDataList:
      nodeData = nodeDataList[key]
      del nodeDataList[key]
      nodeDataList[int(key)] = nodeData
    return nodeDataList
      
      
  @staticmethod
  def clearNodeDataList(nodeDataList):
    SaveManager.clearNodeData(nodeDataList[1], nodeDataList)
    
  @staticmethod
  def clearNodeData(nodeData, nodeDataList):
    childrenIds = nodeData.get("childrenIds")
    
    if childrenIds is not None:
      for childId in childrenIds:
        childNodeData = nodeDataList[childId]
        SaveManager.clearNodeData(childNodeData, nodeDataList)
        
    nodeData["x"] = 0
    nodeData["mod"] = 0
    
  
  @staticmethod
  def getNodeDataList(name):
    jsonPath = '../assets/' + name
    return json.load(open(jsonPath))