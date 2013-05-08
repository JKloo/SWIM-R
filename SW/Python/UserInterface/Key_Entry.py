class Key_Entry(object):
    def __init__(self, Key = str(), Code= str(), Speed = int(), counterpart = int()):
        self._Key_Value = Key
        self._Code = Code
        self._Speed = Speed
        self._Counterpart = counterpart
        self._IsPressed = bool()
        self.KILL = False

    def setKeyValue(self, Key_Value = str()):
        self._Key_Value = Key_Value

    def setCode(self, Code=str()):
        self._Code = Code

    def setSpeed(self, Speed = int()):
        self._Speed = Speed

    def setIsPressed(self, IsPressed = bool()):
        self._IsPressed = IsPressed

    def getIsPressed(self):
        return self._IsPressed

    def getCode(self):
        return self._Code

    def getSpeed(self):
        return self._Speed

    def getKeyValue(self):
        return self._Key_Value
    
    def getCounterPart(self):
        return self._Counterpart
    
    def setCounterPart(self, Counterpart = int()):
        self._Counterpart = counterpart
        
    def setKill(self, Kill = bool()):
        self.KILL = Kill
        
    def getKill(self):
        return self.KILL