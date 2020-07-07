from machine import Pin, ADC
from neopixel import NeoPixel
import utime

NUM_PIXELS = 1
colours = {'red': (255, 0, 0),
           'green': (0, 255, 0),
           'blue': (0, 0, 255),
           'orange': (255, 165, 0),
           'off': (0,0,0) }

np_pin = Pin(12, Pin.OUT) # D6 
np = NeoPixel(np_pin, NUM_PIXELS)
np[0] = colours['red']
np.write()

touch = Pin(13, Pin.IN) # D7

powered = Pin(14, Pin.IN) # D5

load = ADC(0)

relay = Pin(5, Pin.OUT) #D1
relay.value(0) 

prev_read = utime.ticks_ms()
print("Starting.")
while True:
    if powered.value() and np[0] != colours['green']:
        np[0] = colours['green']
        np.write()
    if not powered.value() and np[0] != colours['red']:
        np[0] = colours['red']
        np.write()
    if touch.value():
        print("Touch")
        if relay.value():
            relay.value(0)
        else:
            relay.value(1)
        np[0] = colours['orange']
        np.write()
        utime.sleep(0.25)
    if utime.ticks_diff(utime.ticks_ms(), prev_read) >= 1000:
        val = load.read()
        print("Load: ", val, " -> ", (val/310.3)*20, " Amps")
        prev_read = utime.ticks_ms()
