import json
from websocket import create_connection
import sys
import re

# Data structures for measurements
room = {'id': 'room', 'temp': 20, 'return':20}
pump = {'id': 'pump', 'flow': 20, 'return': 20,'power':100,'units':50,'oil':20}
tank = {'id': 'tank', 'top': 20, 'bot': 20,'flow':100}
amb  = {'id': 'amb', 'out':9,'garage':5}
ctl  = {'id': 'ctl', 'state':'...', 'change':0}


# Set up with your private API key, and numeric feed identifier

API_KEY = u'YourAPIKeyHere'
URL = 'ws://api.cosm.com:8080'

ws = create_connection(URL)


request = {u'method':u'put',u'resource':u'/feeds/yourfeed##'}
headers = {u"X-ApiKey":API_KEY}
request[u'headers']=headers
datastreams = []
datastreams.append({'id':'room_temp','current_value':0})
datastreams.append({'id':'room_return','current_value':0})
datastreams.append({'id':'tank_flow','current_value':0})
datastreams.append({'id':'tank_top','current_value':0})
datastreams.append({'id':'tank_bot','current_value':0})
datastreams.append({'id':'pump_flow','current_value':0})
datastreams.append({'id':'pump_return','current_value':0})
datastreams.append({'id':'pump_power','current_value':0})
datastreams.append({'id':'pump_units','current_value':0})
datastreams.append({'id':'amb_ext','current_value':0})
datastreams.append({'id':'amb_garage','current_value':0})

request[u'body'] = {u'datastreams':datastreams}

while True:
  s = sys.stdin.readline()
  if not s:
    break
  lpc = re.split(" +",s)
  # Check for reading line
  if (re.match("[0-9]{6}",lpc[0])):
    try:
      tank['top']     = float(lpc[1])
      tank['bot']     = float(lpc[2])
      tank['flow']    = float(lpc[3])
      pump['flow']    = float(lpc[4])
      amb['out']      = float(lpc[5])
      pump['return']  = float(lpc[6])
      pump['oil']     = float(lpc[7])
      room['temp']    = float(lpc[8])
      room['return']  = float(lpc[9])
      amb['garage']   = float(lpc[10])
      # 11 is spare
      # 12 is :
      pump['power']   = float(lpc[13])
      pump['units']   = float(lpc[14])
      ctl['state']    = lpc[15]
      ctl['change']   = float(lpc[16])
    except:
      print "Unexpected: ", sys.exc_info()[0]
      print tank
      print pump
      print room
      print amb
      print ctl
      print lpc[11]
      print lpc[12]
      print lpc[13]
      break
    print pump
    request['body']['datastreams'][0]['current_value']=room['temp']
    request['body']['datastreams'][1]['current_value']=room['return']
    request['body']['datastreams'][2]['current_value']=tank['flow']
    request['body']['datastreams'][3]['current_value']=tank['top']
    request['body']['datastreams'][4]['current_value']=tank['bot']
    request['body']['datastreams'][5]['current_value']=pump['flow']
    request['body']['datastreams'][6]['current_value']=pump['return']
    request['body']['datastreams'][7]['current_value']=pump['power']
    request['body']['datastreams'][8]['current_value']=pump['units']
    request['body']['datastreams'][9]['current_value']=amb['out']
    request['body']['datastreams'][10]['current_value']=amb['garage']
    ws.send(json.dumps(request))
    #print request
ws.close()
