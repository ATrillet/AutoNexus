from PIL import Image, ImageChops
import numpy as np
import pyscreenshot as ImageGrab
from os import path
from pynput.keyboard import Key, Controller, Listener
from pynput import keyboard
import time

#realm tick rate 0.2s
hp_percent = 23
heal_percent = 50
board = Controller()

def on_press_end(key):
    if key == keyboard.Key.end:
        return False

def on_press_loop(key):
    if key == keyboard.Key.alt_l:
        return False

def auto_nexus(hpx, hpy, x_diff):
    im1 = ImageGrab.grab(bbox=(hpx,hpy,hpx+x_diff,hpy+1))  # x1, y1, x2, y2
    xnexus = int((hp_percent/100)*x_diff)
    xheal = int((heal_percent/100)*x_diff)
    rgb_im = im1.convert('RGB')
    a1,b1,c1 = rgb_im.getpixel((xnexus, 0))
    a2,b2,c2 = rgb_im.getpixel((xheal, 0))
    if a1==84 and b1==84 and c1==84:
        board.press('r')
        print("dying")
        time.sleep(4)
    elif a2==84 and b2==84 and c2==84:
        board.press('f')




def find_hp_bar(hpr,hpg,hpb):
    img = ImageGrab.grab()
    img.save('screenshot.png')

    w, h = img.size
    midw = int(w/2)
    midh = int(h/2)

    rgb_im = img.convert('RGB')

    arrayx = []
    arrayy = []

    for y in range(0, midh):
        for x in range(midw, w):
            r,g,b = rgb_im.getpixel((x, y))
            if r==hpr and g==hpg and b==hpb:
                arrayx.append(x)
                arrayy.append(y)

    pixarray = []

    x1 = arrayx[0]
    x2 = arrayx[-1]
    xdiff = x2-x1

    y1 = arrayy[0]

    return x1, y1, xdiff
    

xs, y, xdiff = find_hp_bar(224,52,52)

test = True
print("starting")
while test:
    auto_nexus(xs,y, xdiff)
    with keyboard.Listener(on_press=on_press_end) as listener2:
        time.sleep(.01)
        if not listener2.running:
            print('end')
            test = False
    
