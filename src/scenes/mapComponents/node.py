from direct.showbase.ShowBase import ShowBase

class Node():

  def __init__(self, showBase):
    # self.showBase = showBase
    self.addModel(showBase)

  def addModel(self, showBase):
    self.model = showBase.loader.loadModel("../models/capsule") 
    scale = 1
    self.model.setScale(scale, scale, scale)
    self.model.reparentTo(showBase.render)