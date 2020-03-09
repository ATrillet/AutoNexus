from PIL import Image, ImageChops
import numpy as np
import pyscreenshot as ImageGrab
from os import path
from pynput.keyboard import Key, Controller, Listener
from pynput import keyboard
import time

#realm tick rate 0.2s

def on_press_end(key):
    if key == keyboard.Key.end:
        return False

def on_press_loop(key):
    if key == keyboard.Key.alt_l:
        return False

def auto_nexus():
    time.sleep(1)
    print("snap")
    im1 = ImageGrab.grab(bbox=(2120, 630, 2300, 670))  # x1, y1, x2, y2
    time.sleep(1)
    im2 = ImageGrab.grab(bbox=(2120, 630, 2300, 670))
    im1.save('screenshot.png')
    im2.save('screenshot1.png')

    diff = ImageChops.difference(im1,im2)
    diff.save('test.png')
    return np.mean(diff)

values = []
for x in range(10):
    change = auto_nexus()
    values.append(change)
    print(change)
    if change > 150:
        break

# i = 0
# test = True
# state = False
# while test:
#     with keyboard.Listener(on_press=on_press_loop) as listener:
#         time.sleep(.4)
#         if not listener.running:
#             state = not state
#     with keyboard.Listener(on_press=on_press_end) as listener2:
#         time.sleep(.10)
#         if not listener2.running:
#             print('end')
#             test = False

#     if state:
#         print("running...")
#         auto_nexus()
#     else:
#         print("off...")

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


