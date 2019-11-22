#!/usr/bin/env python
#
# Ping script for Mining Rig
# Tested on HS 110  should work with  HS-100 as well but remove the wattage function
#

import sys
import checking
import globalconfig as cfg
print(type(cfg.rig1['plugip']))
checking.checkrigWattage(
    cfg.rig1['plugip'], minwatt=200, waittime=10, retry=2, debug=False)
# checking.checkrig(cfg.rig2['host'],cfg.rig2['plugip']) either uncomment this line to check the second rig or create new file with same code
