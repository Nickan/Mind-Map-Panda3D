# from scenes.cameramanager import CameraManager
# from scenes.mapComponents.background import Background

# from direct.actor.Actor import Actor

# from panda3d.core import CollisionTraverser, CollisionNode, CollisionSphere
# from panda3d.core import CollisionHandlerQueue, CollisionRay
# from panda3d.core import LPoint3, LVector3, BitMask32
# from panda3d.core import NodePath
# from panda3d.core import LVecBase3f
# from panda3d.core import DecalEffect
# from panda3d.core import CardMaker
# from direct.task.Task import Task

from scenes.states.state import State

from scenes.states.staticMapState import StaticMapState


from scenes.cameramanager import CameraManager
from scenes.mapComponents.node import Node


# from panda3d.core import TextNode

class Map():

  def __init__(self, showBase):
    self.showBase = showBase

    self.initCamera()
    self.initNode()

    self.state = StaticMapState()
    self.state.enter(self)

    # self.initOthers()

  def initCamera(self):
    self.cameraManager = CameraManager(self.showBase)

  def initNode(self):
    self.node = Node(self.showBase)












    
  # def initOthers(self):
  #   # self.addPandaActor()
  #   # self.setBg()
  #   self.initCamera()
    
  #   self.addTestModel()
  #   self.addTextOnTheModel()

  #   self.showBase.accept('w', self.forward)
  #   self.showBase.accept('s', self.backard)
  #   self.showBase.accept('a', self.left)
  #   self.showBase.accept('d', self.right)

  #   self.showBase.accept('arrow_up', self.up)
  #   self.showBase.accept('arrow_down', self.down)


  #   self.setupDragObject()

  #   self.addAnimation()

  

  # def setupDragObject(self):
  #   # cNodeActor = self.testActor.attachNewNode(CollisionNode('cNodeActor'))
  #   # cNodeActor.node().addSolid(CollisionSphere(0, 0, 1.5, 1.5))
  #   # cNodeActor.show()

  #   self.picker = CollisionTraverser()
  #   self.picker.showCollisions(self.showBase.render)
  #   self.pq = CollisionHandlerQueue()


  #   self.pickerNode = CollisionNode('mouseRay')
  #   self.pickerNP = camera.attachNewNode(self.pickerNode)
  #   self.pickerNode.setFromCollideMask(BitMask32.bit(1))

  #   self.testActor.setCollideMask(BitMask32.bit(1))


  #   self.pickerRay = CollisionRay()
  #   self.pickerNode.addSolid(self.pickerRay)
  #   self.picker.addCollider(self.pickerNP, self.pq)

  #   # self.showBase.accept("mouse1",self.mouseClick)

  #   self.dragging = False

  #   self.showBase.mouseTask = taskMgr.add(self.mouseTask, 'mouseTask')
  #   self.showBase.accept("mouse1", self.mouseDown)  # left-click grabs a piece
  #   self.showBase.accept("mouse1-up", self.mouseUp)  # releasing places it


    

  # def mouseClick(self):
  #   print('mouse click')

  #   if self.showBase.mouseWatcherNode.hasMouse():
  #     mpos = self.showBase.mouseWatcherNode.getMouse()
  #     print(mpos)

  #     self.pickerRay.setFromLens(self.showBase.camNode,mpos.getX(),mpos.getY())
  #     self.picker.traverse(self.showBase.render)

  #     # if we have hit something sort the hits so that the closest is first and highlight the node
  #     if self.pq.getNumEntries() > 0:
  #       self.pq.sortEntries()
  #       pickedObj = self.pq.getEntry(0).getIntoNodePath()
  #       print('click on ' + pickedObj.getName())


  # def mouseTask(self, task):
  #   if self.showBase.mouseWatcherNode.hasMouse():
  #     mpos = self.showBase.mouseWatcherNode.getMouse()

  #     self.pickerRay.setFromLens(self.showBase.camNode, mpos.getX(), mpos.getY())
  #     self.picker.traverse(self.testActor)

  #     if self.dragging is True:
  #       render = self.showBase.render
  #       camera = self.showBase.camera

  #       nearPoint = render.getRelativePoint(
  #                   camera, self.pickerRay.getOrigin())
  #       # Same thing with the direction of the ray
  #       nearVec = render.getRelativeVector(
  #                 camera, self.pickerRay.getDirection())


  #       if self.pq.getNumEntries() > 0:
  #         self.pq.sortEntries()
  #         pickedObj = self.pq.getEntry(0).getIntoNodePath()
  #         print('click on ' + pickedObj.getName())
  #         pickedObj.setPos(self.pointAtZ(0, nearPoint, nearVec))

  #       # self.testActor.setPos(self.pointAtZ(0, nearPoint, nearVec))
  #       # self.pieces[self.dragging].obj.setPos(
  #       #     PointAtZ(.5, nearPoint, nearVec))

  #   return Task.cont

  # def pointAtZ(self, z, point, vec):
  #   return point + vec * ((z - point.getZ()) / vec.getZ())


  # def mouseDown(self):
  #   self.dragging = True

  # def mouseUp(self):
  #   self.dragging = False





  # def addTextOnTheModel(self):

  #   self.textRotation = LVecBase3f(0, 90, 180)

  #   # self.text
  #   # self.text3d
  #   self.text = TextNode("Node 1")
  #   self.text.setText("Nickan")
  #   self.text.setTextColor(0, 0, 1, 1)
  #   self.text.setAlign(TextNode.A_center)
    
    
  #   self.text3d = NodePath(self.text)
  #   self.text3d.reparentTo(self.testActor)
  #   self.text3d.setPos(0, 0, -1.1)
  #   self.text3d.setHpr(self.textRotation)
  #   self.text3d.setTwoSided(True)

  # def up(self):
  #   self.textRotation.addY(5)
  #   self.testActor.setHpr(self.textRotation)

  # def down(self):
  #   self.textRotation.addY(-5)
  #   self.testActor.setHpr(self.textRotation)




  # def addAnimation(self):
  #   self.anim = Actor("../models/animation",
  #                               {"swing": "../models/animation-swing"})
  #   self.anim.reparentTo(self.showBase.render)
  #   self.anim.loop("swing")




  # def setBg(self):
  #   self.bg = Background(self.showBase)

  # def addTestModel(self):
  #   self.testActor = loader.loadModel("../models/capsule") 
  #   scale = 1
  #   self.testActor.setScale(scale, scale, scale)
  #   self.testActor.reparentTo(self.showBase.render)

  #   self.camPos = self.testActor.getPos()
  #   # print('testActor ' + str(self.testActor.getPos()))

  # def forward(self):
  #   print("forward")
  #   self.camPos.z += 1

  #   self.testActor.setPos(self.camPos)
  #   self.showCameraPos()

  # def backard(self):
  #   print("backard")
  #   self.camPos.z += -1

  #   self.testActor.setPos(self.camPos)
  #   self.showCameraPos()

  # def left(self):
  #   print("left")
  #   self.camPos.x += 1

  #   self.testActor.setPos(self.camPos)
  #   self.showCameraPos()

  # def right(self):
  #   print("right")
  #   self.camPos.x += -1

  #   self.testActor.setPos(self.camPos)
  #   self.showCameraPos()

  # # def up(self):
  # #   print("up")
  # #   self.camPos.y += 1

  # #   self.testActor.setPos(self.camPos)
  # #   self.showCameraPos()

  # # def down(self):
  # #   print("down")
  # #   self.camPos.y += -1

  # #   self.testActor.setPos(self.camPos)
  # #   self.showCameraPos()

  # def showCameraPos(self):
  #   print("pos " + str(self.testActor.getPos()))
  #   print("hpr " + str(self.testActor.getHpr()))
  #   print("x " + str(self.testActor.getX()))
  #   print("y " + str(self.testActor.getY()))
  #   print("z " + str(self.testActor.getZ()))


  
  