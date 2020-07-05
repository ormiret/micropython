# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import webrepl
webrepl.start()

from secrets import networks

#connect to wifi
import network, time
ap = network.WLAN(network.AP_IF)
ap.active(False)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
nets = wlan.scan()
for net in nets:
    ssid = net[0].decode()
    if ssid in networks:
        print("Network found ", ssid)
        wlan.connect(ssid, networks[ssid])
        while not wlan.isconnected():
            time.sleep(1)
        print("Connected to ", ssid)
        ip = wlan.ifconfig()[0]
        print("IP:", ip)
        break
    else:
        print("Unknown network: ", ssid)    
else:
    print("No known networks seen. Switching off networking")
    wlan.active(False)

gc.collect()



