'''
Created 2/9/2013

@author: Jon
'''

import sys
sys.path.append('C:\\WINDOWS\\Microsoft.NET\\Framework\\v2.0.50727')
sys.path.append('C:\Python27\Lib\site-packages')
sys.path.append("C:\Python27\Lib")
sys.path.append('C:\Users\Jon\Documents\GitHub\SWIM-R\Mike\SWIMR')
sys.path.append('C:\Users\Jeff\Documents\GitHub\SWIM-R\Mike\SWIMR')
import clr
import System
import socket
import time
from client_interface import *
from ControlsEntry import *
from Key_Map import *
from KeyDown_Custom import *
import threading
import cPickle

clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System.Drawing import *
from System.Windows.Forms import *

class MyForm(Form):
    '''
    classdocs
    '''    
        
    def __init__(self):
        #globals
        self.key_map = Key_Map()
        self.input_type = 'hold'
        self._lblDirection1 = System.Windows.Forms.Label()
        self._lblDirection2 = System.Windows.Forms.Label()
        self._lblDirection3 = System.Windows.Forms.Label()
        self._lblDirection4 = System.Windows.Forms.Label()
        self._lblDirection5 = System.Windows.Forms.Label()
        self._lblDirection6 = System.Windows.Forms.Label()
        
        try:
            self.testing = sys.argv[1]=='testing'
        except IndexError:
            self.testing = False
        try:
            PI_IP = "192.168.0.103"
            PI_PORT = 9999
            self.client_interface = ClientInterface(PI_IP, PI_PORT, self.testing)
            if not self.testing:
                self.client_interface.start()
        except timeout:
            MessageBox.Show("Something has gone wrong with client_interface")

        self.InitializeGUI()
        self.LoadPastState()
       
    def InitializeGUI(self):     
        #initialize events
        self.KeyDown += KeyEventHandler(self.Key_Pressed)
        self.KeyUp += KeyEventHandler(self.Key_Released)
        #
        #image rotation stuff
        #
        self.current_angle = float()
        self.bitmap = System.Drawing.Bitmap("compass.png")
        self.pictyaBOX = System.Windows.Forms.PictureBox()
        self.pictyaBOX.Image = self.bitmap
        self.pictyaBOX.Size = System.Drawing.Size(self.bitmap.Width,self.bitmap.Height)
        self.pictyaBOX.Location = System.Drawing.Point(200, 200)
        self.pictyaBOX.MouseClick += MouseEventHandler(self.CallRotate)
        self.Controls.Add(self.pictyaBOX)

        # Configure motor value labels
        self._lblDirection1.Text = '128'
        self._lblDirection1.Location = System.Drawing.Point(180, 50)
        self._lblDirection1.Size = System.Drawing.Size(50, 13)

        self._lblDirection2.Text = '128'
        self._lblDirection2.Location = System.Drawing.Point(180, 65)
        self._lblDirection2.Size = System.Drawing.Size(50, 13)

        self._lblDirection3.Text = '128'
        self._lblDirection3.Location = System.Drawing.Point(180, 80)
        self._lblDirection3.Size = System.Drawing.Size(50, 13)

        self._lblDirection4.Text = '128'
        self._lblDirection4.Location = System.Drawing.Point(180, 95)
        self._lblDirection4.Size = System.Drawing.Size(50, 13)

        self._lblDirection5.Text = '128'
        self._lblDirection5.Location = System.Drawing.Point(180, 110)
        self._lblDirection5.Size = System.Drawing.Size(50, 13)
        
        self._lblDirection6.Text = '128'
        self._lblDirection6.Location = System.Drawing.Point(180, 125)
        self._lblDirection6.Size = System.Drawing.Size(50, 13)
        
        #labels to label the other labels
        self._lblD1 = System.Windows.Forms.Label()
        self._lblD2 = System.Windows.Forms.Label()
        self._lblD3 = System.Windows.Forms.Label()
        self._lblD4 = System.Windows.Forms.Label()
        self._lblD5 = System.Windows.Forms.Label()
        self._lblD6 = System.Windows.Forms.Label()

        self._lblD1.Location = System.Drawing.Point(75,50)
        self._lblD1.Size = System.Drawing.Size(120,13)
        self._lblD1.Text = "X:"

        self._lblD2.Location = System.Drawing.Point(75,65)
        self._lblD2.Size = System.Drawing.Size(120,13)
        self._lblD2.Text = "Y:"

        self._lblD3.Location = System.Drawing.Point(75,80)
        self._lblD3.Size = System.Drawing.Size(120,13)
        self._lblD3.Text = "Z:"

        self._lblD4.Location = System.Drawing.Point(75,95)
        self._lblD4.Size = System.Drawing.Size(120,13)
        self._lblD4.Text = "Roll:"

        self._lblD5.Location = System.Drawing.Point(75,110)
        self._lblD5.Size = System.Drawing.Size(120,13)
        self._lblD5.Text = "Pitch:"

        self._lblD6.Location = System.Drawing.Point(75,125)
        self._lblD6.Size = System.Drawing.Size(120,13)
        self._lblD6.Text = "Yaw:"

        #labels for IMU values
        self._lblIMU_roll = System.Windows.Forms.Label()
        self._lblIMU_pitch = System.Windows.Forms.Label()
        self._lblIMU_yaw = System.Windows.Forms.Label()
        
        self._lblIMU_roll.Location = System.Drawing.Point(300,325)
        self._lblIMU_roll.Size = System.Drawing.Size(120,13)
        self._lblIMU_roll.Text = "####"

        self._lblIMU_pitch.Location = System.Drawing.Point(300,340)
        self._lblIMU_pitch.Size = System.Drawing.Size(120,13)
        self._lblIMU_pitch.Text = "####"

        self._lblIMU_yaw.Location = System.Drawing.Point(300,355)
        self._lblIMU_yaw.Size = System.Drawing.Size(120,13)
        self._lblIMU_yaw.Text = "####"

        #main menu
        self._menuStrip1 = System.Windows.Forms.MenuStrip()
        self._fileToolStripMenuItem11 = System.Windows.Forms.ToolStripMenuItem("Settings", None, System.EventHandler(self.Show_A_BOX))
        self._fileToolStripMenuItem12 = System.Windows.Forms.ToolStripMenuItem("Exit", None, System.EventHandler(self.Exit))
        self._fileToolStripMenuItem11.Text = 'Settings'
        self._fileToolStripMenuItem1 = System.Windows.Forms.ToolStripMenuItem("File", None, *System.Array[System.Windows.Forms.ToolStripItem]((self._fileToolStripMenuItem11, self._fileToolStripMenuItem12,)))
        #
        # menuStrip1
        #
        self._menuStrip1.Items.AddRange(System.Array[System.Windows.Forms.ToolStripItem]((self._fileToolStripMenuItem1, )))
        self._menuStrip1.Location = System.Drawing.Point(0, 0)
        self._menuStrip1.Name = 'menuStrip1'
        self._menuStrip1.Size = System.Drawing.Size(292, 24)
        self._menuStrip1.TabIndex = 0
        self._menuStrip1.Text = 'menuStrip1'
        #
        # fileToolStripMenuItem
        #
        self._fileToolStripMenuItem1.Name = 'fileToolStripMenuItem1'
        self._fileToolStripMenuItem1.Size = System.Drawing.Size(35, 20)
        self._fileToolStripMenuItem1.Text = 'File'
        
        # Form
        self.Controls.Add(self._menuStrip1)
        self.MainMenuStrip = self._menuStrip1
        self.Text = 'SWIM-R'
        self.ClientSize = System.Drawing.Size(850, 720)
        self.WindowState = System.Windows.Forms.FormWindowState.Maximized
        label_thread = Thread(target = self.go, args=())
        label_thread.setDaemon(1)
        label_thread.start()
        self.FormClosing += System.Windows.Forms.FormClosingEventHandler(self.Exit)
        #
        # Add the controls to the form.
        #
        self.Controls.Add(self._lblDirection1)
        self.Controls.Add(self._lblDirection2)
        self.Controls.Add(self._lblDirection3)
        self.Controls.Add(self._lblDirection4)
        self.Controls.Add(self._lblDirection5)
        self.Controls.Add(self._lblDirection6)
        self.Controls.Add(self._lblD1)
        self.Controls.Add(self._lblD2)
        self.Controls.Add(self._lblD3)
        self.Controls.Add(self._lblD4)
        self.Controls.Add(self._lblD5)
        self.Controls.Add(self._lblD6)
        self.Controls.Add(self._lblIMU_roll)
        self.Controls.Add(self._lblIMU_pitch)
        self.Controls.Add(self._lblIMU_yaw)
        
        #Configure the image  
        image2 = Image.FromFile("GUI_drawing.png")
        self._pictureBox2 = PictureBox()
        self._pictureBox2.SizeMode = PictureBoxSizeMode.StretchImage
        self._pictureBox2.Image = image2
        self._pictureBox2.Name = "pictureBox2"
        self._pictureBox2.Dock = DockStyle.Fill
        self.Controls.Add(self._pictureBox2)

    def Key_Pressed(self, sender, args):
        if not self.testing:
            if not (self.client_interface.getconnectionstatus()):
                MessageBox.Show("Connection Lost")
                return
            
        key_entry = self.key_map.getKeyEntry(str(args.KeyData))
        if key_entry.getKeyValue() != "Empty":
            counterPartKey_entry = self.key_map.getKeyEntryI(key_entry.getCounterPart())
            if not counterPartKey_entry.getIsPressed() and not key_entry.getIsPressed():
                if self.input_type == 'hold':
                    key_entry.setIsPressed(True)
                    self.Keydown_custom = KeyDown_Custom(key_entry, self.client_interface, self.input_type)
                    self.Keydown_custom.start()
                else:
                    code = key_entry.getCode()
                    if code[1] == '1' and key_entry.getSpeed() < 255:
                        key_entry.setSpeed(key_entry.getSpeed() + 16)
                            
                    elif code[1] == '2' and key_entry.getSpeed() > 0:
                        key_entry.setSpeed(key_entry.getSpeed() - 16)
                    self.key_map.getKeyEntryI(key_entry.getCounterPart()).setSpeed(key_entry.getSpeed())
                    key_entry.setIsPressed(True)
                    self.Keydown_custom = KeyDown_Custom(key_entry, self.client_interface, self.input_type)
                    self.Keydown_custom.start()


    def Key_Released(self, sender, args):
        key_entry = self.key_map.getKeyEntry(str(args.KeyData))
        key_entry.setIsPressed(False)
                
    def Show_A_BOX(self, sender, args):
        self.key_map.setKILLAll(True)
        self.controls_entry = ControlsEntry()
        self.controls_entry.initializeGUI(self.key_map, self.input_type)
        self.controls_entry.Show()
        self.controls_entry.FormClosing += FormClosingEventHandler(self.Controls_Closing_Event)
        
    def Controls_Closing_Event(self, sender, args):
        self.input_type = self.controls_entry.getInputType()
        self.key_map.setKILLAll(False)
        
    def Exit(self, sender, args):
        self.key_map.setKILLAll(True)
        time.sleep(.01)
        
    def LoadPastState(self):
        g = open('config.swmr', 'r')
        data = cPickle.load(g)
        self.input_type = data.pop(12, 'tap')
        self.key_map.setNewDictValues(data)
        #TODO add something in file to load here and set data accordingly
        
    def CallRotate(self,sender,args):
        if args.Button == MouseButtons.Right:
            self.pictyaBOX.Image = self.DoRotate(self.bitmap, 30)
        else:
            self.pictyaBOX.Image = self.DoRotate(self.bitmap, -30)
        
    def DoRotate(self, img = System.Drawing.Image, angle = float()):
        self.current_angle += angle
        returnBitmap = System.Drawing.Bitmap(img.Width, img.Height)
        returnBitmap.SetResolution(img.HorizontalResolution, img.VerticalResolution)
        g = System.Drawing.Graphics.FromImage(returnBitmap)
        g.TranslateTransform(img.Width/2, img.Height / 2)
        g.RotateTransform(self.current_angle);
        g.InterpolationMode = System.Drawing.Graphics.InterpolationMode.PropertyType.HighQualityBicubic
        g.TranslateTransform(-img.Width/2,-img.Height / 2)
        g.DrawImageUnscaled(img, Point(0, 0))
        g.Dispose()
        return returnBitmap
    
    def go(self):
        x1 = self.key_map.getKeyEntryI(6)
        x2 = self.key_map.getKeyEntryI(7)
        y1 = self.key_map.getKeyEntryI(8)
        y2 = self.key_map.getKeyEntryI(9)
        z1 = self.key_map.getKeyEntryI(10)
        z2 = self.key_map.getKeyEntryI(11)
        roll1 = self.key_map.getKeyEntryI(0)
        roll2 = self.key_map.getKeyEntryI(1)
        pitch1 = self.key_map.getKeyEntryI(2)
        pitch2 = self.key_map.getKeyEntryI(3)
        yaw1 = self.key_map.getKeyEntryI(4)
        yaw2 = self.key_map.getKeyEntryI(5)
        
        while True:
            if self.input_type == "hold":
                if x1.getSpeed() == 127 and x2.getSpeed() != 127:
                    self._lblDirection1.Text = str(x2.getSpeed())
                elif x1.getSpeed() != 127 and x2.getSpeed() == 127:
                    self._lblDirection1.Text = str(x1.getSpeed())
                else:
                    self._lblDirection1.Text = str(127)
                    
                if y1.getSpeed() == 127 and y2.getSpeed() != 127:
                    self._lblDirection2.Text = str(y2.getSpeed())
                elif y1.getSpeed() != 127 and y2.getSpeed() == 127:
                    self._lblDirection2.Text = str(y1.getSpeed())
                else:
                    self._lblDirection2.Text = str(127)
                    
                if z1.getSpeed() == 127 and z2.getSpeed() != 127:
                    self._lblDirection3.Text = str(z2.getSpeed())
                elif z1.getSpeed() != 127 and z2.getSpeed() == 127:
                    self._lblDirection3.Text = str(z1.getSpeed())
                else:
                    self._lblDirection3.Text = str(127)
                    
                if roll1.getSpeed() == 127 and roll2.getSpeed() != 127:
                    self._lblDirection4.Text = str(roll2.getSpeed())
                elif roll1.getSpeed() != 127 and roll2.getSpeed() == 127:
                    self._lblDirection4.Text = str(roll1.getSpeed())
                else:
                    self._lblDirection4.Text = str(127)
                    
                if pitch1.getSpeed() == 127 and pitch2.getSpeed() != 127:
                    self._lblDirection5.Text = str(pitch2.getSpeed())
                elif pitch1.getSpeed() != 127 and pitch2.getSpeed() == 127:
                    self._lblDirection5.Text = str(pitch1.getSpeed())
                else:
                    self._lblDirection5.Text = str(127)
                    
                if yaw1.getSpeed() == 127 and yaw2.getSpeed() != 127:
                    self._lblDirection6.Text = str(yaw2.getSpeed())
                elif yaw1.getSpeed() != 127 and yaw2.getSpeed() == 127:
                    self._lblDirection6.Text = str(yaw1.getSpeed())
                else:
                    self._lblDirection6.Text = str(127)
                    
            elif self.input_type == 'tap':
                self._lblDirection1.Text = str(x1.getSpeed())
                self._lblDirection2.Text = str(y1.getSpeed())
                self._lblDirection3.Text = str(z1.getSpeed())
                self._lblDirection4.Text = str(roll1.getSpeed())
                self._lblDirection5.Text = str(pitch1.getSpeed())
                self._lblDirection6.Text = str(yaw1.getSpeed())
                
            time.sleep(.01)
        
    

Application.EnableVisualStyles()
Application.SetCompatibleTextRenderingDefault(False)

form = MyForm()
Application.Run(form)
