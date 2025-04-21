#apply it later 
import time
import subprocess
import os

script_Line="/home/pi/nourta3deelmpu2.py"
script_Evac="/home/pi/VL53L0X_rasp_python/python/evacuation.py"
switch_file="/tmp/switch_script"

current_script = "Line"
process = subprocess.Popen(["python3",script_Line])

#to be written in Line code and Evac code on event and to be executed once
#########################################
# with open("/tmp/switch_script","w") as f:
#    f.write("switch") *executed when seen silver or black, general function: automate the button*
##########################################
while True:
    if os.path.exists(switch_file):
        os.remove(switch_file)
        process.terminate()
        process.wait()    
        if current_script == "Line":
            process = subprocess.run(["python3","evacuation.py"],cwd="/home/pi/VL53L0X_rasp_python/python/")
            current_script = "Evac"
        else:
            process = subprocess.Popen(["python3",script_Line])

            current_script = "Line"
