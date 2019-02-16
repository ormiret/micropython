from machine import Pin
from neopixel import NeoPixel
import time


import network
sta_if = network.WLAN(network.STA_IF)
sta_if.active(False)
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

NUM_PIXELS = 10

r, g, b = (0, 0, 0)
r_step, g_step, b_step = (3, 7, 4)
pin = Pin(0, Pin.OUT)   
np = NeoPixel(pin, NUM_PIXELS)
    
while True:
    print("loop")
    print("Setting pixels to %d %d %d"%(r, g, b))
    for i in range(NUM_PIXELS):
        np[i] = (r, g, b) 
    np.write() # write data to all pixels
    r, g, b = ((r+r_step)%255, (g+g_step)%255, (b+b_step)%255)
    time.sleep(.25)


# started at 13:56
# died at 21:17(ish)
# run time 
