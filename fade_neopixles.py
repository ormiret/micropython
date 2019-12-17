from machine import Pin
from neopixel import NeoPixel
import urandom
import time

NUM_PIXELS = 60
NUM_PANELS = 3
PANELS = [20, 19, 21]

STEPS = 50
PAUSE = 0.01

pin = Pin(5, Pin.OUT) # D1 on nodemcu
# \o/ looks like number on the silkscreen match up to GPIO numbers on the ESP32 boards I've got

np = NeoPixel(pin, NUM_PIXELS)

np[0] = (0, 128, 0)
np.write()
for i in range(1, NUM_PIXELS):
    np[i-1] = (0,0,0)
    np[i] = (0, 128, 0)
    np.write()
    time.sleep(.05)


# from colorsys.py
def hsv_to_rgb(h, s, v):
    if s == 0.0:
        return v, v, v
    i = int(h*6.0) # XXX assume int() truncates!
    f = (h*6.0) - i
    p = v*(1.0 - s)
    q = v*(1.0 - s*f)
    t = v*(1.0 - s*(1.0-f))
    i = i%6
    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q
    # Cannot get here

def randc():
    r,g,b = hsv_to_rgb(urandom.getrandbits(8)/255.0, 1, 1.0)
    return [int(r*255), int(g*255), int(b*255)]

def fade_each_px():
    cur = [randc() for x in range(NUM_PIXELS)]
    nxt = [randc() for x in range(NUM_PIXELS)]
    while True:
        for s in range(STEPS):
            for p in range(NUM_PIXELS):
                np[p] = [int(cur[p][c]+(s*(nxt[p][c]-cur[p][c])/STEPS)) for c in range(3)]
            np.write()
            time.sleep(PAUSE)
        cur = nxt
        nxt = [randc() for x in range(NUM_PIXELS)]
        time.sleep(1000*PAUSE)
        print("Next colour.")
    
def fade_each():
    cur = [randc() for x in range(NUM_PANELS)]
    nxt = [randc() for x in range(NUM_PANELS)]
    while True:
        for i in range(STEPS):
            for p in range(NUM_PANELS):
                for q in range(PANELS[p]):
                    np[sum(PANELS[:p])+q] = [int(cur[p][j]+(i*(nxt[p][j]-cur[p][j])/STEPS)) for j in range(3)]
            np.write()
            time.sleep(PAUSE)
        cur = nxt
        nxt = [randc() for x in range(NUM_PANELS)]
        time.sleep(1.5)
        print("Next colour.")

def jmp_each():
    while True:
        for i in range(NUM_PIXELS):
            np[i] = [int(v) for v in randc()]
        np.write()
        time.sleep(0.5)

def fade_all():
    cur = randc()
    nxt = randc()
    while True:
        for i in range(STEPS):
            val = [int(cur[j]+(i*(nxt[j]-cur[j])/STEPS)) for j in range(3)]
            for p in range(NUM_PIXELS):
                np[p] = val
            np.write()
            time.sleep(PAUSE)
        cur = nxt
        nxt = randc()
        time.sleep(PAUSE*20)
        print("Next colour")

fade_each()
# jmp_each()
# fade_each_px()
# fade_all()
