from machine import Pin
from time import sleep

pins = [14, 12, 13, 15] #D5, D6, D7, D8

pin_led_states = [
    [1, 0, -1, -1], #R1
    [-1, 0, -1, 1], #G1
    [-1, 0, 1, -1], #B1
    [-1, 1, 0, -1], #R2
    [1, -1, 0, -1], #G2
    [-1, -1, 0, 1], #B2
    [-1, -1, 1, 0], #R3
    [-1, 1, -1, 0], #G3
    [1, -1, -1, 0], #B3
    [0, -1, -1, 1], #R4
    [0, -1, 1, -1], #G4
    [0, 1, -1, -1]] #B4

def set_pin(pin_index, pin_state):
    print("Pin ", pins[pin_index], " ", pin_state)
    if pin_state == -1:
        Pin(pins[pin_index], Pin.IN, Pin.PULL_UP)
    else:
        p = Pin(pins[pin_index], Pin.OUT)
        if pin_state:
            p.on()
        else:
            p.off()

def light_led(led_number):
    for pin_index, pin_state in enumerate(pin_led_states[led_number]):
        set_pin(pin_index, pin_state)

for i in range(4):
    set_pin(i, -1)

while True:
    print("Loop.")
    for i in range(12):
        light_led(i)
        sleep(.25)
