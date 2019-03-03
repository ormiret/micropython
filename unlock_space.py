import machine
from neopixel import NeoPixel
import time

import urequests
import ujson
import utime

import gc
#import webrepl
#webrepl.start()
gc.collect()

from secrets import networks, unlock_url
colours = {'red': (0, 255, 0),
           'green': (255, 0, 0),
           'blue': (0, 0, 255),
           'orange': (165, 255, 0),
           'off': (0,0,0) }

led_pin = machine.Pin(0, machine.Pin.OUT) # D3
np = NeoPixel(led_pin, 1)

button = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)

# light LED red
np[0] = colours['orange']
np.write()

def blink(p, col=colours['red'], dur=0.25, rep=3):
    orig = p[0]
    for i in range(rep):
        p[0] = col
        p.write()
        time.sleep(dur)
        p[0] = colours['off']
        p.write()
        time.sleep(dur)
    p[0] = orig
    p.write()

#connect to wifi
import network, time
ap = network.WLAN(network.AP_IF)
ap.active(False)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
nets = wlan.scan()
for net in nets:
    ssid = net[0].decode()
    if ssid in networks:
        print("Network found ", ssid)
        wlan.connect(ssid, networks[ssid])
        while not wlan.isconnected():
            time.sleep(1)
        print("Connected to ", ssid)
        ip = wlan.ifconfig()[0]
        print("IP:", ip)
        np[0] = colours['blue']
        np.write()
        break
    else:
        print(net[0].decode(), " not in known networks")
else:
    print("No known networks seen. Switching off networking")
    wlan.active(False)
    np[0] = colours['red']
    np.write()

if wlan.active():
    while True:
        if not button.value():
            resp = urequests.get(unlock_url)
            ul = ujson.loads(resp.text)
            if ul['unlocked']:
                print("Unlocked")
                np[0] = colours['green']
                np.write()
                time.sleep(10)
                np[0] = colours['blue']
                np.write()
            else:
                print("Error:", ul['message'])
                blink(np, colours['red'], rep=5)
