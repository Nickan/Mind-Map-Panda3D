from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task

from scenes.map import Map
 
class Epiphany(ShowBase):
 
  def __init__(self):
    ShowBase.__init__(self)
    # self.scene = self.loader.loadModel("../models/environment")
    # self.scene.reparentTo(self.render)
    # self.scene.setScale(0.2, 0.2, 0.2)
    # self.scene.setPos(-8, 42, 0)

    # self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

    map = Map(self)


  def spinCameraTask(self, task):
    angleDegrees = task.time * 6.0
    angleRadians = angleDegrees * (pi / 180.0)
    self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
    self.camera.setHpr(angleDegrees, 0, 0)
    return Task.cont

  
 
app = Epiphany()
app.run()