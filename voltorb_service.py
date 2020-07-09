#!/usr/bin/env python3

import os,subprocess,json,time

configFile="/etc/Voltorb/config"
batteryValuesFile="/etc/Voltorb/battery_values"
perfValuesFile="/etc/Voltorb/perf_values"
genValuesFile="/etc/Voltorb/gen_values"

def isOnBattery():
    out=subprocess.getoutput("acpi -b")
    out=out.split(" ")
        
    if out[2]=="Discharging,":
        return True
        
    else:
        return False

def applySettings(t):
    with open(t,"r") as f:
        a=f.readlines()
        val=json.loads(a[0])
        cmd="undervolt "+" --temp "+str(val["temp"])+" --core " +str(val["core"])+" --gpu "+str(val["gpu"])+" --cache "+str(val["cache"])+" --uncore "+str(val["uncore"])+ " --analogio "+str(val["analogio"])
        os.system(cmd)    

def profilesEnabled():
    with open(configFile,"r") as f:
        t=f.readlines()
        i=json.loads(t[0])
        return i["PROFILES_ENABLED"]

if profilesEnabled():
    prevState=isOnBattery()
    
    while True:
        if isOnBattery()!=prevState:
            if isOnBattery()==0:
                print("Voltorb: Switching to performance mode.")
                applySettings(perfValuesFile)
                    
            elif isOnBattery():
                print("Voltorb: Switching to battery mode.")
                applySettings(batteryValuesFile)
                    
        prevState=isOnBattery()
        time.sleep(10)

else:
    print("Voltorb service started.")
    applySettings(genValuesFile)
