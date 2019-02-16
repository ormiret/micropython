from machine import Pin, PWM
from time import sleep

import network
sta_if = network.WLAN(network.STA_IF)
sta_if.active(False)
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)
print("Killed networking")

pwm = [PWM(Pin(5), freq=500, duty=512),
       PWM(Pin(4), freq=500, duty=512),
       PWM(Pin(0), freq=500, duty=512),
       PWM(Pin(14), freq=500, duty=512)]

max_width = 300
min_width = .1

mstep = 1.2
astep = [1, 3, 5, 7]
mode = "add"

cur_width = [min_width] * 4

if mode == "mult":
    while True:
        pwm.duty(int(cur_width))
        
        sleep(0.01)

        cur_width *= wstep
        print("cur_width:", cur_width)
    
        if cur_width > max_width or cur_width < min_width:
            mstep = 1/mstep
            cur_width *= mstep
else:
    while True:
        for i in range(len(pwm)):
            # print("Set %d to %d"%(i, cur_width[i]))
            pwm[i].duty(int(cur_width[i]))
            cur_width[i] += astep[i]
            if cur_width[i] > max_width or cur_width[i] < min_width:
                astep[i] = -1 * astep[i]
                cur_width[i] += astep[i]
        sleep(0.01)
            
