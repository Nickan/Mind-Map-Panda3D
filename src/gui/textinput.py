from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *

from panda3d.core import NodePath
from panda3d.core import TextNode

from Tkinter import Tk
from tkSimpleDialog import askstring

class TextInput():
  
  def __init__(self, onEnterTextFn):
    self.onEnterTextFn = onEnterTextFn
    self.addText()
   
  def addText(self):
    Tk().withdraw()
    text = askstring("Enter text", "")
    self.onEnterTextFn(text)

     
    