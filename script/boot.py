import os
import machine
import pycom
import network
import config
import ubinascii

uart = machine.UART(0, 115200)
os.dupterm(uart)

pycom.heartbeat(False)

server = network.Server(login=(config.USERNAME, config.PASSWORD), timeout=60)
macdev = ubinascii.hexlify(machine.unique_id(),':').decode()
print("MAC address:", macdev)
wlan = network.WLAN()  # Default is WLAN.AP, so LoPy is accessible via telnet.
print("WLAN MODE:  ", wlan.mode())

machine.main('main.py')
print('==========Starting main.py==========\n')
