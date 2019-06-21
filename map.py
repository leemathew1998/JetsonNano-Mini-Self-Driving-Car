import urllib.request
import json
import serial
import pynmea2
import time

ser = serial.Serial("/dev/gps0",9600)
while True:
    line = ser.readline()
    line=str(line,encoding='utf-8')
    if line[:6] == '$GPGGA': 
        rmc = pynmea2.parse(line)
        print("Latitude:",float(rmc.lat)/100)
        print("Longitude:",float(rmc.lon)/100)
       # break

def map_detact(lng, lat):
    url="http://api.map.baidu.com/direction/v2/riding?origin=27.821536,113.106619&destination="+str(lat)+","+str(lng)+"&ak=FQZ4nfmp8I8G5XX2Vxz5xIyDiSd8iTaX"
    req = urllib.request.urlopen(url)
    jsons = req.read().decode('utf-8')
    jsons = json.loads(jsons)
    jsons = jsons['result']
    jsons = jsons['routes']
    jsons = jsons[0]
    jsons = jsons['steps']
    jsons = jsons[0]
    turn_type = 0
    
    ######
    # 0 = no return
    # 1 = left
    # 2 = right
    # 3 = stop
    # 4 = front
    # 5 = wrong echo
    if jsons['distance'] < 10:
        if jsons['turn_type'] == '右转':
            turn_type = 2
        elif jsons['turn_type'] == '左转':
            turn_type = 1
        elif jsons['turn_type'] == '直行':
            turn_type = 4
        elif jsons['turn_type'] == '':
            turn_type = 3
        else:
            turn_type = 5
        return turn_type, jsons['distance']

    else:
        return turn_type, jsons['distance']


#map_detact(lng=113.106585, lat=27.819086)
