import p9813
import machine
import time
import urandom

STEPS = 20
PAUSE = 5
BETWEEN = 2

num_lights = 6
pin_clk = machine.Pin(14, machine.Pin.OUT) #D2
pin_data = machine.Pin(27, machine.Pin.OUT) #D3

chain = p9813.P9813(pin_clk, pin_data, num_lights)

chain[0] = [0, 128, 0]
chain.write()
time.sleep(0.5)
for i in range(1, num_lights):
    chain[i-1] = [0, 0, 0]
    chain[i] = [0, 128, 0]
    chain.write()
    time.sleep(0.5)

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
    cur = [randc() for x in range(num_lights)]
    nxt = [randc() for x in range(num_lights)]
    while True:
        for i in range(STEPS):
            for p in range(num_lights):
                chain[p] = [int(cur[p][j]+(i*(nxt[p][j]-cur[p][j])/STEPS)) for j in range(3)]
            chain.write()
            time.sleep(PAUSE)
        cur = nxt
        nxt = [randc() for x in range(num_lights)]
        time.sleep(BETWEEN)
        print("Next colour.")

def fade_cycle():
    while True:
        for l in range(num_lights):
            c = randc()
            print("light :", l, "colour: ", c)
            for i in range(STEPS):
                chain[l] = [int(i/STEPS*c[j]) for j in range(3)]
                chain.write()
                time.sleep(PAUSE)
            for i in range(STEPS, 0, -1):
                chain[l] = [int(i/STEPS*c[j]) for j in range(3)]
                chain.write()
                time.sleep(PAUSE)


def fade_all():
    cur = randc()
    nxt = randc()
    while True:
        for i in range(STEPS):
            val = [int(cur[j]+(i*(nxt[j]-cur[j])/STEPS)) for j in range(3)]
            for p in range(num_lights):
                chain[p] = val
            chain.write()
            time.sleep(PAUSE)
        cur = nxt
        nxt = randc()
        time.sleep(BETWEEN)
        print("Next colour ", nxt)
        
fade_all()
