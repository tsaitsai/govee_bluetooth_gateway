#!/usr/bin/python
'''
This is a python Bluetooth advertisement scanner for the Govee brand Bluetooth
temperature sensor.  Tested on model H5075 using Raspberry Pi 3.
Temperature, humidity, and battery level is published as MQTT messages.

Credit:  I used information for Govee advertisement format from
github.com/Thrilleratplay/GoveeWatcher

Install dependencies:
 sudo apt-get install python3-pip libglib2.0-dev
 sudo pip3 install bluepy
 sudo apt install -y mosquitto mosquitto-clients
 sudo pip3 install paho-mqtt

Needs sudo to run on Raspbian
sudo python3 govee_ble_mqtt_pi.py

Run in background
sudo nohup python3 govee_ble_mqtt_pi.py &

'''

from __future__ import print_function

from time import gmtime, strftime, sleep
from bluepy.btle import Scanner, DefaultDelegate, BTLEException
import sys
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_message(client, userdata, msg):
    print("on message")
    
client = mqtt.Client()
mqtt_prefix = "/sensor/govee"
mqtt_gateway_name = "/upstairs/"

class ScanDelegate(DefaultDelegate):
    
    global client
    # mqtt message topic/payload:  /prefix/gateway_name/mac/
    global mqtt_prefix
    global mqtt_gateway_name
    
    def handleDiscovery(self, dev, isNewDev, isNewData):
        #if (dev.addr == "a4:c1:38:xx:xx:xx") or (dev.addr == "a4:c1:38:xx:xx:xx"):
        if dev.addr[:8]=="a4:c1:38":          
            
            #returns a list, of which the [2] item of the [3] tupple is manufacturing data
            adv_list = dev.getScanData()
            
            adv_manuf_data = adv_list[2][2]
            
            #print("manuf data = ", adv_manuf_data)

            #this is the location of the encoded temp/humidity and battery data
            temp_hum_data = adv_manuf_data[6:12]
            battery = adv_manuf_data[12:14]
            
            #convert to integer
            val = (int(temp_hum_data, 16))

            #decode tip from eharris: https://github.com/Thrilleratplay/GoveeWatcher/issues/2
            is_negative = False
            temp_C = 500
            humidity = 500
            if (val & 0x800000):
                is_negative = True
                val = val ^ 0x800000
            try:
                humidity = (val % 1000) / 10
                temp_C = int(val / 1000) / 10
                if (is_negative):
                    temp_C = 0 - temp_C
            except:
                print("issues with integer conversion")

            try:
                battery_percent = int(adv_manuf_data[12:14]) / 64 * 100
            except:
                battery_percent = 200
            battery_percent = round(battery_percent)

            temp_F = round(temp_C*9/5+32, 1)

            try:
                hum_percent = ((int(temp_hum_data, 16)) % 1000) / 10
            except:
                hum_percent = 200
            hum_percent = round(hum_percent)
            mac=dev.addr
            signal = dev.rssi

            #print("mac=", mac, "   percent humidity ", hum_percent, "   temp_F = ", temp_F, "   battery percent=", battery_percent, "  rssi=", signal)
            mqtt_topic = mqtt_prefix + mqtt_gateway_name + mac + "/"

            client.publish(mqtt_topic+"rssi", signal, qos=0)
            client.publish(mqtt_topic+"temp_F", temp_F, qos=0)
            client.publish(mqtt_topic+"hum", hum_percent, qos=0)
            client.publish(mqtt_topic+"battery_pct", battery_percent, qos=0)
            
            sys.stdout.flush()

scanner = Scanner().withDelegate(ScanDelegate())

#replace localhost with your MQTT broker
client.connect("localhost",1883,60)

client.on_connect = on_connect
client.on_message = on_message

while True:
    scanner.scan(60.0, passive=True)

