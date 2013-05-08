import sys
sys.path.append('C:\Python27\Lib\site-packages')
sys.path.append("C:\Python27\Lib")
from Key_Entry import *

class Key_Map(object):
    """description of class"""

    def __init__(self):
        self.key_entry0 = Key_Entry('E','11', 127, 1) #roll right
        self.key_entry1 = Key_Entry('Q','12', 127, 0)
        self.key_entry2 = Key_Entry('S','21', 127, 3) #pitch Down
        self.key_entry3 = Key_Entry('W','22', 127, 2)
        self.key_entry4 = Key_Entry('A','31', 127, 5) #yaw Left
        self.key_entry5 = Key_Entry('D','32', 127, 4)
        self.key_entry6 = Key_Entry('Up','41', 127, 7) #x Forward
        self.key_entry7 = Key_Entry('Down','42', 127, 6)
        self.key_entry8 = Key_Entry('Left','51', 127, 9) #y Left
        self.key_entry9 = Key_Entry('Right','52', 127, 8)
        self.key_entry10 = Key_Entry('Space','61', 127, 11) #z surface
        self.key_entry11 = Key_Entry('B','62', 127, 10)

        self.key_dict = {
                            0:self.key_entry0,
                            1:self.key_entry1,
                            2:self.key_entry2,
                            3:self.key_entry3,
                            4:self.key_entry4,
                            5:self.key_entry5,
                            6:self.key_entry6,
                            7:self.key_entry7,
                            8:self.key_entry8,
                            9:self.key_entry9,
                            10:self.key_entry10,
                            11:self.key_entry11
                            }
    
    def getIndex(self, key_entry = Key_Entry()):
        index = 0
        for k_e in self.key_dict.values():
            if k_e == key_entry:
                return index
            index = index + 1
        return -1
    
    def setKeyDict(self, key_Dict = dict()):
        self.key_dict = key_Dict
        
    def getAllDictValues(self):
        returnDict = dict()
        for i in range (0, 12):
            returnDict[i] = self.key_dict[i].getKeyValue()
        return returnDict
        
    def getKeyDict(self):
        return self.key_dict

    def getKeyEntry(self, Value = str()):
        for val in self.key_dict.values():
            if Value == val.getKeyValue():
                return val
        return Key_Entry("Empty", '00', -1, -1)

    def getKeyEntryI(self, index = int()):
        return self.key_dict[index]
    
    def setKILLAll(self, kill = bool()):
        for i in self.key_dict.values():
            i.setKill(kill)
            
    def setNewDictValues(self, new_dict = dict()):
        for i in range(0,12):
            if new_dict[i] != '-':
                self.key_dict[i].setKeyValue(new_dict[i])