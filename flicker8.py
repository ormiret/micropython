from machine import Pin
from neopixel import NeoPixel
import time

# Translated from Tim Bartlett's arduino code
# https://github.com/timpear/NeoCandle

NUM_PIXELS = 9

redPx = 255
grnHigh = 100
bluePx = 10

burnDepth = 10
flutterDepth = 25
cycleTime = .120

flickerDepth = (burnDepth + flutterDepth) / 2.4
burnLow = grnHigh - burnDepth
burnDelay = (cycleTime/2)/burnDepth
fDelay = burnDelay
flickLow = int(grnHigh - flickerDepth)
flickDelay = (cycleTime/2)/flickerDepth
flutLow = int(grnHigh - flutterDepth)
flutDelay = (cycleTime/2)/flutterDepth

pin = Pin(0, Pin.OUT) # D3 on nodemcu   
np = NeoPixel(pin, NUM_PIXELS)

def setall(r, g, b):
    for i in range(NUM_PIXELS):
        np[i] = (r, g, b)
    np.write()

def fire(grnMin):
    for grnPx in range(grnHigh, grnMin, -1):
        setall(redPx, grnPx, bluePx)
        time.sleep(fDelay)
    for grnPx in range(grnMin, grnHigh):
        setall(redPx, grnPx, bluePx)
        time.sleep(fDelay)

def on(t):
    setall(redPx, grnHigh-5, bluePx)
    time.sleep(t)

def burn(t):
    fDelay = burnDelay
    for var in range(t*8):
        fire(burnLow)

def flicker(t):
    fDelay = burnDelay
    fire(burnLow)
    for var in range(t*8):
        fire(flickLow)
    fDelay = burnDelay
    for var in range(3):
        fire(burnLow)

def flutter(t):
    fDelay = burnDelay
    fire(burnLow)
    fDelay = burnDelay
    fire(flickLow)
    fDelay = flutDelay
    for var in range(t*8):
        fire(flutLow)
    fDelay = flickDelay
    fire(flickLow)
    fire(flickLow)
    fDelay = burnDelay
    fire(burnLow)
    fire(burnLow)

def run():
    print("burn")
    burn(10)
    print("flicker")
    flicker(5)
    print("burn")
    burn(8)
    print("flutter")
    flutter(6)
    print("burn")
    burn(3)
    print("on")
    on(10)
    print("burn")
    burn(10)
    print("flicker")
    flicker(10)
         

while True:
    print("loop")
    run()
