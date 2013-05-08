
import sys
sys.path.append('C:\\WINDOWS\\Microsoft.NET\\Framework\\v2.0.50727')
sys.path.append('C:\Python27\Lib\site-packages')
sys.path.append("C:\Python27\Lib")
sys.path.append('..')

import clr
import System
from client_interface import *
from  threading import Thread
import time
from Key_Map import *
from Key_Entry import *
import cPickle

clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System.Drawing import *
from System.Windows.Forms import *


class Settings(Form):
    """description of class"""
    def initializeGUI(self, key_map = Key_Map(), tab_index = int()):
        #globals
        self.keyPressed = bool()
        self.new_Value = str()
        self.read = bool()
        self.counter = 99
        self.L = threading.Lock()
        self.cancel_countdown = False
        self.tab_index = tab_index
        
        self.gkey_map = key_map
        self.input_key_dict = self.gkey_map.getKeyDict()
        self.new_Dict = {
                         0:'-',
                         1:'-',
                         2:'-',
                         3:'-',
                         4:'-',
                         5:'-',
                         6:'-',
                         7:'-',
                         8:'-',
                         9:'-',
                         10:'-',
                         11:'-'
                         }
        
        self.default_dict = {
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
                         13:os.path.abspath('Data.csv')
                         }
        self.LoadPastState()
    
        #initailize all GUI components
        self.tab_control = System.Windows.Forms.TabControl()
        self.tabPage1 = System.Windows.Forms.TabPage()
        self.tabPage2 = System.Windows.Forms.TabPage()
            #declare tabPage1 Buttons
        self._btnForward = System.Windows.Forms.Button()
        self._btnBackward = System.Windows.Forms.Button()
        self._btnStrafeL = System.Windows.Forms.Button()
        self._btnStrafeR = System.Windows.Forms.Button()
        self._btnSurface = System.Windows.Forms.Button()
        self._btnSink = System.Windows.Forms.Button()
        self._btnRollL = System.Windows.Forms.Button()
        self._btnRollR = System.Windows.Forms.Button()
        self._btnLookUp = System.Windows.Forms.Button()
        self._btnLookDown = System.Windows.Forms.Button()
        self._btnLookL = System.Windows.Forms.Button()
        self._btnLookR = System.Windows.Forms.Button()
        self._btnDefault = System.Windows.Forms.Button()
        self._btnOK = System.Windows.Forms.Button()
        self._btnApply = System.Windows.Forms.Button()
        self._btnCancel = System.Windows.Forms.Button()
            #declare tabPage1 textboxes
        self._txtbxForward = System.Windows.Forms.TextBox()
        self._txtbxBackward = System.Windows.Forms.TextBox()
        self._txtbxStrafeL = System.Windows.Forms.TextBox()
        self._txtbxStrafeR = System.Windows.Forms.TextBox()
        self._txtbxSurface = System.Windows.Forms.TextBox()
        self._txtbxSink = System.Windows.Forms.TextBox()
        self._txtbxRollL = System.Windows.Forms.TextBox()
        self._txtbxRollR = System.Windows.Forms.TextBox()
        self._txtbxLookUp = System.Windows.Forms.TextBox()
        self._txtbxLookDown = System.Windows.Forms.TextBox()
        self._txtbxLookL = System.Windows.Forms.TextBox()
        self._txtbxLookR = System.Windows.Forms.TextBox()
            #declare tabPage2 controls
        self._lblDataArchiving = System.Windows.Forms.Label()
        self._txtbxDataLocation = System.Windows.Forms.TextBox()
        self._btnDataSearch = System.Windows.Forms.Button()
        self._cbDataArchiving = System.Windows.Forms.CheckBox()
        
        #tabPage1
        self.tabPage1.Location = Point(4, 22)
        self.tabPage1.Name = "tabPage1"
        self.tabPage1.Padding = System.Windows.Forms.Padding(3)
        self.tabPage1.Size = Size(584, 252)
        self.tabPage1.TabIndex = 0
        self.tabPage1.Text = "Controls"
        self.tabPage1.UseVisualStyleBackColor = True
        
        #Button Forward
        self._btnForward.Text = 'Forward'
        self._btnForward.Location = Point(70,50)
        self._btnForward.Size = Size(100,23)
        self._btnForward.Click += System.EventHandler(self.InputButton_Pushed)
        #Textbox Forward
        self._txtbxForward.Text = self.input_key_dict[6].getKeyValue() #show value stored in Key_Map
        self._txtbxForward.Location = System.Drawing.Point(175,52)
        self._txtbxForward.Size = System.Drawing.Size(95,23)
        self._txtbxForward.TextAlign = System.Windows.Forms.HorizontalAlignment.Center
        self._txtbxForward.Tag = 6
        self._txtbxForward.ReadOnly = True

        #Button Backward
        self._btnBackward.Text = 'Backward'
        self._btnBackward.Location = System.Drawing.Point(305,50)
        self._btnBackward.Size = System.Drawing.Size(100,23)
        self._btnBackward.Click += System.EventHandler(self.InputButton_Pushed)
        #Textbox Backward
        self._txtbxBackward.Text = self.input_key_dict[7].getKeyValue() #show value stored in Key_Map
        self._txtbxBackward.Location = System.Drawing.Point(410,52)
        self._txtbxBackward.Size = System.Drawing.Size(95,23)
        self._txtbxBackward.TextAlign = System.Windows.Forms.HorizontalAlignment.Center
        self._txtbxBackward.Tag = 7
        self._txtbxBackward.ReadOnly = True

        #Button Strafe Left
        self._btnStrafeL.Text = 'Strafe Left'
        self._btnStrafeL.Location = System.Drawing.Point(70,75)
        self._btnStrafeL.Size = System.Drawing.Size(100,23)
        self._btnStrafeL.Click += System.EventHandler(self.InputButton_Pushed)
        #Textbox Strafe Left
        self._txtbxStrafeL.Text = self.input_key_dict[8].getKeyValue() #show value stored in Key_Map
        self._txtbxStrafeL.Location = System.Drawing.Point(175,75)
        self._txtbxStrafeL.Size = System.Drawing.Size(95,23)
        self._txtbxStrafeL.TextAlign = System.Windows.Forms.HorizontalAlignment.Center
        self._txtbxStrafeL.Tag = 8
        self._txtbxStrafeL.ReadOnly = True
        
        #Button Strafe Right
        self._btnStrafeR.Text = 'Strafe Right'
        self._btnStrafeR.Location = System.Drawing.Point(305,75)
        self._btnStrafeR.Size = System.Drawing.Size(100,23)
        self._btnStrafeR.Click += System.EventHandler(self.InputButton_Pushed)
        #Textbox Strafe Left
        self._txtbxStrafeR.Text = self.input_key_dict[9].getKeyValue() #show value stored in Key_Map
        self._txtbxStrafeR.Location = System.Drawing.Point(410,75)
        self._txtbxStrafeR.Size = System.Drawing.Size(95,23)
        self._txtbxStrafeR.TextAlign = System.Windows.Forms.HorizontalAlignment.Center
        self._txtbxStrafeR.Tag = 9
        self._txtbxStrafeR.ReadOnly = True
        
        #Button Surface
        self._btnSurface.Text = 'Surface'
        self._btnSurface.Location = System.Drawing.Point(70,100)
        self._btnSurface.Size = System.Drawing.Size(100,23)
        self._btnSurface.Click += System.EventHandler(self.InputButton_Pushed)
        #Textbox Surface
        self._txtbxSurface.Text = self.input_key_dict[10].getKeyValue() #show value stored in Key_Map
        self._txtbxSurface.Location = System.Drawing.Point(175,100)
        self._txtbxSurface.Size = System.Drawing.Size(95,23)
        self._txtbxSurface.TextAlign = System.Windows.Forms.HorizontalAlignment.Center
        self._txtbxSurface.Tag = 10
        self._txtbxSurface.ReadOnly = True
        
        #Button Sink
        self._btnSink.Text = 'Sink'
        self._btnSink.Location = System.Drawing.Point(305,100)
        self._btnSink.Size = System.Drawing.Size(100,23)
        self._btnSink.Click += System.EventHandler(self.InputButton_Pushed)
        #Textbox Sink
        self._txtbxSink.Text = self.input_key_dict[11].getKeyValue() #show value stored in Key_Map
        self._txtbxSink.Location = System.Drawing.Point(410,100)
        self._txtbxSink.Size = System.Drawing.Size(95,23)
        self._txtbxSink.TextAlign = System.Windows.Forms.HorizontalAlignment.Center
        self._txtbxSink.Tag = 11
        self._txtbxSink.ReadOnly = True
        
        #Button Roll Left
        self._btnRollL.Text = 'Roll Left'
        self._btnRollL.Location = System.Drawing.Point(70,125)
        self._btnRollL.Size = System.Drawing.Size(100,23)
        self._btnRollL.Click += System.EventHandler(self.InputButton_Pushed)
        #Textbox Roll Left
        self._txtbxRollL.Text = self.input_key_dict[1].getKeyValue() #show value stored in Key_Map
        self._txtbxRollL.Location = System.Drawing.Point(175,125)
        self._txtbxRollL.Size = System.Drawing.Size(95,23)
        self._txtbxRollL.TextAlign = System.Windows.Forms.HorizontalAlignment.Center
        self._txtbxRollL.Tag = 1
        self._txtbxRollL.ReadOnly = True

        #Button Roll Right
        self._btnRollR.Text = 'Roll Right'
        self._btnRollR.Location = System.Drawing.Point(305,125)
        self._btnRollR.Size = System.Drawing.Size(100,23)
        self._btnRollR.Click += System.EventHandler(self.InputButton_Pushed)
        #Textbox Roll Right
        self._txtbxRollR.Text = self.input_key_dict[0].getKeyValue() #show value stored in Key_Map
        self._txtbxRollR.Location = System.Drawing.Point(410,125)
        self._txtbxRollR.Size = System.Drawing.Size(95,23)
        self._txtbxRollR.TextAlign = System.Windows.Forms.HorizontalAlignment.Center
        self._txtbxRollR.Tag = 0
        self._txtbxRollR.ReadOnly = True

        #Button Look Up
        self._btnLookUp.Text = 'Look Up'
        self._btnLookUp.Location = System.Drawing.Point(70,150)
        self._btnLookUp.Size = System.Drawing.Size(100,23)
        self._btnLookUp.Click += System.EventHandler(self.InputButton_Pushed)
        #Textbox Look Up
        self._txtbxLookUp.Text = self.input_key_dict[3].getKeyValue() #show value stored in Key_Map
        self._txtbxLookUp.Location = System.Drawing.Point(175,150)
        self._txtbxLookUp.Size = System.Drawing.Size(95,23)
        self._txtbxLookUp.TextAlign = System.Windows.Forms.HorizontalAlignment.Center
        self._txtbxLookUp.Tag = 3
        self._txtbxLookUp.ReadOnly = True

        #Button Look Down
        self._btnLookDown.Text = 'Look Down'
        self._btnLookDown.Location = System.Drawing.Point(305,150)
        self._btnLookDown.Size = System.Drawing.Size(100,23)
        self._btnLookDown.Click += System.EventHandler(self.InputButton_Pushed)
        #Textbox Look Down
        self._txtbxLookDown.Text = self.input_key_dict[2].getKeyValue() #show value stored in Key_Map
        self._txtbxLookDown.Location = System.Drawing.Point(410,150)
        self._txtbxLookDown.Size = System.Drawing.Size(95,23)
        self._txtbxLookDown.TextAlign = System.Windows.Forms.HorizontalAlignment.Center
        self._txtbxLookDown.Tag = 2
        self._txtbxLookDown.ReadOnly = True

        #Button Look Left
        self._btnLookL.Text = 'Look Left'
        self._btnLookL.Location = System.Drawing.Point(70,175)
        self._btnLookL.Size = System.Drawing.Size(100,23)
        self._btnLookL.Click += System.EventHandler(self.InputButton_Pushed)
        #Textbox Look Left
        self._txtbxLookL.Text = self.input_key_dict[4].getKeyValue() #show value stored in Key_Map
        self._txtbxLookL.Location = System.Drawing.Point(175,175)
        self._txtbxLookL.Size = System.Drawing.Size(95,23)
        self._txtbxLookL.TextAlign = System.Windows.Forms.HorizontalAlignment.Center
        self._txtbxLookL.Tag = 4
        self._txtbxLookL.ReadOnly = True

        #Button Look Right
        self._btnLookR.Text = 'Look Right'
        self._btnLookR.Location = System.Drawing.Point(305,175)
        self._btnLookR.Size = System.Drawing.Size(100,23)
        self._btnLookR.Click += System.EventHandler(self.InputButton_Pushed)
        #Textbox Look Right
        self._txtbxLookR.Text = self.input_key_dict[5].getKeyValue() #show value stored in Key_Map
        self._txtbxLookR.Location = System.Drawing.Point(410,175)
        self._txtbxLookR.Size = System.Drawing.Size(95,23)
        self._txtbxLookR.TextAlign = System.Windows.Forms.HorizontalAlignment.Center
        self._txtbxLookR.Tag = 5
        self._txtbxLookR.ReadOnly = True
        
        #Button Default
        self._btnDefault.Text = "Default Controls"
        self._btnDefault.Location = System.Drawing.Point(500, 10)
        self._btnDefault.Size = System.Drawing.Size(80, 23)
        self._btnDefault.Click +=System.EventHandler(self.btnDefault_Pushed)
        
        #Button OK
        self._btnOK.Text = "Okay"
        self._btnOK.Size = System.Drawing.Size(75,23)
        self._btnOK.Location = System.Drawing.Point(350,310)
        self._btnOK.Click += System.EventHandler(self.btnOk_Pushed)
        
        #Button Apply
        self._btnApply.Text = "Apply"
        self._btnApply.Size = System.Drawing.Size(75,23)
        self._btnApply.Location = System.Drawing.Point(430,310)
        self._btnApply.Click += System.EventHandler(self.btnApply_Pushed)
        self._btnApply.Enabled = False
        
        #Button Cancel
        self._btnCancel.Text = "Cancel"
        self._btnCancel.Size = System.Drawing.Size(75,23)
        self._btnCancel.Location = System.Drawing.Point(510,310)
        self._btnCancel.Click += System.EventHandler(self.btnCancel_Pushed)
        
        #Radio Button Hold
        self.rbhold_increment = System.Windows.Forms.RadioButton()
        self.rbhold_increment.Text = "Hold Increment Keyboard"
        self.rbhold_increment.Location = System.Drawing.Point(175,10)
        self.rbhold_increment.Click += System.EventHandler(self.TypeChanged)
        
        #Radio Button Tap
        self.rbtap_increment = System.Windows.Forms.RadioButton()
        self.rbtap_increment.Text = "Tap Increment Keyboard"
        self.rbtap_increment.Location = System.Drawing.Point(15,10)
        self.rbtap_increment.Click += System.EventHandler(self.TypeChanged)
        
        if self.input_type == "tap":
            self.rbtap_increment.Checked = System.Windows.Forms.CheckState.Checked
        elif self.input_type == "hold":
            self.rbhold_increment.Checked = System.Windows.Forms.CheckState.Checked

        #ADD ALL tabPage1 CONTROLS!
        self.tabPage1.Controls.Add(self._btnForward)
        self.tabPage1.Controls.Add(self._btnBackward)
        self.tabPage1.Controls.Add(self._btnStrafeL)
        self.tabPage1.Controls.Add(self._btnStrafeR)
        self.tabPage1.Controls.Add(self._btnSurface)
        self.tabPage1.Controls.Add(self._btnSink)
        self.tabPage1.Controls.Add(self._btnRollL)
        self.tabPage1.Controls.Add(self._btnRollR)
        self.tabPage1.Controls.Add(self._btnLookUp)
        self.tabPage1.Controls.Add(self._btnLookDown)
        self.tabPage1.Controls.Add(self._btnLookL)
        self.tabPage1.Controls.Add(self._btnLookR)
        self.tabPage1.Controls.Add(self._txtbxForward)
        self.tabPage1.Controls.Add(self._txtbxBackward)
        self.tabPage1.Controls.Add(self._txtbxStrafeL)
        self.tabPage1.Controls.Add(self._txtbxStrafeR)
        self.tabPage1.Controls.Add(self._txtbxSurface)
        self.tabPage1.Controls.Add(self._txtbxSink)
        self.tabPage1.Controls.Add(self._txtbxRollL)
        self.tabPage1.Controls.Add(self._txtbxRollR)
        self.tabPage1.Controls.Add(self._txtbxLookUp)
        self.tabPage1.Controls.Add(self._txtbxLookDown)
        self.tabPage1.Controls.Add(self._txtbxLookL)
        self.tabPage1.Controls.Add(self._txtbxLookR)
        self.tabPage1.Controls.Add(self.rbhold_increment)
        self.tabPage1.Controls.Add(self.rbtap_increment)
        self.tabPage1.Controls.Add(self._btnDefault)
        #
        # 
        # tabPage2
        # 
        #
        
        #Label Data Archiving
        self._lblDataArchiving.Text = "Data Archiving Location:"
        self._lblDataArchiving.Location = System.Drawing.Point(15, 40)
        self._lblDataArchiving.Size = System.Drawing.Size(135, 13)
        #Textbox Data Archiving
        self._txtbxDataLocation.Text = self.data_archive_location
        self._txtbxDataLocation.Location = System.Drawing.Point(20, 60)
        self._txtbxDataLocation.Size = System.Drawing.Size(445, 20)
        self._txtbxDataLocation.TextChanged += System.EventHandler(self.txtDataLocation_TextChange)
        #Button Data Archiving
        self._btnDataSearch.Text = "Search"
        self._btnDataSearch.Location = System.Drawing.Point(470, 59)
        self._btnDataSearch.Size = System.Drawing.Size(100,23)
        self._btnDataSearch.Click += System.EventHandler(self.btnDataSearch_Pushed)
        #Checkbox Data Archiving
        self._cbDataArchiving.Text ='Use Data Arching'
        self._cbDataArchiving.Location = System.Drawing.Point(15,20)
        self._cbDataArchiving.Size = System.Drawing.Size(118, 17)
        self._cbDataArchiving.Checked = self.use_data_archiving
        self._cbDataArchiving.CheckedChanged += System.EventHandler(self.cbDataArchive_CheckChanged)
        
        
        self.tabPage2.Location = System.Drawing.Point(4, 22)
        self.tabPage2.Name = "tabPage2"
        self.tabPage2.Padding = System.Windows.Forms.Padding(3)
        self.tabPage2.Size = System.Drawing.Size(584, 252)
        self.tabPage2.TabIndex = 1
        self.tabPage2.Text = "Output"
        self.tabPage2.UseVisualStyleBackColor = True
        
        #Add all tabPage2 controls
        self.tabPage2.Controls.Add(self._cbDataArchiving)
        self.tabPage2.Controls.Add(self._lblDataArchiving)
        self.tabPage2.Controls.Add(self._txtbxDataLocation)
        self.tabPage2.Controls.Add(self._btnDataSearch)
        
        #tab controller
        self.tab_control.Controls.Add(self.tabPage1)
        self.tab_control.Controls.Add(self.tabPage2)
        self.tab_control.Dock = System.Windows.Forms.DockStyle.Top
        self.tab_control.KeyDown += KeyEventHandler(self.Key_Press_Event)
        self.tab_control.Location = System.Drawing.Point(0, 0)
        self.tab_control.Name = "tab_control"
        self.tab_control.SelectedIndex = self.tab_index
        self.tab_control.Size = System.Drawing.Size(592, 278)
        self.tab_control.TabIndex = 3

        #FORM
        self.ClientSize = System.Drawing.Size(600,345)
        self.Name = "Form"
        self.Locked = True
        self.Text = "Settings"
        self.Controls.Add(self.tab_control)
        self.Controls.Add(self._btnOK)
        self.Controls.Add(self._btnApply)
        self.Controls.Add(self._btnCancel)
        self.MinimumSize = self.Size
        self.MaximumSize = self.Size
        self.AcceptButton = self._btnOK
        self.CancelButton = self._btnCancel
        self.TopMost = True
        
    def txtDataLocation_TextChange(self, sender, args):
        self.new_data_archiving_location = self._txtbxDataLocation.Text
        if self.data_archive_location != self.new_data_archiving_location and self.new_data_archiving_location != "":
            self._btnApply.Enabled = True
        
    def Key_Press_Event(self, sender, args):
        if self.tab_control.SelectedIndex == 0:
            args.Handled = True
            if self.read:
                self.L.acquire()
                self.new_Value = str(args.KeyData)
                self.keyPressed = True
                self.L.release()
            
    def go(self, txtbx = System.Windows.Forms.TextBox, index = int()):
        while not self.keyPressed and not self.cancel_countdown:
            txtbx.Text = "Press Key... " + str(self.counter)[0]
            time.sleep(.1)  
            self.counter = self.counter - 1
            if self.counter == 9:
                break
        if self.keyPressed:
            txtbx.Text = self.new_Value
        else:
            if self.new_Dict[index] == '-':
                txtbx.Text = self.input_key_dict[index].getKeyValue()
            else:
                txtbx.Text = self.new_Dict[index]
        self.counter = 99
        self.new_Dict[index] = txtbx.Text
        self.keyPressed = False
        self.disableButtons(self.tabPage1, True, self)
        self.read = False
        self.cancel_countdown = False
        if self.areControlsDirty():
            self._btnApply.Enabled = True
        else:
            self._btnApply.Enabled = False
        
    def InputButton_Pushed(self, sender, args):
        self.ActiveControl = self.tab_control
        self.disableButtons(self.tabPage1, False, sender)
        if not self.read:
            self.thread_dict = {
                    "Roll Right":Thread(target = self.go, args=(self._txtbxRollR, 0)),
                    "Roll Left":Thread(target = self.go, args=(self._txtbxRollL, 1)),
                    "Look Down":Thread(target = self.go, args=(self._txtbxLookDown, 2)),
                    "Look Up":Thread(target = self.go, args=(self._txtbxLookUp, 3)),
                    "Look Left":Thread(target = self.go, args=(self._txtbxLookL, 4)),
                    "Look Right":Thread(target = self.go, args=(self._txtbxLookR, 5)),
                    "Forward":Thread(target = self.go, args=(self._txtbxForward, 6)),
                    "Backward":Thread(target = self.go, args=(self._txtbxBackward, 7)),
                    "Strafe Left":Thread(target = self.go, args=(self._txtbxStrafeL, 8)),
                    "Strafe Right":Thread(target = self.go, args=(self._txtbxStrafeR, 9)),
                    "Surface":Thread(target = self.go, args=(self._txtbxSurface, 10)),
                    "Sink":Thread(target = self.go, args=(self._txtbxSink, 11))
                    }
            
            t = self.thread_dict[sender.Text]
            t.setDaemon(1)
            t.start()
            self.read = True
        else:
            self.cancel_countdown = True
        
    def disableButtons(self, Parent_Control = System.Windows.Forms.Control, Enabled = bool(), exceptionButton = System.Windows.Forms.Button):
        for (i, control) in enumerate(Parent_Control.Controls):
            if control.GetType() == System.Windows.Forms.Button and control != exceptionButton:
                control.Enabled = Enabled
            if control.HasChildren:
                self.disableButtons(control, Enabled, exceptionButton)
                
    def btnDefault_Pushed(self, sender, args):
        self.new_Dict = self.default_dict
        for (i,control) in enumerate(self.tabPage1.Controls):
            if control.GetType() == System.Windows.Forms.TextBox:
                control.Text = self.default_dict[control.Tag]
        if self.areControlsDirty():
            self._btnApply.Enabled = True
        else:
            self._btnApply.Enabled = False
            
    def btnDataSearch_Pushed(self, sender, args):
        saveDialog = System.Windows.Forms.SaveFileDialog()
        saveDialog.Filter = "csv files (*.csv)|*.csv|All files(*.*)|*.*"
        saveDialog.FilterIndex = 1
        if saveDialog.ShowDialog(self) == System.Windows.Forms.DialogResult.OK:
            self._txtbxDataLocation.Text = saveDialog.FileName

    def cbDataArchive_CheckChanged(self, sender, args):
        self.new_use_data_archiving = sender.Checked
        self._btnApply.Enabled = True
        
    def UpdateChanges(self):
        self.gkey_map.setNewDictValues(self.new_Dict)
        
        if self.input_type != self.new_input_type and self.new_input_type != "":
            self.input_type = self.new_input_type
        if self.use_data_archiving != self.new_use_data_archiving:
            self.use_data_archiving = self.new_use_data_archiving
        if self.data_archive_location != self.new_data_archiving_location and self.new_data_archiving_location != "":
            self.data_archive_location = self.new_data_archiving_location
            if not os.path.exists(self.data_archive_location):
                f = open(self.data_archive_location, 'w')
                f.writelines("DateTime, WaterTemp, CaseTemp, Humdity, Depth")
                f.close()
            
        temp_dict = self.gkey_map.getAllDictValues()
        temp_dict[12] = self.input_type
        temp_dict[13] = self.data_archive_location
        temp_dict[14] = self.new_use_data_archiving
        f = open('config.swmr', 'w')
        cPickle.dump(temp_dict, f)
        f.close()
        
        if self.areControlsDirty():
            self._btnApply.Enabled = True
        else:
            self._btnApply.Enabled = False
        
    def btnOk_Pushed(self, sender, args):
        if self._btnApply.Enabled == True:
            self.UpdateChanges()
        self.Close()
        
    def btnApply_Pushed(self, sender, args):
        self.UpdateChanges()
        
    def btnCancel_Pushed(self, sender, args):
        if self.areControlsDirty():
            result = System.Windows.Forms.MessageBox.Show("Are you sure you wish to disregard changes?", 'Cancel?', System.Windows.Forms.MessageBoxButtons.YesNo)
            if result != System.Windows.Forms.DialogResult.Yes:
                return
        self.Close()
        
    def TypeChanged(self, sender, args):
        if self.rbhold_increment.Checked == True:
            self.new_input_type = 'hold'
        else:
            self.new_input_type = 'tap'
        self._btnApply.Enabled = True
        
    def getInputType(self):
        return self.input_type
    def getDataLocation(self):
        return self.data_archive_location
    def getUseDataArchiving(self):
        return self.use_data_archiving
    
    def LoadPastState(self):
        defaultfile = str()
        if sys.platform == 'win32' or 'cli':
            defaultfile = os.getcwd()+"\DefaultData.csv"
        else:
            defaultfile = os.getcwd()+"/DefaultData.csv"
        g = open('config.swmr', 'r')
        data = cPickle.load(g)
        self.input_type = data.pop(12, 'tap')
        self.new_input_type = self.input_type
        self.data_archive_location = data.pop(13, defaultfile)
        if not os.path.exists(self.data_archive_location):
            self.data_archive_location = defaultfile
        self.new_data_archiving_location = self.data_archive_location
        self.use_data_archiving = data.pop(14, False)
        
        self.new_use_data_archiving = self.use_data_archiving
        g.close()
        
    def areControlsDirty(self):
        for i in range(0,12):
            if self.new_Dict[i] != self.input_key_dict[i].getKeyValue() and self.new_Dict[i] != '-':
                return True
            if self.input_type != self.new_input_type:
                return True
            if self.data_archive_location != self.new_data_archiving_location:
                return True
            if self.use_data_archiving != self.new_use_data_archiving:
                return True
        return False
    