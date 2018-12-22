

from epiphany import Epiphany

from scenes.states.cleanState import CleanState

from test.debuggingState import DebuggingState

class Main():
 
  def __init__(self):
    epiphany = Epiphany()
    epiphany.map.setState(CleanState(epiphany.map))
    epiphany.run()
    
main = Main()
    









