#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013 Setkeh Mkfr
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.  See COPYING for more details.

#Short Python Example for connecting to The Cgminer API
#Written By: setkeh <https://github.com/setkeh>
#Thanks to Jezzz for all his Support.
#NOTE: When adding a param with a pipe | in bash or ZSH you must wrap the arg in quotes
#E.G "pga|0"

import socket
import json
import sys
import datetime
from subprocess import Popen, PIPE
import requests

Data = datetime.datetime.now().strftime("%d/%m/%y as %H:%M")

def linesplit(socket):
    buffer = socket.recv(4096)
    done = False
    while not done:
        more = socket.recv(4096)
        if not more:
            done = True
        else:
            buffer = buffer+more
    if buffer:
        return buffer

def extract_json(api_ip, api_port, request):
    try:
    # Try the connection with the API
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((api_ip,int(api_port)))
    except:
        #Popen(['/usr/local/bin/telegram-send', 'Miner offline'])
        #sys.exit(1)
        print "Deu merda"
    
    s.send(json.dumps(request))
    
    response = linesplit(s)
    response = response.replace('\x00','')
    response = response.replace("\\", "\\\\")
    s.close()
    return response


# ********************************* Antminer S9 ********************************* #
antminer = extract_json('10.0.0.100', 4028, {'command':'stats'})
antminer = antminer[:220]+','+antminer[220:]
antminer = json.loads(antminer)

Max_Temp = antminer['STATS'][1]['temp_max']
Chip0_Temp = antminer['STATS'][1]['temp6']
Chip1_Temp = antminer['STATS'][1]['temp7']
Chip2_Temp = antminer['STATS'][1]['temp8']
Hash_Rate = antminer['STATS'][1]['GHS 5s']
Chip0_Hash_Rate = antminer['STATS'][1]['chain_rate6']
Chip1_Hash_Rate = antminer['STATS'][1]['chain_rate7']
Chip2_Hash_Rate = antminer['STATS'][1]['chain_rate8']

if  Hash_Rate < 10000:
    message = ('''A consulta na API da miner indicou que o Hasrate está em '''+str(Hash_Rate)+''' Hash\/s.
O hasrate em cada chip é:
    - Chip 0: '''+str(Chip0_Hash_Rate)+''';
    - Chip 1: '''+str(Chip1_Hash_Rate)+''';
    - Chip 2: '''+str(Chip2_Hash_Rate)+''';

Consulta realizada em '''+Data)
    Popen(['/usr/local/bin/telegram-send', message])

if  Max_Temp > 100:
    message = ('''A consulta na API da miner indicou que o a temperatura máxima está acima de 100ºC.
As temperaturas estão em: 
    - Chip 0: '''+str(Chip0_Temp)+''';
    - Chip 1: '''+str(Chip1_Temp)+''';
    - Chip 2: '''+str(Chip2_Temp)+'''.

Consulta realizada em '''+Data)
    Popen(['/usr/local/bin/telegram-send', message])

# ********************************* Rig0 ********************************* #
try:
    r = requests.get('http://10.0.0.102:42000/getstat')
    gtx460_Temp = r.json()['result'][0]['temperature']
    Rig_Hash_Rate = r.json()['result'][0]['speed_sps']
    
    if  gtx460_Temp > 80:
        message = ('''A consulta na API da rig0 indicou que o a temperatura máxima está acima de '''+gtx460_Temp+'''
    Consulta realizada em '''+Data)
        Popen(['/usr/local/bin/telegram-send', message])
except:
    message = ('''A consulta na API da rig0 indicou que a mineração na GTX460 está parada.
Consulta realizada em '''+Data)
    Popen(['/usr/local/bin/telegram-send', message])

sys.exit(0)













