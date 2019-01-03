import json
import os.path
import copy

from builtins import staticmethod
from scenes.mapComponents.dataContainer import DataContainer
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

class SaveManager():
  CAM = "-cam.json"
  
  @staticmethod
  def saveData(allData, allStatusData, camDict):
    Tk().withdraw()
    fileName = asksaveasfilename()
    if len(fileName) < 1:
      return

    if '.json' not in fileName:
      fileName += '.json'

    SaveManager.saveSettingJson(fileName, allStatusData)
    SaveManager.saveToJson(fileName, camDict, SaveManager.CAM)
    with open(fileName, 'w') as fp:
      json.dump(allData, fp)
      
  @staticmethod
  def loadDataContainer(onLoadFilePathCb):
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    fileName = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    
    if len(fileName) < 1:
      return

    allStatusData = SaveManager.loadSettingJson(fileName)
    allData = SaveManager.loadAndConvertToDict(fileName)
    camDict = SaveManager.loadFromJson(fileName, SaveManager.CAM, False)
    onLoadFilePathCb(allData, allStatusData, camDict)
    
  @staticmethod
  def loadAndConvertToDict(fileName):
    jsonObj = json.load(open(fileName))
    return SaveManager.setKeyAsInt(jsonObj)
    
  @staticmethod
  def setKeyAsInt(json):
    newData = {}

    for key in json:
      nodeData = json[key]
      newData[int(key)] = nodeData
    return newData
      
      
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
  def saveSettingJson(filename, allStatusData):
    SaveManager.mainJson = filename

    modFilename = filename.replace(".json", "")
    SaveManager.settingJson = modFilename + "-setting.json"
    SaveManager.createFile(SaveManager.settingJson,
      allStatusData)

  @staticmethod
  def saveToJson(filename, dataDict, postFix):
    modFilename = filename.replace(".json", "")
    nFileName = modFilename + postFix
    SaveManager.createFile(nFileName, dataDict)

  @staticmethod
  def loadFromJson(fileName, postFix, convertKeyToInt = True):
    modFilename = fileName.replace(".json", "")
    nFileName = modFilename + postFix
    if os.path.exists(nFileName):
      if convertKeyToInt:
        return SaveManager.loadAndConvertToDict(nFileName)
      return json.load(open(nFileName))
    else:
      SaveManager.createFile(nFileName, {})
  
  @staticmethod
  def loadSettingJson(fileName):
    SaveManager.mainJson = fileName

    modFilename = fileName.replace(".json", "")
    SaveManager.settingJson = modFilename + "-setting.json"
    if os.path.exists(SaveManager.settingJson):
      SaveManager.loadSettingJsonData(SaveManager.settingJson)
    else:
      SaveManager.createFile(SaveManager.settingJson,
        SaveManager.settingJsonMap)
    return SaveManager.settingJsonMap
  

  @staticmethod
  def createFile(filePath, dict):
    with open(filePath, 'w') as fp:
      json.dump(dict, fp)

  @staticmethod
  def loadSettingJsonData(filePath):
    SaveManager.settingJsonMap = SaveManager.loadAndConvertToDict(filePath)
