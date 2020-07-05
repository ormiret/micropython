from machine import Pin
from neopixel import NeoPixel
import urandom
import time

NUM_PIXELS = 1
colours = {'red': (0, 255, 0),
           'green': (255, 0, 0),
           'blue': (0, 0, 255),
           'orange': (165, 255, 0),
           'off': (0,0,0) }

sequence = list(colours.values())
pos = 0
np_pin = Pin(12, Pin.OUT) # D6 on nodemcu D1
np = NeoPixel(np_pin, NUM_PIXELS)
np[0] = sequence[pos]
np.write()

touch = Pin(13, Pin.IN)

print("Starting.")
while True:
    if touch.value():
        print("Touch")
        pos = (pos+1)%len(sequence)
        np[0] = sequence[pos]
        np.write()
        time.sleep(0.5)

fade_each()
# jmp_each()
# fade_each_px()
# fade_all()
