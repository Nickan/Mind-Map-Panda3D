from direct.showbase.ShowBase import ShowBase

class Node():

  def __init__(self, loader, nodePath):
    # self.showBase = showBase
    self.addModel(loader, nodePath)
    self.addText()

  def addModel(self, loader, nodePath):
    self.model = loader.loadModel("../models/capsule") 
    scale = 1
    self.model.setScale(scale, scale, scale)
    self.model.reparentTo(nodePath)

  def addText(self):
    print("addText")

  