from machine import Pin
from neopixel import NeoPixel
import socket
import network
import time

NUM_PIXELS = 64
port = 10089

pin = Pin(2, Pin.OUT) #D3 on nodeMCU
np = NeoPixel(pin, NUM_PIXELS)

ip = wlan.ifconfig()[0]
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((ip, port))

np[0] = (0, 128, 0)
np.write()
for i in range(1, NUM_PIXELS):
    np[i-1] = (0,0,0)
    np[i] = (0, 128, 0)
    np.write()
    time.sleep(.05)


print("waiting...")
while True:
    data, addr = s.recvfrom(NUM_PIXELS*3)
    # s.sendto(data, addr)
    # print("Received ",len(data)," bytes from ",addr)
    if len(data) >= NUM_PIXELS*3:
        for i in range(NUM_PIXELS):
            np[i] = (data[3*i], data[3*i+1], data[3*i+2])
        np.write()
        # print("Updated neopixels")
