

from epiphany import Epiphany
from scenes.states.cleanState import CleanState

from test.debuggingState import DebuggingState

class Main():
 
  def __init__(self):
    epiphany = Epiphany()
    state = CleanState(epiphany, {}, {})
    state.enter()
    epiphany.run()
    
main = Main()
    









