import machine
import p9813
import time

import gc
#import webrepl
#webrepl.start()
gc.collect()


num_conts = 1
pin_clk = machine.Pin(5, machine.Pin.OUT) #D1
pin_data = machine.Pin(4, machine.Pin.OUT) #D2

chain = p9813.P9813(pin_clk, pin_data, num_conts)

def blank():
    for i in range(num_conts):
        chain[i] = [0, 0, 0]

def blink():
    for i in range(num_conts):
        for j in range(3):
            blank()
            val = [0, 0, 0]
            val[j] = 127
            chain[i] = val
            print(i, ", ", j, " ,", chain) 
            chain.write()
            time.sleep(1)

while True:
    blink()
