from panda3d.core import LVecBase3f
from panda3d.core import Point2

class CoordManager():
  

  @staticmethod
  def convertWorldToScreenCoords2D(map, mainNode):
    cam = map.showBase.cam
    camLens = map.showBase.camLens
    p2d = CoordManager.compute2dPosition(cam, camLens, mainNode)
    return p2d
    
    
  @staticmethod
  def compute2dPosition(cam, camLens, nodePath, point = LVecBase3f(0, 0, 0)):
    """ Computes a 3-d point, relative to the indicated node, into a
    2-d point as seen by the camera.  The range of the returned value
    is based on the len's current film size and film offset, which is
    (-1 .. 1) by default. """
    
    # Convert the point into the camera's coordinate space
    p3d = cam.getRelativePoint(nodePath, point)

    # Ask the lens to project the 3-d point to 2-d.
    p2d = Point2()
    if camLens.project(p3d, p2d):
      # Got it!
      return p2d

    # If project() returns false, it means the point was behind the
    # lens.
    return None
  
  
  
  
  
  
  
  
  
  