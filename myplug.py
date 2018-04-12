#!/usr/bin/env python
#
# TP-Link Wi-Fi Smart Plug Protocol Client
# For use with TP-Link HS-100 or HS-110
#
# by Lubomir Stroetmann
# Copyright 2016 softScheck GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
import socket
import argparse
import json
import logging
import globalconfig as cfg
logging.basicConfig(filename=cfg.logfilename,level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
#import logging
#logging.basicConfig(filename='log-rig.txt',level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

version = 0.1

# Check if IP is valid
def validIP(ip):
	try:
		socket.inet_pton(socket.AF_INET, ip)
	except socket.error:
		parser.error("Invalid IP Address.")
	return ip

# Predefined Smart Plug Commands
# For a full list of commands, consult tplink_commands.txt
commands = {'info'     : '{"system":{"get_sysinfo":{}}}',
			'on'       : '{"system":{"set_relay_state":{"state":1}}}',
			'off'      : '{"system":{"set_relay_state":{"state":0}}}',
			'cloudinfo': '{"cnCloud":{"get_info":{}}}',
			'wlanscan' : '{"netif":{"get_scaninfo":{"refresh":0}}}',
			'time'     : '{"time":{"get_time":{}}}',
			'schedule' : '{"schedule":{"get_rules":{}}}',
			'countdown': '{"count_down":{"get_rules":{}}}',
			'antitheft': '{"anti_theft":{"get_rules":{}}}',
			'reboot'   : '{"system":{"reboot":{"delay":1}}}',
			'reset'    : '{"system":{"reset":{"delay":1}}}',
			'stats'		: '{"emeter":{"get_realtime":{}}}'
}

# Encryption and Decryption of TP-Link Smart Home Protocol
# XOR Autokey Cipher with starting key = 171
def encrypt(string):
    key = 171
    result = b"\0\0\0"+ chr(len(string)).encode('latin-1')
    for i in string.encode('latin-1'):
        a = key ^ i
        key = a
        result += chr(a).encode('latin-1')
    return result


def decrypt(string):
    key = 171
    result = ""
    for i in string:
        a = key ^ i
        key = i
        result += chr(a)
    return result

# Parse commandline arguments
# parser = argparse.ArgumentParser(description="TP-Link Wi-Fi Smart Plug Client v" + str(version))
# parser.add_argument("-t", "--target", metavar="<ip>", required=True, help="Target IP Address", type=validIP)
# group = parser.add_mutually_exclusive_group(required=True)
# group.add_argument("-c", "--command", metavar="<command>", help="Preset command to send. Choices are: "+", ".join(commands), choices=commands)
# group.add_argument("-j", "--json", metavar="<JSON string>", help="Full JSON string of command to send")
# args = parser.parse_args()

# Set target IP, port and command to send
#ip = "192.168.1.138"
port = 9999
#if args.command is None:
#	cmd = args.json
#else:
#	cmd = commands[args.command]
#
def getplugstats(ip):
        result = docommand("stats",ip)
        power = str( result['emeter']['get_realtime']['power'])
        print ("Power : ", power)
        #logging.info('Current Wattage' + power )
        return power


# Send Command to plug 
def docommand(command, ip):
        cmd = commands[command]
        # Send command and receive reply
        try:
                sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock_tcp.connect((ip, port))
                sock_tcp.send(encrypt(cmd))
                data = sock_tcp.recv(2048)
                sock_tcp.close()

                print ("Sent:     ", cmd)
                print ("Received: ", decrypt(data[4:]))
                response = decrypt(data[4:])
                result =  json.loads(response)
                return result        
        except socket.error:
                logging.error("Cound not connect to host " + ip + ":" + str(port))
                quit("Cound not connect to host " + ip + ":" + str(port))
                