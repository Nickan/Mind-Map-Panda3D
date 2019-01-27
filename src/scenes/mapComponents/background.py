class Background():

  def __init__(self, showBase):
    self.showBase = showBase
    self.color = (0.09, 0.13, 0.16, 1)
    self.showBase.setBackgroundColor(self.color)