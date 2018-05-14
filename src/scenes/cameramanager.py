from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
from panda3d.core import LPoint3, LVector3, BitMask32


from direct.showbase.ShowBase import Plane, ShowBase, Vec3, Point3
from direct.task.Task import Task

class CameraManager():
  ZOOM_SPEED = 5

  def __init__(self, showBase):
    self.showBase = showBase
    self.showBase.disableMouse()
    self.setDefaultSettings()
    self.initMouseToWorldCoordConversion()
    self.initMouseRayCollision()
    self.savedCollisionPoint = Vec3(0, 0, 0)

  def initMouseRayCollision(self):
    z = 0
    self.plane = Plane(Vec3(0, 0, 1), Point3(0, 0, z))

  def setDefaultSettings(self):
    self.showBase.camera.setPos(0, 0, -100)
    self.camPos = self.showBase.camera.getPos()
    self.showBase.camera.setHpr(0, 90, 0)

    self.dragging = False  

  def zoomIn(self):
    camera = self.showBase.camera
    curPos = camera.getPos()
    curPos.z += CameraManager.ZOOM_SPEED

    camera.setPos(curPos)

  def zoomOut(self):
    camera = self.showBase.camera
    curPos = camera.getPos()
    curPos.z += -CameraManager.ZOOM_SPEED

    camera.setPos(curPos)


  def mouse1Down(self):
    self.savedCollisionPoint = self.getMouseCollisionToPlane(self.plane)
    # print("mouse1Down")



  def getMouseCollisionToPlane(self, plane):
    mouseWatcherNode = self.showBase.mouseWatcherNode
    if mouseWatcherNode.hasMouse():
      mpos = mouseWatcherNode.getMouse()

      pos3d = Point3()
      nearPoint = Point3()
      farPoint = Point3()
      self.showBase.camLens.extrude(mpos, nearPoint, farPoint)

      render = self.showBase.render
      camera = self.showBase.camera
      if plane.intersectsLine(pos3d,
          render.getRelativePoint(camera, nearPoint),
          render.getRelativePoint(camera, farPoint)):
        return pos3d
    return None

  def getDelta(self, point1, point2):
    delta = Vec3()
    if point1 is not None:
      if point1.almostEqual(point2) is False:
        delta = point2 - point1
    return delta

  def mouseMove(self, task):
    collisionPoint = self.getMouseCollisionToPlane(self.plane)
    delta = self.getDelta(collisionPoint, self.savedCollisionPoint)

    self.addToCameraPos(delta) # Collision point changes if camera position changes

    collisionPoint = self.getMouseCollisionToPlane(self.plane)
    self.savedCollisionPoint = collisionPoint
    return Task.cont


  def addToCameraPos(self, delta):
    camera = self.showBase.camera
    curPos = camera.getPos()
    camera.setPos(curPos + delta)


    


  def initMouseToWorldCoordConversion(self):
    self.picker = CollisionTraverser()
    self.pq = CollisionHandlerQueue()

    self.pickerNode = CollisionNode('mouseRay')
    self.pickerNP = self.showBase.camera.attachNewNode(self.pickerNode)

    self.pickerNode.setFromCollideMask(BitMask32.bit(1))
    self.pickerRay = CollisionRay()

    self.pickerNode.addSolid(self.pickerRay)

    self.picker.addCollider(self.pickerNP, self.pq)


  def getCoordinates(self):
    mouseWatcherNode = self.showBase.mouseWatcherNode
    mpos = mouseWatcherNode.getMouse()

    self.pickerRay.setFromLens(self.showBase.camNode, mpos.getX(), mpos.getY())

    render = self.showBase.render
    camera = self.showBase.camera
    nearPoint = render.getRelativePoint(camera, self.pickerRay.getOrigin())

    return mpos, nearPoint


  def showValues(self):
    print("camera pos " + str(self.showBase.camera.getPos()))
    print("camera hpr " + str(self.showBase.camera.getHpr()))
    print("camera x " + str(self.showBase.camera.getX()))
    print("camera y " + str(self.showBase.camera.getY()))
    print("camera z " + str(self.showBase.camera.getZ()))