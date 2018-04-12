import time
import subprocess
import os
import myplug
import logging
import send_email
import globalconfig as cfg
logging.basicConfig(filename=cfg.logfilename,level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# Windows' ping returns  1 on success and 0 on failure, so we need to not the result.
# If you want to suppress ping's output, simply add > NUL to the command
def ping(address):
    return not os.system('ping %s -n 1' % (address,))

def checkrig(ip,plugip):
    # if ping is not successfull 
    if ping(ip) == 0:
        print("Offline we need to turn off and back on the switch")
        #Below goes the off and on
        myplug.docommand("off",plugip)
        time.sleep(3) # wait 3 seconds
        
        myplug.docommand("on",plugip)
        #Send email notification and write to log
        logging.error('Ping Failed! We had to restart the rig')
        send_email.sendemailreport("ERROR Rig Dead!!!")
    # if ping successfull 
    else:
        wattage = myplug.getplugstats(plugip)
        print("Online Do Nothing!!")
        # Write to log the rig is on
        logging.info('Ping successfull! Power Usage :' + wattage + " Watts ")
        send_email.sendemailreport("Power Usage : " + wattage + " Watts ")
