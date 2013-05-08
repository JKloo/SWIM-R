'''
Created 2/9/2013

@author: Jon
'''

import sys
sys.path.append('C:\\WINDOWS\\Microsoft.NET\\Framework\\v2.0.50727')
sys.path.append('C:\Python27\Lib\site-packages')
sys.path.append("C:\Python27\Lib")
sys.path.append('..')

import clr
import System
import socket
import time
import threading
import cPickle
import datetime
from System import Array, Byte

clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
clr.AddReference('SlimDX')
import SlimDX
import SlimDX.DirectInput

from System.Drawing import *
from System.Windows.Forms import *

from client_interface import *
from Settings import *
from Key_Map import *
from KeyDown_Custom import *
from SwimJoystick import *

class MyForm(Form):
    '''
    classdocs
    '''    
    def __init__(self):
        #globals
        
        '''
        self.joy = SlimDX.DirectInput.Joystick
        self.state = SlimDX.DirectInput.JoystickState()
        
        dinput = SlimDX.DirectInput.DirectInput()

          
        for device in dinput.GetDevices(SlimDX.DirectInput.DeviceClass.GameController, SlimDX.DirectInput.DeviceEnumerationFlags.AttachedOnly):
        
            try:
                
                self.joy = SlimDX.DirectInput.Joystick(dinput, device.InstanceGuid);
                self.joy.SetCooperativeLevel(self, CooperativeLevel.Exclusive | CooperativeLevel.Foreground);
                break;
            
            except:
                pass
            
        

        if self.joy == None:
        
            MessageBox.Show("There are no joysticks attached to the system.")
            return
        
        for deviceObject in self.joy.GetObjects():
            if deviceObject.ObjectType != 0 and SlimDX.DirectInput.ObjectDeviceType.Axis != 0:
                gar = self.joy.GetObjectPropertiesById(int(deviceObject.ObjectType))
                gar.SetRange(-1000,1000)
        
        self.joy.Acquire();
        '''
        
        self.screen = Screen.PrimaryScreen.Bounds
        self.working_area = Screen.PrimaryScreen.WorkingArea
        self.scaleFactor = float(self.working_area.Width)/1920.0
        self.key_map = Key_Map()
        self.data_archive_location = str()
        self.input_type = 'hold'
        self.is_Armed = False
        self.formClosed = False
        self.fullscreen = False
        self.kill = False
        self.PITCH_LIMIT = 103 * self.scaleFactor
        self.DEPTH_LIMIT = 743 * self.scaleFactor
        try:
            self.testing = sys.argv[1]=='testing'
        except IndexError:
            self.testing = False
        try:
            PI_IP = "192.168.0.104"
            PI_PORT = 9999
            self.Cursor = Cursors.WaitCursor
            self.client_interface = ClientInterface(PI_IP, PI_PORT, self.testing)
            time.sleep(1)
            
        except socket.timeout:
            MessageBox.Show("Something has gone wrong with client_interface")

        self.InitializeGUI()
        self.LoadPastState()     
       
    def InitializeGUI(self):     
        #initialize events
        self.KeyPreview = True
        self.KeyDown += KeyEventHandler(self.Key_Pressed)
        self.KeyUp += KeyEventHandler(self.Key_Released)
        #initialize all controls
        self.WindowState = FormWindowState.Maximized
        self.Size = Size(self.working_area.Width, self.working_area.Height)
        self.input_val_label_x = Label()
        self.input_val_label_y = Label()
        self.input_val_label_z = Label()
        self.input_val_label_roll = Label()
        self.input_val_label_pitch = Label()
        self.input_val_label_yaw = Label()
        self.input_label_x = Label()
        self.input_label_y = Label()
        self.input_label_z = Label()
        self.input_label_roll = Label()
        self.input_label_pitch = Label()
        self.input_label_yaw = Label()
        self.compass_needle = PictureBox()
        self.pitch_indicator = PictureBox()
        self.roll_indicator = PictureBox()
        self.depth_indicator = PictureBox()
        self._lblIMU_roll = Label()
        self._lblIMU_pitch = Label()
        self._lblIMU_yaw = Label()
        self._lblWaterTemp = Label()
        self._lblCaseTemp = Label()
        self._lblHumidity = Label()
        self._lblBatteryLife = Label()
        self.input_label_depth = Label()
        self.splitpanel = SplitContainer()
        self._panel = Panel()
        self.MainWindow = PictureBox()
        self._pictLeft = PictureBox()
        self._pictRight = PictureBox()
        self._pictBottomLeft = PictureBox()
        self._pictBottomRight = PictureBox()
        self._pictMid = PictureBox()
        self._menuStrip1 = MenuStrip()
        self._menuStrip1.SuspendLayout()
        self.SuspendLayout()   
        
        # Configure motor value labels
        self.input_val_label_x.Text = '127'
        self.input_val_label_x.Location = Point(180, 50)
        self.input_val_label_x.Size = Size(50, 13)

        self.input_val_label_y.Text = '127'
        self.input_val_label_y.Location = Point(180, 65)
        self.input_val_label_y.Size = Size(50, 13)

        self.input_val_label_z.Text = '127'
        self.input_val_label_z.Location = Point(180, 80)
        self.input_val_label_z.Size = Size(50, 13)

        self.input_val_label_roll.Text = '127'
        self.input_val_label_roll.Location = Point(180, 95)
        self.input_val_label_roll.Size = Size(50, 13)

        self.input_val_label_pitch.Text = '127'
        self.input_val_label_pitch.Location = Point(180, 110)
        self.input_val_label_pitch.Size = Size(50, 13)
        
        self.input_val_label_yaw.Text = '127'
        self.input_val_label_yaw.Location = Point(180, 125)
        self.input_val_label_yaw.Size = Size(50, 13)
        
        #labels to label the other labels
        self.input_label_x.Location = Point(75,50)
        self.input_label_x.Size = Size(120,13)
        self.input_label_x.Text = "X:"

        self.input_label_y.Location = Point(75,65)
        self.input_label_y.Size = Size(120,13)
        self.input_label_y.Text = "Y:"

        self.input_label_z.Location = Point(75,80)
        self.input_label_z.Size = Size(120,13)
        self.input_label_z.Text = "Z:"

        self.input_label_roll.Location = Point(75,95)
        self.input_label_roll.Size = Size(120,13)
        self.input_label_roll.Text = "Roll:"

        self.input_label_pitch.Location = Point(75,110)
        self.input_label_pitch.Size = Size(120,13)
        self.input_label_pitch.Text = "Pitch:"

        self.input_label_yaw.Location = Point(75,125)
        self.input_label_yaw.Size = Size(120,13)
        self.input_label_yaw.Text = "Yaw:"

        #labels for IMU values
        height = int(self.working_area.Height - 140)
        box_height = 17
        box_width = 175
        h_middle = int(self.working_area.Width / 2)
        box_boarder = 7
        
        self._lblIMU_roll.Location = Point(h_middle - 2*box_width - 3*box_boarder, height)
        self._lblIMU_roll.Size = Size(box_width,box_height)
        self._lblIMU_roll.Text = "####"
        self._lblIMU_roll.Font = Font("Microsoft Sans Serif", 9.5, FontStyle.Bold, GraphicsUnit.Point)
        self._lblIMU_roll.Anchor = AnchorStyles.Bottom
        
        self._lblIMU_pitch.Location = Point(h_middle - box_width - box_boarder,height)
        self._lblIMU_pitch.Size = Size(box_width,box_height)
        self._lblIMU_pitch.Text = "####"
        self._lblIMU_pitch.Font = Font("Microsoft Sans Serif", 9.5, FontStyle.Bold, GraphicsUnit.Point)
        self._lblIMU_pitch.Anchor = AnchorStyles.Bottom
        
        self._lblIMU_yaw.Location = Point(h_middle + box_boarder,height)
        self._lblIMU_yaw.Size = Size(box_width,box_height)
        self._lblIMU_yaw.Text = "####"
        self._lblIMU_yaw.Font = Font("Microsoft Sans Serif", 9.5, FontStyle.Bold, GraphicsUnit.Point)
        self._lblIMU_yaw.Anchor = AnchorStyles.Bottom
        
        self.input_label_depth.Location = Point(h_middle + box_width + 3*box_boarder, height)
        self.input_label_depth.Size = Size(box_width,box_height)
        self.input_label_depth.Text = "####"
        self.input_label_depth.Font = Font("Microsoft Sans Serif", 9.5, FontStyle.Bold, GraphicsUnit.Point)
        self.input_label_depth.Anchor = AnchorStyles.Bottom
        
        self._lblWaterTemp.Location = Point(h_middle - 2*box_width - 3*box_boarder, height + box_height + box_boarder)
        self._lblWaterTemp.Size = Size(box_width,box_height)
        self._lblWaterTemp.Text = "####"
        self._lblWaterTemp.Font = Font("Microsoft Sans Serif", 9.5, FontStyle.Bold, GraphicsUnit.Point)
        self._lblWaterTemp.Anchor = AnchorStyles.Bottom
        
        self._lblCaseTemp.Location = Point(h_middle - box_width - box_boarder, height + box_height + box_boarder)
        self._lblCaseTemp.Size = Size(box_width,box_height)
        self._lblCaseTemp.Text = "####"
        self._lblCaseTemp.Font = Font("Microsoft Sans Serif", 9.5, FontStyle.Bold, GraphicsUnit.Point)
        self._lblCaseTemp.Anchor = AnchorStyles.Bottom
        
        self._lblHumidity.Location = Point(h_middle + box_boarder, height + box_height + box_boarder)
        self._lblHumidity.Size = Size(box_width,box_height)
        self._lblHumidity.Text = "####"
        self._lblHumidity.Font = Font("Microsoft Sans Serif", 9.5, FontStyle.Bold, GraphicsUnit.Point)
        self._lblHumidity.Anchor = AnchorStyles.Bottom
        
        self._lblBatteryLife.Location = Point(h_middle + box_width + 3*box_boarder, height + box_height + box_boarder)
        self._lblBatteryLife.Size = Size(box_width,box_height)
        self._lblBatteryLife.Text = "####"
        self._lblBatteryLife.Font = Font("Microsoft Sans Serif", 9.5, FontStyle.Bold, GraphicsUnit.Point)
        self._lblBatteryLife.Anchor = AnchorStyles.Bottom
    
        #panel
        self.splitpanel.BackColor = Color.Transparent
        self.splitpanel.Dock = DockStyle.Fill
        self.splitpanel.Name = 'splitp'
        self.splitpanel.Size = Size(self.ClientRectangle.Width, self.ClientRectangle.Height)
        self.splitpanel.Orientation = Orientation.Horizontal
        self.splitpanel.SplitterDistance = self._menuStrip1.Height-1
        self.splitpanel.Margin = Padding(0)
        self.splitpanel.IsSplitterFixed = True
        self.splitpanel.FixedPanel = FixedPanel.Panel1
        self.splitpanel.SplitterWidth = 1
        self.splitpanel.Panel2.Controls.Add(self.MainWindow)
        
        #Configure the main image
        self.MainWindow.BackColor = Color.White
        self.MainWindow.Dock = DockStyle.Fill
        self.MainWindow.SizeMode = PictureBoxSizeMode.CenterImage
        self.MainWindow.Location = Point(0, 1)
        GUI_drawing = Image.FromFile("images/temp.gif")
        self.MainWindow.Image = GUI_drawing
        self.MainWindow.Name = "MainWindow"
        
        #configure bottom left
        self._pictBottomLeft.BackColor = Color.Transparent
        self._pictBottomLeft.SizeMode = PictureBoxSizeMode.StretchImage
        pictBottomLeft_image = Image.FromFile( "images/bottomleft.png")
        self._pictBottomLeft.Image = pictBottomLeft_image
        self._pictBottomLeft.Size = Size(pictBottomLeft_image.Width * self.scaleFactor, pictBottomLeft_image.Height * self.scaleFactor)
        self._pictBottomLeft.Location = Point(0, self.MainWindow.Height - pictBottomLeft_image.Height * self.scaleFactor)
        self._pictBottomLeft.Anchor = (AnchorStyles.Bottom \
                                  | AnchorStyles.Left)
        
        #Configure left image
        self._pictLeft.BackColor = Color.Transparent
        self._pictLeft.SizeMode = PictureBoxSizeMode.StretchImage
        self._pictLeft.Location = Point(0,0)
        self._pictLeft.Anchor = ((AnchorStyles.Top \
                                  | AnchorStyles.Bottom) \
                                  | AnchorStyles.Left)
        pictLeft_image = Image.FromFile( 'images/left.png')
        self._pictLeft.Image = pictLeft_image
        self._pictLeft.Size = Size(pictLeft_image.Width * self.scaleFactor, self.MainWindow.Height - pictBottomLeft_image.Height * self.scaleFactor)
        
        #configure bottom right
        self._pictBottomRight.BackColor = Color.Transparent
        self._pictBottomRight.SizeMode = PictureBoxSizeMode.StretchImage
        pictBottomRight_image = Image.FromFile( "images/bottomright.png")
        self._pictBottomRight.Image = pictBottomRight_image
        self._pictBottomRight.Size = Size(pictBottomLeft_image.Width * self.scaleFactor, pictBottomRight_image.Height * self.scaleFactor)
        self._pictBottomRight.Location = Point(self.MainWindow.Width - pictBottomRight_image.Width * self.scaleFactor, self.MainWindow.Height - pictBottomRight_image.Height * self.scaleFactor)
        self._pictBottomRight.Anchor = (AnchorStyles.Bottom \
                                  | AnchorStyles.Right)
        
        #Configure right image
        self._pictRight.BackColor = Color.Transparent
        self._pictRight.SizeMode = PictureBoxSizeMode.StretchImage
        pictRight_image = Image.FromFile( 'images/right.png')
        self._pictRight.Size = Size(pictLeft_image.Width * self.scaleFactor, self.MainWindow.Height - pictBottomRight_image.Height * self.scaleFactor)
        self._pictRight.Location = Point(self.MainWindow.Width - pictRight_image.Width * self.scaleFactor, 0)
        self._pictRight.Anchor = ((AnchorStyles.Top \
                                  | AnchorStyles.Bottom) \
                                  | AnchorStyles.Right)
        self._pictRight.Image = pictRight_image
        
        #Configure middle bar
        self._pictMid.BackColor = Color.Transparent
        self._pictMid.SizeMode = PictureBoxSizeMode.StretchImage
        pictMid_image = Image.FromFile( 'images/middle.png')
        self._pictMid.Size = Size(pictMid_image.Width * self.scaleFactor, pictMid_image.Height * self.scaleFactor)
        self._pictMid.Location = Point(self.MainWindow.Width/2 - (pictMid_image.Width * self.scaleFactor)/2, self.MainWindow.Height - pictMid_image.Height * self.scaleFactor)
        self._pictMid.Anchor = ((AnchorStyles.Left \
                                  | AnchorStyles.Bottom) \
                                  | AnchorStyles.Right)
        self._pictMid.Image = pictMid_image
        
        #image needle stuff
        self.compass_needle.BackColor = Color.Transparent
        self.compass_needle_image = Image.FromFile( "images/compass.png")
        self.compass_needle.SizeMode = PictureBoxSizeMode.StretchImage
        self.compass_needle.Image = self.compass_needle_image
        self.compass_needle.Size = Size(self.compass_needle_image.Width * self.scaleFactor, self.compass_needle_image.Height * self.scaleFactor)
        self.compass_needle.Location = Point(self._pictBottomRight.Width *.604 - self.compass_needle.Width/2, self._pictBottomRight.Height *.555 - self.compass_needle.Width/2)
        self._pictBottomRight.Controls.Add(self.compass_needle)
        self.compass_needle.Anchor = (AnchorStyles.Bottom \
                                  | AnchorStyles.Right)
        #roll indicator
        self.roll_indicator.BackColor = Color.Transparent
        self.roll_indicator_image = Image.FromFile( "images/roll_indicator_285x285.png")
        self.roll_indicator.SizeMode = PictureBoxSizeMode.StretchImage
        self.roll_indicator.Image = self.roll_indicator_image
        self.roll_indicator.Size = Size(self.roll_indicator_image.Width * self.scaleFactor, self.roll_indicator_image.Height * self.scaleFactor)
        self.roll_indicator.Location = Point(self._pictBottomLeft.Width *.407 - self.roll_indicator.Width/2, self._pictBottomLeft.Height *.555 - self.roll_indicator.Width/2)
        self._pictBottomLeft.Controls.Add(self.roll_indicator)
        self.roll_indicator.Anchor = (AnchorStyles.Bottom \
                                  | AnchorStyles.Left)
               
        #pitch indicator
        self.pitch_indicator.BackColor = Color.Transparent
        self.pitch_indicator_image = Image.FromFile( "images/pitch_indicator_285x285.png")
        self.pitch_indicator.SizeMode = PictureBoxSizeMode.StretchImage
        self.pitch_indicator.Image = self.pitch_indicator_image
        self.pitch_indicator.Size = Size(self.pitch_indicator_image.Width * self.scaleFactor, self.pitch_indicator_image.Height * self.scaleFactor)
        self.pitch_indicator.Location = Point(1,1)
        self.roll_indicator.Controls.Add(self.pitch_indicator)
        self.pitch_indicator.Anchor = (AnchorStyles.Bottom \
                                  | AnchorStyles.Left)
        self.pitch_indicator.Name = "pitch_indicator"
        
        #depth indicator
        self.depth_indicator.BackColor = Color.Transparent
        self.depth_indicator_image = Image.FromFile( "images/depth_indicator_285x285.png")
        self.depth_indicator.SizeMode = PictureBoxSizeMode.StretchImage
        self.depth_indicator.Image = self.depth_indicator_image
        self.depth_indicator.Size = Size(self.depth_indicator_image.Width * self.scaleFactor, self.depth_indicator_image.Height * self.scaleFactor)
        self.depth_indicator.Location = Point(self._pictLeft.Width/2. -self.depth_indicator.Width/2.,0-self.depth_indicator.Height/2.)
        self._pictRight.Controls.Add(self.depth_indicator)
        self.depth_indicator.Anchor = (AnchorStyles.Top \
                                  | AnchorStyles.Left)
        self.depth_indicator.Name = "depth_indicator"
        
        #main menu
        self._fileToolStripMenuItem12 = ToolStripMenuItem("&Fullscreen", None, System.EventHandler(self.Fullscreen))
        self._fileToolStripMenuItem12.ShortcutKeys = (Keys.Control | Keys.F)
        
        self._fileToolStripMenuItem13 = ToolStripMenuItem("Arm\t", None, System.EventHandler(self.Arm))
        self._fileToolStripMenuItem13.ShortcutKeys = (Keys.Control | Keys.A)
        
        self._fileToolStripMenuItem14 = ToolStripMenuItem("E&xit\t", None, System.EventHandler(self.Exit))
        self._fileToolStripMenuItem14.ShortcutKeys = (Keys.Control | Keys.X)
        self._fileToolStripMenuItem14.ShowShortcutKeys = False
        
        self._fileToolStripMenuItem1 = ToolStripMenuItem("&File")
        self._fileToolStripMenuItem1.DropDownItems.Add(self._fileToolStripMenuItem12)
        self._fileToolStripMenuItem1.DropDownItems.Add(self._fileToolStripMenuItem13)
        self._fileToolStripMenuItem1.DropDownItems.Add(self._fileToolStripMenuItem14)
        
        self._fileToolStripMenuItem22 = ToolStripMenuItem("&Controls", None, System.EventHandler(self.ShowSettings))
        self._fileToolStripMenuItem22.ShortcutKeys = (Keys.Control | Keys.C)
        
        self._fileToolStripMenuItem23 = ToolStripMenuItem("&Output", None, System.EventHandler(self.ShowSettings))
        self._fileToolStripMenuItem23.ShortcutKeys = (Keys.Control | Keys.O)
        
        self._fileToolStripMenuItem2 = ToolStripMenuItem("S&ettings")
        self._fileToolStripMenuItem2.DropDownItems.Add(self._fileToolStripMenuItem22)
        self._fileToolStripMenuItem2.DropDownItems.Add(self._fileToolStripMenuItem23)
        #
        # menuStrip1
        #
        self._menuStrip1.Items.AddRange(System.Array[ToolStripItem]((self._fileToolStripMenuItem1, self._fileToolStripMenuItem2,)))
        self._menuStrip1.Location = Point(0, 0)
        self._menuStrip1.Name = 'menuStrip1'
        self._menuStrip1.Size = Size(292, 24)
        self._menuStrip1.TabIndex = 0
        self._menuStrip1.Text = 'menuStrip1'
        
        # Form
        self.MainMenuStrip = self._menuStrip1
        self.Text = 'SWIM-R'
        
        self.joy = False
        self.joystick = None
        self.joy_thread = Thread(target=self.update_joy, args=())
        self.joy_thread.setDaemon(1)
        self.joy_thread.start()

        
        self.video_thread = Thread(target = self.update_video, args=())
        self.video_thread.setDaemon(1)
        self.video_thread.start()
        
        self.label_thread = Thread(target = self.update_labels, args=())
        self.label_thread.setDaemon(1)
        self.label_thread.start()
        
        self.FormClosing += FormClosingEventHandler(self.Exit)
        self.Load += System.EventHandler(self.FormLoad)
        
        #
        # Add the controls to the form.
        #
        self.MainWindow.Controls.Add(self.input_val_label_x)
        self.MainWindow.Controls.Add(self.input_val_label_y)
        self.MainWindow.Controls.Add(self.input_val_label_z)
        self.MainWindow.Controls.Add(self.input_val_label_roll)
        self.MainWindow.Controls.Add(self.input_val_label_pitch)
        self.MainWindow.Controls.Add(self.input_val_label_yaw)
        self.MainWindow.Controls.Add(self.input_label_x)
        self.MainWindow.Controls.Add(self.input_label_y)
        self.MainWindow.Controls.Add(self.input_label_z)
        self.MainWindow.Controls.Add(self.input_label_roll)
        self.MainWindow.Controls.Add(self.input_label_pitch)
        self.MainWindow.Controls.Add(self.input_label_yaw)
        self.MainWindow.Controls.Add(self._lblIMU_roll)
        self.MainWindow.Controls.Add(self._lblIMU_pitch)
        self.MainWindow.Controls.Add(self._lblIMU_yaw)
        self.MainWindow.Controls.Add(self._lblWaterTemp)
        self.MainWindow.Controls.Add(self._lblCaseTemp)
        self.MainWindow.Controls.Add(self._lblHumidity)
        self.MainWindow.Controls.Add(self._lblBatteryLife)
        self.MainWindow.Controls.Add(self.input_label_depth)
        self.MainWindow.Controls.Add(self._pictLeft)
        self.MainWindow.Controls.Add(self._pictBottomLeft)
        self.MainWindow.Controls.Add(self._pictRight)
        self.MainWindow.Controls.Add(self._pictBottomRight)
        self.MainWindow.Controls.Add(self._pictMid)
        self.splitpanel.Panel1.Controls.Add(self._menuStrip1)
        self.Controls.Add(self.splitpanel)
        
        self._menuStrip1.ResumeLayout(False);
        self._menuStrip1.PerformLayout();
        self.ResumeLayout(False);
        self.PerformLayout()
        print "Form Initialized"
        
    def FormLoad(self,sender,args):
        if not self.testing:
            while not self.client_interface.getconnectionstatus():
                time.sleep(1)
        self.Cursor = Cursors.Default
    
    def Key_Pressed(self, sender, args):
        if self.fullscreen and str(args.KeyData) == "Escape":
            self.FormBorderStyle = FormBorderStyle.Fixed3D
            self.WindowState = FormWindowState.Maximized
            self.fullscreen = False
            self.splitpanel.Panel1Collapsed =False
            
        if not self.testing:
            try:
                if not (self.client_interface.getconnectionstatus()):
                    MessageBox.Show("Connection Lost")
                    return
            except:
                self.client_interface = ClientInterface(PI_IP, PI_PORT, self.testing)
            
        if self.is_Armed:
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
                            key_entry.setSpeed(key_entry.getSpeed() + 8)
                                
                        elif code[1] == '2' and key_entry.getSpeed() > 0:
                            key_entry.setSpeed(key_entry.getSpeed() - 8)
                        self.key_map.getKeyEntryI(key_entry.getCounterPart()).setSpeed(key_entry.getSpeed())
                        key_entry.setIsPressed(True)
                        self.Keydown_custom = KeyDown_Custom(key_entry, self.client_interface, self.input_type)
                        self.Keydown_custom.start()

    def Key_Released(self, sender, args):
        key_entry = self.key_map.getKeyEntry(str(args.KeyData))
        key_entry.setIsPressed(False)
          
    def ShowSettings(self, sender, args):
        self.key_map.setKILLAll(True)
        self.kill = True
        self.controls_entry = Settings()
        if sender.Text == "&Controls":
            self.controls_entry.initializeGUI(self.key_map,0)
        else:
            self.controls_entry.initializeGUI(self.key_map,1)
        self.controls_entry.Show()
        self.controls_entry.FormClosing += FormClosingEventHandler(self.Controls_Closing_Event)
        
    def Controls_Closing_Event(self, sender, args):
        self.input_type = self.controls_entry.getInputType()
        self.data_archive_location = self.controls_entry.getDataLocation()
        self.use_data_archiving = self.controls_entry.getUseDataArchiving()
        self.key_map.setKILLAll(False)
        self.kill = False
        if not self.video_thread.is_alive():
            self.video_thread = Thread(target = self.update_video, args=())
            self.video_thread.start()
        if not self.label_thread.is_alive():
            self.label_thread = Thread(target = self.update_labels, args=())
            self.label_thread.start()
        
    def Arm(self, sender, args):
        if not self.is_Armed: 
            self.is_Armed = True
            self.client_interface.setARM(True)
            self._fileToolStripMenuItem13.Text = "Disarm"
            if self.use_data_archiving:
                self.data_archive_thread = Thread(target = self.do_data_archive, args=())
                self.data_archive_thread.start()
        else:
            self.client_interface.setARM(False)
            self._fileToolStripMenuItem13.Text = "Arm"
            self.is_Armed = False
        
    def Fullscreen(self, sender, args):
        if not self.fullscreen:
            self.FormBorderStyle = FormBorderStyle.None
            self.TopMost = True
            self.splitpanel.Panel1Collapsed =True
            self.Location = Point(0,0)
            self.fullscreen = True
            self.WindowState = FormWindowState.Normal
            self.Size = Size(self.screen.Width, self.screen.Height)
        else:
            self.FormBorderStyle = FormBorderStyle.Fixed3D
            self.WindowState = FormWindowState.Maximized
            self.fullscreen = False
            self.splitpanel.Panel1Collapsed =False
                
    def Exit(self, sender, args):
        self.key_map.setKILLAll(True)
        time.sleep(.01)
        self.Control_Dict = {
                                '1':self.client_interface.setRoll,
                                '2':self.client_interface.setPitch,
                                '3':self.client_interface.setYaw,
                                '4':self.client_interface.setX,
                                '5':self.client_interface.setY,
                                '6':self.client_interface.setZ
                                }
        for key in self.Control_Dict.keys():
            Set = self.Control_Dict[key]
            Set(127)
        self.kill = True
        self.is_Armed = False
        self.client_interface.setARM(False)
        '''
        if self.joy != None:
            
            self.joy.Unacquire()
            self.joy.Dispose();
            
        self.joy = None;    
            '''
            
            
            
        if not self.formClosed:
            self.formClosed = True
            self.Close()
        return
        
    def LoadPastState(self):
        defaultfile = "DefaultData.csv"
        data = object()
        try:
            g = open('config.swmr', 'r')
            data = cPickle.load(g)
            self.input_type = data.pop(12, 'tap')
            self.key_map.setNewDictValues(data)
            self.data_archive_location = data.pop(13, defaultfile)
            if not os.path.exists(self.data_archive_location):
                self.data_archive_location = defaultfile
            self.use_data_archiving = data.pop(14, False)
            print "Past state loaded"
        except IOError:
            f = open('config.swmr', 'w')
            default_dict = {
                         0:'E',
                         1:'Q',
                         2:'S',
                         3:'W',
                         4:'A',
                         5:'D',
                         6:'Up',
                         7:'Down',
                         8:'Left',
                         9:'Right',
                         10:'Space',
                         11:'B',
                         12:'tap',
                         13:defaultfile,
                         14:False
                         }
            cPickle.dump(default_dict, f)
            f.close()
            self.input_type = default_dict[12]
            self.key_map.setNewDictValues(default_dict)
            self.data_archive_location = default_dict[13]
            self.use_data_archiving = default_dict[14]
            print "Past state NOT loaded"
        
    def RotateImage(self, img = Image, angle = float()):
        returnBitmap = Bitmap(img.Width, img.Height)
        try:
            returnBitmap.SetResolution(img.HorizontalResolution, img.VerticalResolution)
            returnBitmap.MakeTransparent()
            g = Graphics.FromImage(returnBitmap)
            
            g.TranslateTransform(img.Width/2, img.Height / 2)
            g.RotateTransform(angle);
            g.InterpolationMode = Graphics.InterpolationMode.PropertyType.HighQualityBicubic
            g.TranslateTransform(-img.Width/2,-img.Height / 2)
            g.DrawImageUnscaled(img, Point(0, 0))
            g.Dispose()
        except:
            pass
        return returnBitmap
    
    def MoveVerticalIndicators(self, img = PictureBox, input = float()):
        new_location = img.Location
        try:
            input *= -1 # flip the sign because windows are numbered upside down
            if img.Name == 'pitch_indicator':
                if input > 45:
                    new_location.Y = self.PITCH_LIMIT
                elif input < -45:
                    new_location.Y =-self.PITCH_LIMIT
                else:
                    new_location.Y = input * (self.PITCH_LIMIT/45.)
                    '''
                    
                    depth scale is 20
                    
                    '''
            if img.Name == 'depth_indicator':
                if input > 0:
                    new_location.Y = 0
                elif input < -20:
                    new_location.Y = self.DEPTH_LIMIT - img.Height * .5
                else:
                    new_location.Y = -input * (self._pictRight.Height/20.) - img.Height/2.
        except:
            pass
        return new_location
    
    def do_data_archive(self):
        if not os.path.exists(self.data_archive_location):
            self.data_file = open(self.data_archive_location, 'a')
            self.data_file.writelines("DateTime, WaterTemp, CaseTemp, Humdity, Depth\n")
        else:
            self.data_file = open(self.data_archive_location, 'a')
        while self.is_Armed:
            now = datetime.datetime.now()
            if now.second == 0 and now.microsecond/100000 == 0:
                self.data_file.writelines("{0}, {1}, {2}, {3}, {4}\n".format(str(now.strftime("%Y-%m-%d %I:%M %p")), \
                                                                      str(float(self.client_interface.getWaterTemperature())), \
                                                                      str(float(self.client_interface.getCaseTemperature())),\
                                                                      str(float(self.client_interface.getHumidity())), \
                                                                      str(float(self.client_interface.getDepth()))))
            time.sleep(.1)
        self.data_file.close()
        
    def update_joy(self):
        try:
            self.joystick = SwimJoystick()
            print "joystick attached!"
            self.joy = True
        except:
            self.joy = False
        while not self.kill:
            if self.joy:
                self.client_interface.setX(self.joystick.getForward())
                self.client_interface.setYaw(self.joystick.getYaw())
                self.client_interface.setZ(self.joystick.getVertical())
                self.client_interface.setRoll(self.joystick.getRoll())
                self.client_interface.setPitch(self.joystick.getPitch())
                self.client_interface.setARM(self.joystick.getARM())
                #print self.client_interface.getpacket()
                self.is_Armed = self.joystick.getARM()
                if self.is_Armed:
                    self._fileToolStripMenuItem13.Text = "Disarm"
                else:
                    self._fileToolStripMenuItem13.Text = "Arm"
            time.sleep(0.1)
        
        
    def update_video(self):
        #if not self.testing:
            self.MainWindow.SizeMode = PictureBoxSizeMode.StretchImage
            while not self.kill:
                try:
                    sourceURL = "http://192.168.0.103/jpg/image.jpg"
                    #sourceURL = "http://192.168.0.103/video.mp4"
                    buffer = Array.CreateInstance(System.Byte, 100000)
                    read = 0 
                    
                
                    total = 0
                    req = clr.Convert(System.Net.WebRequest.Create(sourceURL),System.Net.HttpWebRequest)
                
                    resp = req.GetResponse()
                    stream = resp.GetResponseStream()
                    read = stream.Read(buffer, total, 1000)
                    while (read != 0):
                        total += read
                        read = stream.Read(buffer, total, 1000)
                    ms = System.IO.MemoryStream( buffer, 0, total )
                    self.MainWindow.Image = Bitmap.FromStream( ms )
                    time.sleep(.01)
                    try:
                        pass
#                        file = System.IO.FileStream("video.avi", System.IO.FileMode.Create, System.IO.FileAccess.Write)
#                        ms.Read(buffer, 0, total)
#                        file.Write( buffer, 0, total )
#                        file.Close()

#                        f = open("video.avi", "wb")
#                        f.write(System.IO.MemoryStream( buffer, 0, total ))
#                        f.close()
                    except Exception,e:
                        print "no video save: {0}".format(e)
                except Exception as e:
                    print "this one: " + str(e)
        
    def update_labels(self):

        while not self.kill:
            try:
                if not self.client_interface.getconnectionstatus():
                    self._fileToolStripMenuItem13.Text = "Arm"
                    self.is_Armed = False   
                
                speeds = self.client_interface.getpacket()
                self.input_val_label_x.Text = str(speeds['X'])
                self.input_val_label_y.Text = str(speeds['Y'])
                self.input_val_label_z.Text = str(speeds['Z'])
                self.input_val_label_roll.Text = str(speeds['ROLL'])
                self.input_val_label_pitch.Text = str(speeds['PITCH'])
                self.input_val_label_yaw.Text = str(speeds['YAW'])

            except:
                print "SPEED LABELS ERROR!!"
            
            try:
                self.roll_indicator.Image = self.RotateImage(self.roll_indicator_image, float(self.client_interface.getRoll()))
                self.roll_indicator.BackColor = Color.Transparent
                self._lblIMU_roll.Text = "Roll: {0} [deg]".format(  str(float(self.client_interface.getRoll())))
                
                self.pitch_indicator.Location = self.MoveVerticalIndicators(self.pitch_indicator, float(self.client_interface.getPitch()))
                self._lblIMU_pitch.Text = "Pitch: {0} [deg]".format( str(float(self.client_interface.getPitch())))
                                
                self.depth_indicator.Location = self.MoveVerticalIndicators(self.depth_indicator, float(self.client_interface.getDepth()))
                self.input_label_depth.Text = "Depth: {0} [ft]".format( str(float(self.client_interface.getDepth())))
                
                self.compass_needle.Image = self.RotateImage(self.compass_needle_image, float(self.client_interface.getYaw()))
                self.compass_needle.BackColor = Color.Transparent
                self._lblIMU_yaw.Text = "Yaw: {0} [deg]".format( str(float(self.client_interface.getYaw())))
                
                self._lblWaterTemp.Text = "Water Temp: {0} [degC]".format( str(float(self.client_interface.getWaterTemperature())))
                self._lblCaseTemp.Text = "Case Temp: {0} [degC]".format( str(float(self.client_interface.getCaseTemperature())))
                self._lblHumidity.Text = "Humidity: {0} [%]".format( str(float(self.client_interface.getHumidity())))
                self._lblBatteryLife.Text = "Battery: {0} [V]".format( str(float(self.client_interface.getBatteryLife())))
                
            except:
                print "IMU LABELS ERROR!!"
            
            time.sleep(.1)



Application.EnableVisualStyles()
Application.SetCompatibleTextRenderingDefault(False)

form = MyForm()
Application.Run(form)
