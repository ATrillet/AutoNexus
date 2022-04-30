from PIL import Image, ImageChops
from mss.models import Pixels
#import numpy as np
import pyscreenshot as ImageGrab
from os import path
from pynput.keyboard import Key, Controller, Listener
from pynput import keyboard
import time
import mss
import mss.tools

#realm tick rate 0.2s
#Probably wrong now that the game is ported to the new engine
nexus_hp_percent = 30
heal_hp_percent = 50
board = Controller()

#Helps end the loops when the program is running
def on_press_end(key):
    if key == keyboard.Key.end:
        return False

#Takes and x and y value of a specific pixel to check for a change
#That pixel is determined by hp_percent and find_hp_bar
# #When that pixel changes to to the background color of the hp bar, nexus

def auto_nexusv2(x, hpx, hpy, width):
    with mss.mss() as sct:
        monitor = {'mon':1, 'top':hpy, 'left':x, 'width':width, 'height':1}
        output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)
        pic = sct.grab(monitor)
        # mss.tools.to_png(pic.rgb, pic.size, output=output)
        # print(output)
        a = pic.pixel(hpx-x, 0)
        b = pic.pixel(width-1,0)
        # print(a)
        # print(b)
    if ((a[1]==84 or a[1] == 255) & (b[1]==84 or b[1] == 255)):
        board.press('r')
        board.release('r')
        print("dying")
        time.sleep(0.01)

def auto_heal(x, hpx, hpy, width):
    with mss.mss() as sct:
        pic = sct.grab({'mon':1, 'top':hpy, 'left':x, 'width':width, 'height':1})
        a = pic.pixel(hpx-x, 0)
        b = pic.pixel(width-1,0)
        # print(a)
        # print(b)
    if ((a[1]==84 or a[1] == 255) & (b[1]==84 or b[1] == 255)):
        board.press('f')
        board.release('f')
        print("healing")
        time.sleep(.01)



def find_hp_bar(hpr,hpg,hpb):
    img = ImageGrab.grab()      #Grab the entire screen
    img.save('screenshot.png')  #save the screenshot

    gfound = 0

    w, h = img.size             #get the dimensions of the screenshot
    midw = int(w/2)             #I know that the hp bar is on the right side of the screen
    midh = int(h/2)             #I know that the hp bar is on the top side of the screen

    print(img.size)

    im2 = ImageGrab.grab(bbox=(midw,0,w,midh))
    im2.save('im2.png')

    rgb_im = img.convert('RGB') #Convert the image to rgb values

    arrayx = []
    arrayy = []
    
    #When the specific pixel is equal to the hp bar color, save the pixel location.
    for y in range(0, midh):
        for x in range(midw, w):
            r,g,b = rgb_im.getpixel((x, y))
            if (r==135 and g==218 and b==62):
                arrayx.append(x)
                arrayy.append(y)
                gfound = 1
            if (not (r==135 and g==218 and b==62) and gfound==1):
                y = midh
                x = w

    x1 = arrayx[0]          #Get where the hp bar starts on the x axis
    x2 = arrayx[-1]         #Get where the hp bar ends on the x axis
    hp_bar_length = x2-x1            #Determine the length of the hp bar

    y1 = arrayy[0]          #Get the y value that the hp bar starts
    y2 = arrayy[-1]           #Gives where we need to look for y value changes

    return x1,y1,y2,hp_bar_length

def calculate_difference(value, percentage):
    return int(value*(percentage/100))

def setup():
    x,y,y2,hp_pixel_count = find_hp_bar(135,218,62)               #135, 218, 62 is the rgb value of the green realm currenty uses for the HP bar.  When we see this color, we have found the bar
    # nexusx = x + calculate_difference(hp_pixel_count, 30)
    # healx = x + calculate_difference(hp_pixel_count,50)
    nexusx = x + round(hp_pixel_count*nexus_hp_percent/100)
    healx = x + round(hp_pixel_count*heal_hp_percent/100)

    print(x)
    print(nexusx)
    print(healx)
    print(hp_pixel_count)
    print(y)
    print(y2)
    
    imgtest = ImageGrab.grab(bbox=(x,y,x+hp_pixel_count,y2+1))      #Grab the entire screen
    imgtest.save('new_pic.png')  #save the screenshot
    return x,y,nexusx, healx, hp_pixel_count

# im1 = ImageGrab.grab(bbox=(nexusx,y,nexusx+1,y+1))    #The rest is mostly for testing
# rgb_im = im1.convert('RGB') 
# r,g,b = rgb_im.getpixel((0, 0))
# print(r,g,b,sep=',')

x,y,nexusx, healx, width = setup()
test = True
print("starting")
while test:
    start = time.time()
    with keyboard.Listener(on_press=on_press_end) as listener2:
        time.sleep(.01)
        if not listener2.running:
            print('end')
            test = False
    auto_nexusv2(x-1, nexusx, y, width)
    auto_heal(x,healx, y, width)
    end = time.time()
    print(end-start)
