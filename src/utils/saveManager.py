

import json
import os.path
from builtins import staticmethod

from scenes.mapComponents.dataContainer import DataContainer

from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

class SaveManager():
  
  
  @staticmethod
  def saveDataContainer(dataContainer):
    nodeDataList = dataContainer.unfilteredData
    if not nodeDataList:
      nodeDataList = dataContainer.nodeDataList

    SaveManager.clearNodeDataList(nodeDataList)
      
    
    Tk().withdraw()
    fileName = asksaveasfilename()
    
    if len(fileName) < 1:
      return

    SaveManager.saveSettingJson(fileName)
    with open(fileName, 'w') as fp:
      json.dump(nodeDataList, fp)
      
  @staticmethod
  def loadDataContainer(onLoadFilePathCb):
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    fileName = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    
    if len(fileName) < 1:
      return

    allStatusData = SaveManager.loadSettingJson(fileName)
    allData = SaveManager.convertKeyTypeToInt(fileName)
    onLoadFilePathCb(allData, allStatusData)
    
  @staticmethod
  def convertKeyTypeToInt(fileName):
    nodeList = json.load(open(fileName))
    return SaveManager.setKeyAsInt(nodeList)
    
  @staticmethod
  def setKeyAsInt(nodeList):
    for key in nodeList:
      nodeData = nodeList[key]
      del nodeList[key]
      nodeList[int(key)] = nodeData
    return nodeList
      
      
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
  settingJsonMap = {}

  # For loading the settings
  @staticmethod
  def saveSettingJson(filename):
    SaveManager.mainJson = filename

    modFilename = filename.replace(".json", "")
    SaveManager.settingJson = modFilename + "-setting.json"
    SaveManager.createSettingJsonData(SaveManager.settingJson,
      SaveManager.settingJsonMap)
    return SaveManager.settingJsonMap

  
  @staticmethod
  def loadSettingJson(fileName):
    SaveManager.mainJson = fileName

    modFilename = fileName.replace(".json", "")
    SaveManager.settingJson = modFilename + "-setting.json"
    if os.path.exists(SaveManager.settingJson):
      SaveManager.loadSettingJsonData(SaveManager.settingJson)
    else:
      SaveManager.createSettingJsonData(SaveManager.settingJson,
        SaveManager.settingJsonMap)
    return SaveManager.settingJsonMap
  

  @staticmethod
  def createSettingJsonData(filePath, map):
    with open(filePath, 'w') as fp:
      json.dump(map, fp)

  @staticmethod
  def loadSettingJsonData(filePath):
    SaveManager.settingJsonMap = SaveManager.convertKeyTypeToInt(filePath)
