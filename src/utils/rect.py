
class Rect():

  def __init__(self, x, y, width, height):
    halfW = width / 2
    halfH = height / 2
    self.width = width
    self.height = height
    self.left = x - halfW
    self.right = x + halfW
    self.bottom = y - halfH
    self.top = y + halfH


  def collidesWith(self, rect):
    print(str(self.left) + " " + str(self.right) + " " +
      str(self.top) + " " + str(self.bottom))

    print(str(rect.left) + " " + str(rect.right) + " " +
      str(rect.top) + " " + str(rect.bottom))

    return ( 
      ( (rect.left > self.left) and (rect.left < self.right) or
      (rect.right > self.left) and (rect.right < self.right) ) 
      and
      ( (rect.top > self.bottom) and (rect.top < self.top) or
      (rect.bottom > self.bottom) and (rect.bottom < self.top) ) 
      )