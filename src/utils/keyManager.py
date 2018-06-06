

class KeyManager():
  ON_KEY_DOWN_FN = None
  
  @staticmethod
  def setupKeyListener(showBase, onKeyDownFn):
    KeyManager.setupControls(showBase)
    KeyManager.ON_KEY_DOWN_FN = onKeyDownFn
    
  @staticmethod
  def setupControls(showBase):
    showBase.buttonThrowers[0].node().setKeystrokeEvent('keystroke')
    showBase.accept('keystroke', KeyManager.onKeyDown)
    
    
  @staticmethod
  def onKeyDown(keyname):
    KeyManager.ON_KEY_DOWN_FN(keyname)
    
  @staticmethod
  def getModifiedKeyFromKeyInput(text, keyname, onEnterDown):
    if keyname == "\b": # Backspace
      text = text[:-1]
    else:
        
      if keyname == "\r": # Enter
        onEnterDown(text)
        
      if keyname != "\t": # As long as keyname is not a tab
        text += keyname
    return text
    
    
  