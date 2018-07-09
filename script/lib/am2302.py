from dth import DTH
from machine import Pin

# Setup for temperature and humidity sensor
th1 = DTH(Pin('P13', mode=Pin.OPEN_DRAIN), 1)
th2 = DTH(Pin('P23', mode=Pin.OPEN_DRAIN), 1)
