#!/usr/bin/env python
#
# Ping script for Mining Rig
# Tested on HS 110  should work with  HS-100 as well but remove the wattage function 
#
import checking
import globalconfig as cfg
checking.checkrig(cfg.rig1['host'],cfg.rig1['plugip'])   
#checking.checkrig(cfg.rig2['host'],cfg.rig2['plugip']) either uncomment this line to check the second rig or create new file with same code    
