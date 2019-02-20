from machine import Pin
from neopixel import NeoPixel
import time

# Translated from Tim Bartlett's arduino code
# https://github.com/timpear/NeoCandle

NUM_PIXELS = 9

red = 255
grn = 100
blu = 10

rd = 1
gd = 3
bd = 5

pin = Pin(0, Pin.OUT) # D3 on nodemcu   
np = NeoPixel(pin, NUM_PIXELS)

def setall(r, g, b):
    for i in range(NUM_PIXELS):
        np[i] = (r, g, b)
    np.write()


while True:
    red = (red + rd)
    if red > 255 or red < 0:
        rd = -1*rd
        red = red + rd
    grn = grn + gd
    if grn > 255 or grn < 0:
        gd = -1*gd
        grn = grn + gd
    blu = blu + bd
    if blu > 255 or blu < 0:
        bd = -1*bd
        blu = blu + bd
    setall(red, grn, blu)
    time.sleep(.01)
