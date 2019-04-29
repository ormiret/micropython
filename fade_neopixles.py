from machine import Pin
from neopixel import NeoPixel
import urandom
import time

NUM_PIXELS = 64
STEPS = 50

pin = Pin(2, Pin.OUT) #D4 on nodeMCU
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


def fade_each():
    cur = [randc() for x in range(NUM_PIXELS)]
    nxt = [randc() for x in range(NUM_PIXELS)]
    while True:
        for i in range(STEPS):
            for p in range(NUM_PIXELS):
                np[p] = [int(cur[p][j]+(i*(nxt[p][j]-cur[p][j])/STEPS)) for j in range(3)]
            np.write()
            time.sleep(0.01)
        cur = nxt
        nxt = [randc() for x in range(NUM_PIXELS)]
        time.sleep(0.5)
    

fade_each()
