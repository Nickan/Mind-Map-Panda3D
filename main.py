from direct.showbase.ShowBase import ShowBase
 
class Epiphany(ShowBase):
 
  def __init__(self):
    ShowBase.__init__(self)
 
app = Epiphany()
app.run()