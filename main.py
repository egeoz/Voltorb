#!/usr/bin/env python3

from PyQt5 import QtWidgets,QtGui, uic
import sys,subprocess,os,threading,json

configFile="/etc/Voltorb/config"
batteryValuesFile="/etc/Voltorb/battery_values"
perfValuesFile="/etc/Voltorb/perf_values"
genValuesFile="/etc/Voltorb/gen_values"

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("/etc/Voltorb/MainWindow.ui", self)
        
        self.btnApply=self.findChild(QtWidgets.QPushButton,"btnApply")
        self.btnOK=self.findChild(QtWidgets.QPushButton,"btnOK")
        self.btnReset=self.findChild(QtWidgets.QPushButton,"btnReset")
    
    
        self.lblTemp=self.findChild(QtWidgets.QLabel,"lblTemp")
    
    
        self.checkBoxProfile=self.findChild(QtWidgets.QCheckBox,"checkBoxProfile")
        self.btnSave=self.findChild(QtWidgets.QPushButton,"btnSave")
    
        
        self.tabWidget=self.findChild(QtWidgets.QTabWidget,"tabWidget")
        
        self.txtTemp=self.findChild(QtWidgets.QLineEdit,"txtTemp")
        self.txtCore=self.findChild(QtWidgets.QLineEdit,"txtCore")
        self.txtGPU=self.findChild(QtWidgets.QLineEdit,"txtGPU")
        self.txtCache=self.findChild(QtWidgets.QLineEdit,"txtCache")
        self.txtUncore=self.findChild(QtWidgets.QLineEdit,"txtUncore")
        self.txtAna=self.findChild(QtWidgets.QLineEdit,"txtAna")
        
        self.txtTemp_2=self.findChild(QtWidgets.QLineEdit,"txtTemp_2")
        self.txtCore_2=self.findChild(QtWidgets.QLineEdit,"txtCore_2")
        self.txtGPU_2=self.findChild(QtWidgets.QLineEdit,"txtGPU_2")
        self.txtCache_2=self.findChild(QtWidgets.QLineEdit,"txtCache_2")
        self.txtUncore_2=self.findChild(QtWidgets.QLineEdit,"txtUncore_2")
        self.txtAna_2=self.findChild(QtWidgets.QLineEdit,"txtAna_2")
        
        self.txtTemp_3=self.findChild(QtWidgets.QLineEdit,"txtTemp_3")
        self.txtCore_3=self.findChild(QtWidgets.QLineEdit,"txtCore_3")
        self.txtGPU_3=self.findChild(QtWidgets.QLineEdit,"txtGPU_3")
        self.txtCache_3=self.findChild(QtWidgets.QLineEdit,"txtCache_3")
        self.txtUncore_3=self.findChild(QtWidgets.QLineEdit,"txtUncore_3")
        self.txtAna_3=self.findChild(QtWidgets.QLineEdit,"txtAna_3")
        
        
        self.actionExit=self.findChild(QtWidgets.QAction,"actionExit")
        self.actionRefresh=self.findChild(QtWidgets.QAction,"actionRefresh")
        self.actionAbout=self.findChild(QtWidgets.QAction,"actionAbout")
        
        
        self.checkBoxProfile.toggled.connect(self.checkBoxProfile_Toggled)
        self.btnSave.clicked.connect(self.btnSave_Clicked)
        
        self.btnApply.clicked.connect(self.btnApply_Clicked)
        self.btnOK.clicked.connect(self.btnOK_Clicked)
        self.btnReset.clicked.connect(self.btnReset_Clicked)
        
        self.actionExit.triggered.connect(self.actionExit_Triggered)
        self.actionRefresh.triggered.connect(self.actionRefresh_Triggered)
        self.actionAbout.triggered.connect(self.actionAbout_Triggered)
        
        self.setWindowIcon(QtGui.QIcon("/etc/Voltorb/icon.png"))
        
        self.show()
    
    def notRoot(self):
        QtWidgets.QMessageBox.warning(self,"Error","This program requires to be run as root!")
        sys.exit()
    
    def noUndervolt(self):
        QtWidgets.QMessageBox.warning(self,"Error","Cannot find the undervolt binary, is it instaled correctly?")
        sys.exit()

    def isOnBattery(self):
        out=subprocess.getoutput("acpi -b")
        out=out.split(" ")
        
        if out[2]=="Discharging,":
            return True
        
        else:
            return False
    
    def profilesEnabled(self):
        with open(configFile,"r") as f:
            t=f.readlines()
            i=json.loads(t[0])
            return i["PROFILES_ENABLED"]
    
    def setProfilesEnabled(self,b):
        config={"PROFILES_ENABLED":b}
        with open(configFile,"w") as f:
            f.write(json.dumps(config))
            
    def readValues(self,t):
        empty={"temp":"0.0","core":"0.0","gpu":"0.0","cache":"0.0","uncore":"0.0","analogio":"0.0"}
        if t==0:
            if os.path.isfile(genValuesFile):
                with open(genValuesFile,"r") as f:
                    a=f.readlines()
                    i=json.loads(a[0])
                    return i
            else:
                return empty
            
        elif t==1:
            if os.path.isfile(batteryValuesFile):
                with open(batteryValuesFile,"r") as f:
                    a=f.readlines()
                    i=json.loads(a[0])
                    return i
            else:
                return empty
        
        elif t==2:
            if os.path.isfile(perfValuesFile):
                with open(perfValuesFile,"r") as f:
                    a=f.readlines()
                    i=json.loads(a[0])
                    return i 
            else:
                return empty
        
    def loadValues(self):
        out=subprocess.getoutput("undervolt --read")
        t=out.splitlines()
    
        for i in range(len(t)):
            t[i]=(t[i].split(":"))[1]

        temp=(t[0].split(" "))[1]
        core=(t[1].split(" "))[1]
        gpu=(t[2].split(" "))[1]
        cache=(t[3].split(" "))[1]
        uncore=(t[4].split(" "))[1]
        analogio=(t[5].split(" "))[1]
        
        with open("/sys/class/thermal/thermal_zone0/temp","r") as f:
            currentTemp=f.readlines()
            currentTemp=str(int(currentTemp[0])/1000)
        
        self.lblTemp.setText(currentTemp+" °C")
        
        if self.profilesEnabled():
            self.checkBoxProfile.setChecked(True)
            if self.isOnBattery():
                self.txtTemp_2.setText(temp)
                self.txtCore_2.setText(core)
                self.txtGPU_2.setText(gpu)
                self.txtCache_2.setText(cache)
                self.txtUncore_2.setText(uncore)
                self.txtAna_2.setText(analogio)                
                
                self.setValues(2,self.readValues(2))
                
            else:
                self.txtTemp_3.setText(temp)
                self.txtCore_3.setText(core)
                self.txtGPU_3.setText(gpu)
                self.txtCache_3.setText(cache)
                self.txtUncore_3.setText(uncore)
                self.txtAna_3.setText(analogio)                
            
                self.setValues(1,self.readValues(1))                
                
        else:
            self.checkBoxProfile.setChecked(False)
            self.tabWidget.setTabEnabled(0,True)
            self.tabWidget.setTabEnabled(1,False)
            self.tabWidget.setTabEnabled(2,False)
            self.txtTemp.setText(temp)
            self.txtCore.setText(core)
            self.txtGPU.setText(gpu)
            self.txtCache.setText(cache)
            self.txtUncore.setText(uncore)
            self.txtAna.setText(analogio)             

    def setValues(self,t,values):
        if t==0:
            self.txtTemp.setText(str(values["temp"]))
            self.txtCore.setText(str(values["core"]))
            self.txtGPU.setText(str(values["gpu"]))
            self.txtCache.setText(str(values["cache"]))
            self.txtUncore.setText(str(values["uncore"]))
            self.txtAna.setText(str(values["analogio"]))
            
        elif t==1:
            self.txtTemp_2.setText(str(values["temp"]))
            self.txtCore_2.setText(str(values["core"]))
            self.txtGPU_2.setText(str(values["gpu"]))
            self.txtCache_2.setText(str(values["cache"]))
            self.txtUncore_2.setText(str(values["uncore"]))
            self.txtAna_2.setText(str(values["analogio"]))            
            
        elif t==2:
            self.txtTemp_3.setText(str(values["temp"]))
            self.txtCore_3.setText(str(values["core"]))
            self.txtGPU_3.setText(str(values["gpu"]))
            self.txtCache_3.setText(str(values["cache"]))
            self.txtUncore_3.setText(str(values["uncore"]))
            self.txtAna_3.setText(str(values["analogio"]))
            
    
    def getValues(self,t):
        if t==0: # General mode
            temp=int(float(self.txtTemp.text()))
            core=int(float(self.txtCore.text()))
            gpu=int(float(self.txtGPU.text()))
            cache=int(float(self.txtCache.text()))
            uncore=int(float(self.txtUncore.text()))
            analogio=int(float(self.txtAna.text()))
        
        elif t==1: # Battery mode
            temp=int(float(self.txtTemp_2.text()))
            core=int(float(self.txtCore_2.text()))
            gpu=int(float(self.txtGPU_2.text()))
            cache=int(float(self.txtCache_2.text()))
            uncore=int(float(self.txtUncore_2.text()))
            analogio=int(float(self.txtAna_2.text()))            
        
        elif t==2: # Performance mode
            temp=int(float(self.txtTemp_3.text()))
            core=int(float(self.txtCore_3.text()))
            gpu=int(float(self.txtGPU_3.text()))
            cache=int(float(self.txtCache_3.text()))
            uncore=int(float(self.txtUncore_3.text()))
            analogio=int(float(self.txtAna_3.text()))            
    
        values={"temp":temp,"core":core,"gpu":gpu,"cache":cache,"uncore":uncore,"analogio":analogio}
        
        return values
        
    def runCommand(self,save,t):
        cmd=""
        
        if t==0:
            val=self.getValues(0)
            cmd="undervolt "+" --temp "+str(val["temp"])+" --core " +str(val["core"])+" --gpu "+str(val["gpu"])+" --cache "+str(val["cache"])+" --uncore "+str(val["uncore"])+ " --analogio "+str(val["analogio"])
            
            if save:
                self.setProfilesEnabled(0)
                self.writeServiceFile(val,0)

        elif t==1:
            valBat=self.getValues(1)
            valPerf=self.getValues(2)
            
            if self.isOnBattery():
                cmd="undervolt "+" --temp "+str(valBat["temp"])+" --core " +str(valBat["core"])+" --gpu "+str(valBat["gpu"])+" --cache "+str(valBat["cache"])+" --uncore "+str(valBat["uncore"])+ " --analogio "+str(valBat["analogio"])
                
            else:
                cmd="undervolt "+" --temp "+str(valPerf["temp"])+" --core " +str(valPerf["core"])+" --gpu "+str(valPerf["gpu"])+" --cache "+str(valPerf["cache"])+" --uncore "+str(valPerf["uncore"])+ " --analogio "+str(valPerf["analogio"])    
            
            if save:
                self.setProfilesEnabled(1)
                self.writeServiceFile(valBat,1)
                self.writeServiceFile(valPerf,2)
        
        print("Executing: "+cmd)
        
        if os.system(cmd)!=0:
            self.statusBar().showMessage("Error applying settings")
        else:
            self.statusBar().showMessage("Successfully applied the new settings.")

        self.loadValues()
    
    def confirm(self):
        return QtWidgets.QMessageBox.question(self,"Proceed?","Undervolting can cause your system to crash! Make sure to save your data before proceeding.",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    
    def writeServiceFile(self,values,t):
        if t==0: # General mode
            with open(genValuesFile,"w") as f:
                f.write(json.dumps(values))
                
        elif t==1: # Battery mode
            with open(batteryValuesFile,"w") as f:
                f.write(json.dumps(values))
        
        elif t==2: # Performance mode
            with open(perfValuesFile,"w") as f:
                f.write(json.dumps(values))            
            
        self.statusBar().showMessage("Values are successfully saved.")
     
    def btnSave_Clicked(self):
        if self.checkBoxProfile.isChecked():
            self.setProfilesEnabled(1)
            self.writeServiceFile(self.getValues(1),1)
            self.writeServiceFile(self.getValues(2),2)
            
        else:
            self.setProfilesEnabled(0)
            self.writeServiceFile(self.getValues(0),0)
                
    def checkBoxProfile_Toggled(self):
        if self.checkBoxProfile.isChecked():
            self.tabWidget.setTabEnabled(0,False)
            self.tabWidget.setTabEnabled(1,True)
            self.tabWidget.setTabEnabled(2,True)
            self.setValues(1,self.readValues(1))
            self.setValues(2,self.readValues(2))
            self.statusBar().showMessage("Profiles enabled.")
        
        else:
            self.tabWidget.setTabEnabled(0,True)
            self.tabWidget.setTabEnabled(1,False)
            self.tabWidget.setTabEnabled(2,False)
            self.setValues(0,self.readValues(0))
            self.statusBar().showMessage("Profiles disabled.")
    
    def btnApply_Clicked(self):
        if self.confirm()==QtWidgets.QMessageBox.Yes:
            if self.checkBoxProfile.isChecked():
                self.runCommand(False,1)
                
            else:
                self.runCommand(False,0)
    
    def btnOK_Clicked(self):
        if self.confirm()==QtWidgets.QMessageBox.Yes:
            if self.checkBoxProfile.isChecked():
                self.runCommand(True,1)
                
            else:
                self.runCommand(True,0)
                
            os.system("systemctl disable voltorb.service --now &")
            os.system("systemctl enable voltorb.service --now &")
            self.statusBar().showMessage("Enabled Voltorb service")
        
    def btnReset_Clicked(self):
        self.txtTemp.setText("0.0")
        self.txtCore.setText("0.0")
        self.txtGPU.setText("0.0")
        self.txtCache.setText("0.0")
        self.txtUncore.setText("0.0")
        self.txtAna.setText("0.0")

        self.txtTemp_2.setText("0.0")
        self.txtCore_2.setText("0.0")
        self.txtGPU_2.setText("0.0")
        self.txtCache_2.setText("0.0")
        self.txtUncore_2.setText("0.0")
        self.txtAna_2.setText("0.0")
        
        self.txtTemp_3.setText("0.0")
        self.txtCore_3.setText("0.0")
        self.txtGPU_3.setText("0.0")
        self.txtCache_3.setText("0.0")
        self.txtUncore_3.setText("0.0")
        self.txtAna_3.setText("0.0")
        
        self.runCommand(True,0)
        self.runCommand(True,1)
        os.system("systemctl disable voltorb.service --now &")
        self.statusBar().showMessage("Values are reset to 0.0.")
    
    def actionRefresh_Triggered(self):
        self.loadValues()
        
    def actionExit_Triggered(self):
        sys.exit()
    
    def actionAbout_Triggered(self):
        QtWidgets.QMessageBox.about(self, "About Voltorb", "Voltorb is a graphical utility that makes undervolting easy on Intel Haswell and newer processors.")
    

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    
    if os.geteuid() != 0:
        window.notRoot()
    
    try:
        subprocess.call("undervolt")
    except OSError:
        window.noUndervolt()
    
    window.loadValues()
    app.exec_()

if __name__ == '__main__':        
    main()
