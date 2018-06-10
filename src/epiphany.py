from direct.showbase.ShowBase import ShowBase

from panda3d.core import DynamicTextFont
from panda3d.core import Filename
from panda3d.core import WindowProperties

from scenes.map import Map

from scenes.states.state import State
from scenes.states.cleanState import CleanState

import json
import os.path as path

#  C:\dev\visualTool\Panda3D\Epiphany\assets\fonts\ubuntu.regular.ttf
class Epiphany(ShowBase):
 
  def __init__(self):
    ShowBase.__init__(self)
    self.map = None
    self.loadTtf()
    self.initMap()
    
  def loadTtf(self):
    file = "../../assets/fonts/ubuntu.regular.ttf"
    fontPath =  path.abspath(path.join(__file__ ,file))
#     Map.FONT_UBUNTU = self.loader.loadFont(fontPath)
    Map.FONT_UBUNTU = self.loader.loadFont("../ubuntu.regular.ttf")
    Map.FONT_UBUNTU.setPixelsPerUnit(120)
    Map.FONT_UBUNTU.setScaleFactor(3)
    Map.FONT_UBUNTU.setNativeAntialias(0)
    self.setScreenSize()

  def initMap(self):
    self.map = Map(self)
    
  def setScreenSize(self):
    w, h = 1366, 640 
    props = WindowProperties()
#     props.setFullscreen(1)
    props.setSize(w, h)
#     base.openMainWindow()
    base.win.requestProperties(props)
  
  
    
    
    
    
    
    
    
    
    
    
    
    
    
    