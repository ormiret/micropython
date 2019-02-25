from machine import Pin
from neopixel import NeoPixel

import urequests
import ujson
import time

sensor_url = "http://api.luftdaten.info/static/v1/sensor/5331/"

NUM_PIXELS = 16
np_pin = Pin(0, Pin.OUT)
np = NeoPixel(np_pin, NUM_PIXELS)

off = (0,0,0)

def pick_col(lvl):
    colours = {'red': (255, 0, 0),
               'green': (0, 255, 0),
               'blue': (0, 0, 255),
               'orange': (255, 165, 0),
               'yellow': (255, 255, 0),
               'yel_grn': (255, 255, 0),
               'off': (0,0,0) }
    if lvl < 20: return colours['green']
    if lvl < 30: return colours['yellow']
    if lvl < 40: return colours['orange']
    return colours['red']

def build_pix(col, lvl, mxm=100):
    return [col if lvl > i*(mxm/(NUM_PIXELS/2.0)) else off for i in range(8)]

def disp(pix, pm2, pm10):
    vals = build_pix(pick_col(pm2), pm2) + build_pix(pick_col(pm10), pm10)
    for i in range(NUM_PIXELS):
        pix[i] = vals[i]
    pix.write()
    print("Pixel values: ", vals)

def get_current(url):
    resp = urequests.get(url)
    vals = ujson.loads(resp.text)
    return vals[-1]

def update():
    pm10 = 0
    pm2 = 0
    cur = get_current(sensor_url)
    for reading in cur['sensordatavalues']:
        if reading['value_type'] == "P2":
            pm2 = float(reading['value'])
            print("PM2.5 value:", pm2)
        if reading['value_type'] == "P1":
            pm10 = float(reading['value'])
            print("PM10 value:", pm10)
    disp(np, pm2, pm10)

while True:
    update()
    time.sleep(60)
