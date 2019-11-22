#!/usr/bin/env python
#
# Ping script for Mining Rig
# Tested on HS 110  should work with  HS-100 as well but remove the wattage function
#
import getopt
import sys
import checking
import globalconfig as cfg
import logging
import send_email
logging.basicConfig(filename=cfg.logfilename, level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


def printHelp():
    print("---------------------------------------------------------------")
    print("-  Command Options:                                           -")
    print("-  ================                                           -")
    print("-                                                             -")
    print("- -h or --help for this help menu                             -")
    print("- -r or --restart <RigName> restart by RigName in config file -")
    print("- -ip <ip> or --addr Reboot by Ip                             -")
    print("-                                                             -")
    print("---------------------------------------------------------------")


fullCmdArguments = sys.argv
# - further arguments
argumentList = fullCmdArguments[1:]

if not argumentList:
    printHelp()
unixOptions = "hr:p:"
gnuOptions = ["help", "restart=", "addr="]
try:
    arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
except getopt.error as err:
    # output error, and return with an error code
    print(str(err))
    sys.exit(2)

# evaluate given options
for currentArgument, currentValue in arguments:
    if currentArgument in ("-p", "--addr"):
        print("By IP Address mode" + currentValue)
        checking.restart(currentValue, waitsec=1)
    elif currentArgument in ("-h", "--help"):
        printHelp()
    elif currentArgument in ("-r", "--restart"):
        #print(("enabling special output mode (%s)") % (currentValue))
        for k, v in cfg.__dict__.items():
            if isinstance(v, dict) and not k.startswith('_'):
                if k == currentValue:
                    print("found it from -r value" + v['plugip'])
                    checking.restart(v['plugip'], waitsec=1)
                else:
                    print(" Rig Not Found! Sorry!")
