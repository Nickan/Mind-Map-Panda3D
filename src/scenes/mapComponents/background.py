class Background():

  def __init__(self, showBase):
    self.showBase = showBase
    self.color = (0.5, 0.5, 0.5, 1)
    self.showBase.setBackgroundColor(self.color)