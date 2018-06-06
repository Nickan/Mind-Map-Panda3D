

class KeyManager():
  ON_KEY_DOWN_FN = None
  
  BUTTON_DOWN = False
  KEY_DOWN = False
  
  @staticmethod
  def setupKeyListener(showBase, onKeyDownFn):
    KeyManager.setupControls(showBase)
    KeyManager.ON_KEY_DOWN_FN = onKeyDownFn
    
  @staticmethod
  def setupControls(showBase):
    showBase.buttonThrowers[0].node().setButtonDownEvent('buttonDown')
    showBase.buttonThrowers[0].node().setKeystrokeEvent('keystroke')
    showBase.accept('buttonDown', KeyManager.onButtonDown)
    showBase.accept('keystroke', KeyManager.onKeyDown)
    
  
  @staticmethod
  def onButtonDown(keyname):
    if keyname == "backspace" or keyname == "space" or keyname == "enter":
      KeyManager.ON_KEY_DOWN_FN(keyname)
    
  @staticmethod
  def onKeyDown(keyname):
    print(keyname)
    if KeyManager.is_ascii(keyname) and keyname != '\b':
      KeyManager.ON_KEY_DOWN_FN(keyname)
  
  @staticmethod  
  def is_ascii(text):
    try:
      text = text.encode('ascii')
    except UnicodeEncodeError:
      return False
    return True
  