from direct.showbase.ShowBase import ShowBase

from scenes.map import Map
 
class Epiphany(ShowBase):
 
  def __init__(self):
    ShowBase.__init__(self)
    map = Map(self)
 
app = Epiphany()
app.run()