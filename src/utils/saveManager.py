

import json
import os.path
from __builtin__ import staticmethod

from Tkinter import Tk
from tkFileDialog import askopenfilename
from tkFileDialog import asksaveasfilename

class SaveManager():
  
  
  @staticmethod
  def saveNodeDataList(nodeDataList):
    SaveManager.clearNodeDataList(nodeDataList)
    
    Tk().withdraw()
    fileName = asksaveasfilename()
    
    if len(fileName) < 1:
      return

    SaveManager.setMainJsonAndSettingJson(fileName)
    with open(fileName, 'w') as fp:
      json.dump(nodeDataList, fp)
      
  @staticmethod
  def loadNodeDataList(onLoadFilePathCb):
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    fileName = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    
    if len(fileName) < 1:
      return

    SaveManager.setMainJsonAndSettingJson(fileName)
    nodeDataList = SaveManager.loadNodeDataListKeyConvertedToInt(fileName)
    onLoadFilePathCb(nodeDataList)
    
  @staticmethod
  def loadNodeDataListKeyConvertedToInt(fileName):
    nodeDataList = json.load(open(fileName))
    return SaveManager.setKeyAsInt(nodeDataList)
    
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


  mainJson = ""
  settingJson = "-setting.json"

  # For loading the settings
  @staticmethod
  def loadSettingJson():
    SaveManager.getNodeDataList()

  @staticmethod
  def setMainJsonAndSettingJson(filename):
    SaveManager.mainJson = filename

    modFilename = filename.replace(".json", "")
    SaveManager.settingJson = modFilename + "-setting.json"
    if os.path.exists(SaveManager.settingJson):
      print("Setting exists")
    else:
      print("Setting doesn't exists")

    print("SettingJson " + SaveManager.settingJson)
    print("FileName " + SaveManager.mainJson)

