import time
import subprocess
import os
import myplug
import logging
import send_email
import globalconfig as cfg
logging.basicConfig(filename=cfg.logfilename, level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# Just a comment Windows' ping returns  1 on success and 0 on failure, so we need to not the result.
# If you want to suppress ping's output, simply add > NUL to the command


def ping(address):
    return not os.system('ping %s -n 1' % (address,))


def checkrig(ip, plugip):
    # if ping is not successfull
    if ping(ip) == 0:
        print("Offline we need to turn off and back on the switch")
        # Send email notification and write to log
        restart(plugip)
        logging.error('Ping Failed! We had to restart the rig')
        send_email.sendemailreport("ERROR Rig Dead!!!")
    # if ping successfull
    else:
        wattage = myplug.getplugstats(plugip)
        print("Online Do Nothing!!")
        # Write to log the rig is on
        logging.info('Ping successfull! Power Usage :' + wattage + " Watts ")
        send_email.sendemailreport("Power Usage : " + wattage + " Watts ")


def restart(plugip, waitsec=3):
    # Below goes the off and on
    logging.error('We restart the plug ' + plugip + '!!!! ')
    myplug.docommand("off", plugip)
    time.sleep(waitsec)  # wait x seconds
    myplug.docommand("on", plugip)


def checkrigWattage(plugip, minwatt=200, waittime=120, retry=3, debug=False):
    # samplewattage = int(169.82486)  # no needs for a float converting to int
    samplewattage = myplug.getplugstats(plugip)
    wattage = int(float(samplewattage))

    logging.info('Reporting Current Power ' + str(wattage) +
                 " Min Power " + str(minwatt) + " Wait Time in Secs " + str(waittime))

    # retry = 2  # number of time to check before forcing restarting
    i = 1
    while i <= retry:
        if (wattage < minwatt):
            logging.info("The rig power is below : " + str(minwatt) +
                         " we will retry " + str(retry) + " time(s) in " + str(waittime) + " secs ")
            time.sleep(waittime)
            logging.info("Attempt #:" + str(i) + " Time: " +
                         str(waittime)+' sec later')
            if i == (retry - 1):
                if (debug):
                    logging.info("Debug is On Do nothing!")
                else:
                    logging.info("We tried" + str(i) +
                                 "times need to reboot the rig")
                    restart(plugip, waitsec=3)
                break
            i += 1
        else:
            logging.info("All is good nothing to do! Bye")
            break
