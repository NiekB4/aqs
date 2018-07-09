import time
from machine import Pin, UART

# Setup for the Air Dust Sensor PMS5003
SET_PORT1 = 'P8'
SET_PORT2 = 'P9'

#RESET_PORT1 = 'P8'  # not used
#RESET_PORT2 = 'P13'  # not used

STARTUP_TIME = 30  # 30 seconds of startup time, needed for ventilator

set_pin1 = Pin(SET_PORT1, mode=Pin.OUT)
set_pin2 = Pin(SET_PORT2, mode=Pin.OUT)

#  reset_pin1 = Pin(RESET_PORT1, mode=Pin.OUT)
#  reset_pin2 = Pin(RESET_PORT2, mode=Pin.OUT)
data_uart1 = UART(1, baudrate=9600, parity=None, stop=1, pins=('P4', 'P3'))
data_uart2 = UART(1, baudrate=9600, parity=None, stop=1, pins=('P12', 'P11'))


def fan_on():
    set_pin1.value(1)
    set_pin2.value(1)


def fan_off():
    set_pin1.value(0)
    set_pin2.value(0)


def reset():
    pass
    #  reset_pin1.value(1)


def set_sensor():
    fan_on()
    time.sleep(STARTUP_TIME)
