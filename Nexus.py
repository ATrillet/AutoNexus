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

def auto_nexus(hpx, hpy,r,g,b):
    im1 = ImageGrab.grab(bbox=(x,y,x+1,y+1))  # x1, y1, x2, y2
    rgb_im = im1.convert('RGB')
    a,b,c = rgb_im.getpixel((0, 0))
    if a==82 and b==85 and c==82:
        print("dying")
        board.press('r')
    else:
        print("living")




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
            if r==hpr and g==hpg and b==hpb:
            # if r==224 and g==52 and b==52:
                arrayx.append(x)
                arrayy.append(y)

    pixarray = []
    x1 = arrayx[0]
    x2 = arrayx[-1]
    diff = x2-x1
    offsetx = int(diff/hp_percent)
    x2 = x1 + offsetx


    y1 = arrayy[0]
    y2 = arrayy[-1]
    diff = y2-y1
    offsety = int(diff/2)
    y3 = y1 + offsety

    r,g,b = rgb_im.getpixel((x2, y3))

    for y in range(y1, y2):
        pixsub = []
        for x in range(x1, x2):
            pixsub.append(rgb_im.getpixel((x, y)))
        pixarray.append(pixsub)

    new_array = np.array(pixarray, dtype=np.uint8)
    new_image = Image.fromarray(new_array)
    new_image.save('new_pic.png')
    return x2,y3,r,g,b

x,y,r,g,b = find_hp_bar(222,52,49)
im1 = ImageGrab.grab(bbox=(x,y,x+1,y+1))
rgb_im = im1.convert('RGB')
r,g,b = rgb_im.getpixel((0, 0))
print(r,g,b,sep=',')

i = 0
test = True
state = True
while test:
    with keyboard.Listener(on_press=on_press_end) as listener2:
        time.sleep(.05)
        if not listener2.running:
            print('end')
            test = False
    if state:
        # print("running...")
        auto_nexus(x,y,r,g,b)
    else:
        print("off...")

# --------------------------------------------------------------------------    

# with keyboard.Listener(on_press=on_press_start) as listener:
#     listener.join() # wait for F11...

# while True:
#     print("setup")
#     im1 = ImageGrab.grab(bbox=(2120, 630, 2300, 670))  # x1, y1, x2, y2
#     im1.save('screenshot.png')
#     im1.show()
#     time.sleep(4)
#     if keyboard.is_pressed('h'):
#         print("end setup")
#         break
# time.sleep(1)
# while True:
#     if keyboard.is_pressed('alt'):
#         time.sleep(3)
#         print("sleep")
#     else:
#         board = Controller()
#         im1 = ImageGrab.grab(bbox=(2120, 630, 2300, 670))  # x1, y1, x2, y2
#         time.sleep(.100)
#         im2 = ImageGrab.grab(bbox=(2120, 630, 2300, 670))

#         # Testing
#         # im1 = ImageGrab.grab(bbox=(2120, 330, 2350, 600)) #x1, y1, x2, y2
#         # im2 = ImageGrab.grab(bbox=(2120, 330, 2350, 600))

#         # im1.show()

#         im1.save('screenshot.png')
#         im2.save('screenshot1.png')

#         diff = ImageChops.difference(im1, im2)

#         if diff.getbbox():
#             board.press('r')

#     if keyboard.is_pressed('9'):
#         print("End Auto")
#         break


