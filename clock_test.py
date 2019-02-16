from clock import generateClock
from machine import Pin
import p9813
import time

pin_clk = Pin(5, Pin.OUT) #D1
pin_data = Pin(4, Pin.OUT) #D2

num_leds = 8
chain = p9813.P9813(pin_clk, pin_data, num_leds)

while True:
    for h in range(1,13):
        for m in range(60):
            vals = generateClock(h, m)
            for i in range(num_leds):
                chain[i] = vals[i]
            chain.write()
            time.sleep(1)
got 
