import socket
import time
import numpy
import struct
import colorsys
from random import randint, random

NUM_PIXELS = 64
target = ("172.31.5.163", 10089)
framebuf = [[0, 0, 0] for i in xrange(NUM_PIXELS)]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_frame(sock, target, frame):
    message = ""
    for pix in frame:
        message += struct.pack("!BBB", pix[0], pix[1], pix[2])
    sock.sendto(message, target)

def up(c):    
    for i in xrange(NUM_PIXELS):
        framebuf[i-1] = [0,0,0]            
        framebuf[i] = c
        send_frame(s, target, framebuf)
        time.sleep(.1)

def down(c):
    for i in xrange(NUM_PIXELS, 0, -1):
        framebuf[i-1] = [0,0,0]
        framebuf[i-2] = c
        send_frame(s, target, framebuf)
        time.sleep(0.1)

def randc():
    r,g,b = colorsys.hsv_to_rgb(random(), 1, 1.0)
    return [int(r*255), int(g*255), int(b*255)]

def rand():
    for i in xrange(10):
        for j in xrange(NUM_PIXELS):
            framebuf[j] = randc()
        send_frame(s, target, framebuf)
        time.sleep(.5)
        
def set_all(fb, c):
    for i in xrange(NUM_PIXELS):
        fb[i] = c
    return fb

def fade():
    col = randc()
    for sc in range(10, 100, 2) + range(100, 5, -2):
        col_s = [int(sc*v/100) for v in col]
        set_all(framebuf, col_s)
        send_frame(s, target, framebuf)
        time.sleep(0.1)
STEPS=100
def fade_btw(one, two):
    print one, two
    for i in xrange(STEPS):
        t = [one[j]+(i*(two[j]-one[j])/STEPS) for j in xrange(3)]
        set_all(framebuf, t)
        send_frame(s, target, framebuf)
        time.sleep(0.3)
        
def fadec():
    cur = randc()
    nxt = randc()
    while True:
        fade_btw(cur, nxt)
        cur = nxt
        nxt = randc()

def fade_each():
    cur = [randc() for x in xrange(NUM_PIXELS)]
    nxt = [randc() for x in xrange(NUM_PIXELS)]
    frame = cur
    while True:
        for i in xrange(STEPS):
            for p in xrange(NUM_PIXELS):
                frame[p] = [cur[p][j]+(i*(nxt[p][j]-cur[p][j])/STEPS) for j in xrange(3)]
            send_frame(s, target, frame)
            time.sleep(0.3)
        cur = nxt
        nxt = [randc() for x in xrange(NUM_PIXELS)]

def jmp_each():
    while True:
        frame = [randc() for x in xrange(NUM_PIXELS)]
        send_frame(s, target, frame)
        time.sleep(0.5)
        
    
# jmp_each()
# fadec()
fade_each()

while True:
    #c = randc()
    #up(c)
    #down(c)
    #rand()
    #fade()
    set_all(framebuf, randc())
    send_frame(s, target, framebuf)
    time.sleep(1)
        
