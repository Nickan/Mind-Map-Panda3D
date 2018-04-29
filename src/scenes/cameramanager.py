from math import pi, sin, cos

from direct.task import Task

class CameraManager():
  

  def __init__(self, showBase):
    self.showBase = showBase
    self.showBase.disableMouse()
    self.setupControls()
    self.setDefaultSettings()
    self.showValues()
    # self.showBase.taskMgr.add(self.camTest, "camTest")

  def setDefaultSettings(self):
    self.showBase.camera.setPos(0, 0, -25)
    self.camPos = self.showBase.camera.getPos()
    self.showBase.camera.setHpr(0, 90, 180)

    # self.showBase.camera.lookAt(0, 0, 0)

  def setupControls(self):
    self.showBase.accept("wheel_up", self.zoomIn)
    self.showBase.accept("wheel_down", self.zoomOut)
    self.showBase.accept('a', self.left)
    self.showBase.accept('d', self.right)
    self.showBase.accept('arrow_up', self.up)
    self.showBase.accept('arrow_down', self.down)

  def left(self):
    print("left")
    self.camPos.x += -1

    self.showBase.camera.setPos(self.camPos)
    self.showValues()

  def right(self):
    print("right")
    self.camPos.x += 1

    self.showBase.camera.setPos(self.camPos)
    self.showValues()

  def up(self):
    print("up")
    self.camPos.y += 1

    self.showBase.camera.setPos(self.camPos)
    self.showValues()

  def down(self):
    print("down")
    self.camPos.y += -1

    self.showBase.camera.setPos(self.camPos)
    self.showValues()

  def zoomIn(self):
    self.camPos.z += 1

    self.showBase.camera.setPos(self.camPos)
    self.showValues()

  def zoomOut(self):
    self.camPos.z += -1

    self.showBase.camera.setPos(self.camPos)
    self.showValues()


  def showValues(self):
    print("camera pos " + str(self.showBase.camera.getPos()))
    print("camera hpr " + str(self.showBase.camera.getHpr()))
    print("camera x " + str(self.showBase.camera.getX()))
    print("camera y " + str(self.showBase.camera.getY()))
    print("camera z " + str(self.showBase.camera.getZ()))



  def spinCameraTask(self, task):
    angleDegrees = task.time * 6.0
    angleRadians = angleDegrees * (pi / 180.0)


    x = 20 * sin(angleRadians)
    y = -20.0 * cos(angleRadians)
    print("sin " + str(x))
    print("cos " + str(y))
    print("angleRadians " + str(angleRadians))
    self.showBase.camera.setPos(x, y, 3)
    self.showBase.camera.setHpr(angleDegrees, 0, 0)
    return Task.cont

  def camTest(self, task):
    angleDegrees = task.time * 6.0
    # angleRadians = angleDegrees * (pi / 180.0)
    self.showBase.camera.setHpr(0, angleDegrees, 0)
    self.showValues()

    return Task.cont