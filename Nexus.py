from PIL import Image, ImageChops
import numpy as np
import pyscreenshot as ImageGrab
from os import path
from pynput.keyboard import Key, Controller, Listener
from pynput import keyboard
import time

#realm tick rate 0.2s
hp_percent = 3
board = Controller()

def on_press_end(key):
    if key == keyboard.Key.end:
        return False

def on_press_loop(key):
    if key == keyboard.Key.alt_l:
        return False

def auto_nexus(hpx, hpy):
    im1 = ImageGrab.grab(bbox=(x,y,x+1,y+1))  # x1, y1, x2, y2
    rgb_im = im1.convert('RGB')
    a,b,c = rgb_im.getpixel((0, 0))
    if a==84 and b==84 and c==84:
        board.press('f')
        board.press('r')
        print("dying")
        time.sleep(4)




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
        pixsub = []
        for x in range(midw, w):
            r,g,b = rgb_im.getpixel((x, y))
            if r==224 and g==52 and b==52:
                arrayx.append(x)
                arrayy.append(y)

    pixarray = []
    x1 = arrayx[0]
    x2 = arrayx[-1]
    diff = x2-x1
    offsetx = int(diff/hp_percent)
    x3 = x1 + offsetx


    y1 = arrayy[0]
    y2 = arrayy[-1]
    diff = y2-y1
    offsety = 1
    y3 = y1 + offsety

    r,g,b = rgb_im.getpixel((x3, y3))



    for y in range(y1-1,y3-1):
        pixsub = []
        for x in range(x1, x3):
            pixsub.append(rgb_im.getpixel((x, y)))
        pixarray.append(pixsub)

    new_array = np.array(pixarray, dtype=np.uint8)
    new_image = Image.fromarray(new_array)
    new_image.save('new_pic.png')
    return x3,y3

x,y = find_hp_bar(224,52,52)
im1 = ImageGrab.grab(bbox=(x,y,x+1,y+1))
rgb_im = im1.convert('RGB')
r,g,b = rgb_im.getpixel((0, 0))
# print(r,g,b,sep=',')

test = True
print("starting")
while test:
    with keyboard.Listener(on_press=on_press_end) as listener2:
        time.sleep(.01)
        if not listener2.running:
            print('end')
            test = False
    auto_nexus(x,y)
