from direct.showbase.ShowBase import ShowBase

from panda3d.core import DynamicTextFont
from panda3d.core import Filename
from panda3d.core import WindowProperties
from panda3d.core import TextFont

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
    
  def loadTtf(self):
    file = "../../assets/fonts/ubuntu.regular.ttf"
    fontPath =  path.abspath(path.join(__file__ ,file))
#     Map.FONT_UBUNTU = self.loader.loadFont(fontPath)
    Map.FONT_UBUNTU = self.loader.loadFont("../ubuntu.regular.ttf")
    Map.FONT_UBUNTU.setPixelsPerUnit(60)
#     Map.FONT_UBUNTU.setScaleFactor(1)
#     Map.FONT_UBUNTU.setNativeAntialias(0)
#     Map.FONT_UBUNTU.setRenderMode(TextFont.RMSolid)
    Map.FONT_UBUNTU.setPageSize(256,256)
    self.setScreenSize()
    
  def setScreenSize(self):
    w, h = 1366, 750 
    props = WindowProperties()
#     props.setFullscreen(1)
    props.setSize(w, h)
#     base.openMainWindow()
    base.win.requestProperties(props)
  
  
    
    
    
    
    
    
    
    
    
    
    
    
    
    