import threading
from Key_Entry import *
import sys
sys.path.append('..')
from client_interface import *

class KeyDown_Custom(threading.Thread):
    def __init__(self, key_entry = Key_Entry(), client_interface = ClientInterface(), input_type = str()):
        threading.Thread.__init__(self)
        self.NEUTRAL = 127
        self.count = int()
        self.working = True
        self.key_entry_in = key_entry
        self.input_type = input_type
        
        self.Control_Dict = {
                                '1':client_interface.setRoll,
                                '2':client_interface.setPitch,
                                '3':client_interface.setYaw,
                                '4':client_interface.setX,
                                '5':client_interface.setY,
                                '6':client_interface.setZ
                                }

    def run(self):
        code = self.key_entry_in.getCode()
        Set = self.Control_Dict[code[0]]
        if self.input_type == 'tap':
            if not self.key_entry_in.getKill():
                Set(self.key_entry_in.getSpeed())
            else:
                Set(self.NEUTRAL)
#            self.count = self.key_entry_in.getSpeed()
#            while self.count == self.key_entry_in.getSpeed() and not self.key_entry_in.getKill():
#                Set(self.key_entry_in.getSpeed())
#                time.sleep(.01)
#                if self.key_entry_in.getSpeed() == self.NEUTRAL:
#                    break
                
        elif self.input_type == 'hold':
            self.count = self.NEUTRAL
            while self.key_entry_in.getIsPressed() and not self.key_entry_in.getKill():
                if code[1] == '1' and self.count < 255:
                    self.count = self.count + 1
                    
                elif code[1] == '2' and self.count > 0:
                    self.count = self.count - 1
                    
                self.key_entry_in.setSpeed(self.count)
                Set(self.count)
                time.sleep(.01)
            Set(self.NEUTRAL)
            self.key_entry_in.setSpeed(self.NEUTRAL)
            
            