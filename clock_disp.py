import clock
import machine
import p9813
import time

import urequests
import ujson
import utime

import gc
#import webrepl
#webrepl.start()
gc.collect()

from secrets import networks

num_conts = 8
pin_clk = machine.Pin(5, machine.Pin.OUT) #D1
pin_data = machine.Pin(4, machine.Pin.OUT) #D2

chain = p9813.P9813(pin_clk, pin_data, num_conts)


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
        break
    else:
        print(net[0].decode(), " not in known networks")
else:
    print("No known networks seen. Switching off networking")
    wlan.active(False)

def set_time():
    resp = urequests.get("http://idea.bodaegl.com/time.json")
    t = ujson.loads(resp.text)
    clock.clockSet(t['hours'], t['minutes'], t['seconds'])
    print("Time set to ", t['hours'], ":", t['minutes'], ":",  t['seconds'])

def run():
    sep = True
    while True:
        _,_,_,_,h,m,s,ms = machine.RTC().datetime()
        if (h > 12):
            h = h - 12
        c = clock.generateClock(h, m, sep)
        print('{:02}{}{:02} = '.format(h, ':' if sep else ' ',m), c)
        for i in range(num_conts):
            chain[i] = c[i]
        chain.write()
        sep = not sep
        _,_,_,_,h,m,s,ms = machine.RTC().datetime()
        utime.sleep_ms(1000 - ms)

set_time()
run()
