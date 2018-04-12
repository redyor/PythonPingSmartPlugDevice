#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Anthony Tournier"
__version__ = "0.1.0"
__license__ = "MIT"

import requests
from requests.auth import HTTPBasicAuth
from xml.dom.minidom import parse, parseString
from slugify import slugify

username = "MSIAfterburner"
password = "17cc95b4017d496f82"
endpoint = "http://192.168.1.158:82/mahm"

r=requests.get(endpoint, auth=HTTPBasicAuth(username, password))

if r.status_code == 200:
    returnDatas = {}
    xmldoc = parseString(r.text.encode('utf-8'))
    #print(xmldoc)
    dataslist = xmldoc.getElementsByTagName('HardwareMonitorEntry')
    for s in dataslist:
        childs = s.childNodes
        #print(childs) 
        key = slugify(childs[0].firstChild.nodeValue)
        returnDatas[key] = childs[5].firstChild.nodeValue

    print(returnDatas)
else:
    print(r)
