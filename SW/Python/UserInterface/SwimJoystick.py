'''
Created on Apr 29, 2013

@author: Jeff and Mike 
'''
import threading
import clr
clr.AddReference('SlimDX')
import SlimDX
import SlimDX.DirectInput
import time


class SwimJoystick(threading.Thread):
    '''
    classdocs
    '''
    def __init__(self):
        try:
            threading.Thread.__init__(self)
            self.daemon = True
            self.stick = SlimDX.DirectInput.Joystick
            self.state = SlimDX.DirectInput.JoystickState()
            dinput = SlimDX.DirectInput.DirectInput()
            
            for device in dinput.GetDevices(SlimDX.DirectInput.DeviceClass.GameController, SlimDX.DirectInput.DeviceEnumerationFlags.AttachedOnly):
                try:
                    self.stick = SlimDX.DirectInput.Joystick(dinput, device.InstanceGuid);
                    self.stick.SetCooperativeLevel(self, CooperativeLevel.Exclusive | CooperativeLevel.Foreground);
                    break;
                except:
                    pass
            
            if self.stick == None:
                MessageBox.Show("There are no joysticks attached to the system.")
                print "There are no joysticks attached to the system."
                return
            
            for deviceObject in self.stick.GetObjects():
                if deviceObject.ObjectType != 0 and SlimDX.DirectInput.ObjectDeviceType.Axis != 0:
                    gar = self.stick.GetObjectPropertiesById(int(deviceObject.ObjectType))
                    #gar.SetRange(-1000,1000)
            self.stick.Acquire()
            self.valForward  = 127
            self.valRoll  = 127
            self.valVertical = 127
            self.valYaw  = 127
            self.valPitch = 127
            self.arm = False
            
            self.start()
        except Exception as e:
            raise e
        
    def run(self):
        last_arm = False
        while True:
            try:
                currentstate = self.stick.GetCurrentState()
                self.valForward = self.dead_zone( self.invert(currentstate.Y/256) ) 
                self.valRoll = self.dead_zone( currentstate.RotationX/256 )
                self.valVertical = self.dead_zone(currentstate.Z/256 )
                self.valYaw = self.dead_zone( self.invert(currentstate.X/256) )
                self.valPitch = self.dead_zone( currentstate.RotationY/256 )
                #self.valYaw = self.help_straight(self.valForward, self.valYaw)
                self.valRoll = self.scale_rotation(self.valRoll)
                self.valPitch = self.scale_rotation(self.valPitch)
                
                temp_arm = currentstate.GetButtons()[0]
                if not last_arm and currentstate.GetButtons()[0]:
                    self.arm = not self.arm
                last_arm = temp_arm
            except Exception as e:
                print "something wrong with controller" + str(e)
                pass
            
            time.sleep(0.2)
            
    def invert(self, val):
        max = 256
        return max - val
        
    def dead_zone(self, val):
        neutral = 127
        range = 25
        if (neutral-range) < val < (neutral+range):
            return neutral
        else:
            return val + range*int(val<neutral) - range*int(val>neutral)
            
    def scale_rotation(self, val):
        a = 0.75
        neutral = 127
        v = val-neutral
        v *= a
        return neutral + v
        
    def help_straight(self, forward, yaw):
        neutral = 127
        threshold = 70
        scale = 0.3
        if forward > (neutral + threshold):
            y = abs(yaw - neutral)
            yaw = neutral + scale*y*int(yaw > neutral) - scale*y*int(yaw < neutral)
        return yaw
        
    def getForward(self):
        return int(self.valForward)
    
    def getRoll(self):
        return int(self.valRoll)
    
    def getVertical(self):
        return int(self.valVertical)
    
    def getYaw(self):
        return int(self.valYaw)
    
    def getPitch(self):
        return int(self.valPitch)
    
    def getARM(self):
        return self.arm
                
if __name__ == "__main__":
    joy = SwimJoystick()
    while 1:
        print "Forward: {0} Roll: {1} Vertical: {2} Yaw: {3} Pitch: {4}".format(joy.getForward(), 
                                        joy.getRoll(), joy.getVertical(), joy.getYaw(),joy.getPitch())
        time.sleep(.05)
        