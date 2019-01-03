

class KeyManager():
  ON_KEY_DOWN_FN = None
  EXTRA_ARGS = None
  
  @staticmethod
  def setupKeyListener(showBase, onKeyDownFn, extraArgs = None):
    KeyManager.setupControls(showBase)
    KeyManager.ON_KEY_DOWN_FN = onKeyDownFn
    KeyManager.EXTRA_ARGS = extraArgs
    
  @staticmethod
  def setupControls(showBase):
    showBase.accept('keystroke', KeyManager.onKeyDown)
    showBase.buttonThrowers[0].node().setKeystrokeEvent('keystroke')
    
    
  @staticmethod
  def onKeyDown(keyname):
    KeyManager.ON_KEY_DOWN_FN(keyname, KeyManager.EXTRA_ARGS)
    
  @staticmethod
  def getModifiedKeyFromKeyInput(text, keyname, dataId, onEnterDown):
    if keyname == "\b": # Backspace
      text = text[:-1]
    else:
        
      if keyname == "\r": # Enter
        onEnterDown(dataId, text)
        
      if keyname != "\t": # As long as keyname is not a tab
        text += keyname
    return text
    
  @staticmethod
  def clear():
     KeyManager.ON_KEY_DOWN_FN = None
     KeyManager.EXTRA_ARGS = None
    
  