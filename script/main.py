import time
import gc
gc.collect()
from machine import Pin, Timer, UART, WDT
gc.collect()
from network import LoRa, WLAN
gc.collect()
from mqtt import MQTTClient
gc.collect()
import socket
gc.collect()
import binascii
gc.collect()
import struct
gc.collect()
import config
gc.collect()
import machine
gc.collect()
import network
gc.collect()
import ubinascii
gc.collect()
from dth import DTH
gc.collect()
from math import log
gc.collect()
from network import LoRa
gc.collect()
from struct import unpack
gc.collect()
import pms5003
gc.collect()
import am2302
gc.collect()
import urequests
gc.collect()
from machine import I2C
gc.collect()
from bh1750 import BH1750
gc.collect()
# Enable automatic garbage collection:
gc.enable()

"""
SETUP FOR WIFI:
"""

"""
SETUP FOR LORA:
"""

lora = LoRa(mode=LoRa.LORAWAN)
# create  ABP authentication parameters
dev_addr = struct.unpack(">l", binascii.unhexlify(config.DEV_ADDR_kpn))[0]
nwk_swkey = binascii.unhexlify(config.NWKS_KEY_kpn)
app_swkey = binascii.unhexlify(config.APPS_KEY_kpn)


# join a network using ABP (Activation By Personalization)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))
print("LoRa active: ",  lora.has_joined())
# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_CONFIRMED, False)

"""
SETUP FOR SENSORS:
"""


def aq(sleeping, sensor):
    pms5003.fan_on()
    time.sleep(sleeping)
    time.sleep(2)
    if sensor == 1:
        raw = pms5003.data_uart1.read()
    else:
        raw = pms5003.data_uart2.read()
    try:
        unpacking = unpack('>16H', raw)
        pm1_u = int(unpacking[2])
        pm2_u = int(unpacking[3])
        pm10_u = int(unpacking[4])
        pm1_atm_u = int(unpacking[5])
        pm2_atm_u = int(unpacking[6])
        pm10_atm_u = int(unpacking[7])
    except:
        print('No PMS data read... Try again...')
    pm1 = int(hex(pm1_u))
    pm2 = int(hex(pm2_u))
    pm10 = int(hex(pm10_u))
    pm1_atm = int(hex(pm1_atm_u))
    pm2_atm = int(hex(pm2_atm_u))
    pm10_atm = int(hex(pm10_atm_u))
    # print([pm1, pm2, pm10, pm1_atm, pm2_atm, pm10_atm])
    return(pm1, pm2, pm10, pm1_atm, pm2_atm, pm10_atm)


"""
FINAL loop for main.py
"""


def final(sleeping):
    """
    This is the final function, used for the outdoor measurements.
    The function uses one argument sleeping, which represents the interval between measurement cycles in seconds. 
    """
    x = 1
    while True:
        print("7d58. Round ", x)
        time.sleep(2)
        aq1 = aq(20, 1)
        aq2 = aq(20, 2)
        time.sleep(2)
        th1 = am2302.th1.read()
        th2 = am2302.th2.read()
        i2c_light = machine.I2C(0, pins=("P21", "P22"))
        lightsensor = BH1750(i2c_light)
        luminance = lightsensor.luminance(BH1750.ONCE_HIRES_1)
        time.sleep(2)
        print("Results: ")
        print("PMS5003 1:           ", aq1[0:3])
        print("PMS5003 2:           ", aq2[0:3])
        print("Temperature 1:       ", th1.temperature)
        print("Temperature 2:       ", th2.temperature)
        print("Humdity 1:           ", th1.humidity)
        print("Humdity 2:           ", th2.humidity)
        print("Light intensity:     ", luminance)
        gc.collect()
        time.sleep(sleeping)
        gc.collect()
        x += 1
    pms5003.fan_off()


def testlora():
    pm1 = int(hex(0))
    print(type(pm1))
    pm2 = int(hex(0))
    pm10 = int(hex(0))
    pm1_atm = int(hex(0))
    pm2_atm = int(hex(0))
    pm10_atm = int(hex(0))
    print("Sleep for a couple of seconds...")
    time.sleep(5)
    print("Set blocking...")
    s.setblocking(True)
    print("Sleep for a couple of seconds...")
    time.sleep(5)
    #print("Trying to send...")
#    s.send(bytes([pm1, pm2, pm10, pm1_atm, pm2_atm, pm10_atm]))
    print("Sending...")
    s.send(bytes([0x01, 0x02, 0x03]))
    print("Message sent!")
    time.sleep(5)
    print("Unblock..")
    s.setblocking(False)
    #s.setblocking(False)
    print("Done!")

"""
Internal filesystem storage:
"""

wdt = WDT(timeout=1800000)


def createfiles():
    """
    This method creates a new file.
    """
    f = open("data/data.csv", "w")
    f.write('record; sid; aq1_1; aq1_2; aq1_10; aq2_1; aq2_2; aq2_10; temp1; temp2; hum1; hum2; lum; timest; \n')
    f.close()


def start():
    createfiles()

	
BIGSLEEP = 800  # 800 seconds for 15 minutes intervals.
ROUND = 1
TICKER = 1


while True:
    f = open("data/data.csv", "a")
    print("862c. Round ", ROUND)
    time.sleep(2)
    insert_one_1 = aq(5, 1)
    insert_two_1 = aq(5, 2)
    time.sleep(2)
    temphum1 = am2302.th1.read()
    temphum2 = am2302.th2.read()
    i2c_light = machine.I2C(0, pins=("P21", "P22"))  # (P21 is SDA, P22 is clock)
    lightsensor = BH1750(i2c_light)
    luminance = lightsensor.luminance(BH1750.ONCE_HIRES_1)
    time.sleep(2)
    timesec = time.time()
    f.write(str(ROUND) + '; ' + str("862c") + '; ' + str(insert_one_1[0]) + '; ' + str(insert_one_1[1]) + '; ' + str(insert_one_1[2]) + '; ' + str(insert_two_1[0]) + '; ' + str(insert_two_1[1]) + '; ' + str(insert_two_1[2]) + '; ' + str(temphum1.temperature) + '; ' + str(temphum2.temperature) + '; ' + str(temphum1.humidity) + '; ' +  str(temphum2.humidity) + '; ' + str(luminance) + '; ' + str(timesec) + '\n')
    f.close()
    pms5003.fan_off()
    ROUND += 1
    TICKER += 1
    wdt.feed()
    time.sleep(80)
    time.sleep(BIGSLEEP)
