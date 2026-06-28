# Main controller for template matching and determining input pattern
# Inputs get sent to pi pico then returned

import serial
import keyboard
import time
import random
from serial.tools import list_ports
import cv2
import numpy as np
import mss
from comms.pico import Pico
import config
from vision.templateMatcher import matchMyTemplate


templateImg = "./ss/pc/relentless.png"

is_key_held = False
key_held = ""
sct = mss.mss()
last_action = 0

pico = Pico()



def recast_relentless():
    time.sleep(random.uniform(0.1, 0.3))
    # send_key("RELEASE_ALL")
    print("RELEASE_ALL")
    time.sleep(random.uniform(0.1, 0.3))
    print("THREE")
    # send_key("THREE")

# offsets_region = {
#     "left": relentless["x"] + 50,
#   "top": relentless["y"] + 100,
#    "width": 200,
#   "height": 50
# }

#mainloop
while True:
    

    print("Locating Relentless...")

    # ss commented for static testing
    # matchImg = screenshot(config.SCREEN_REGION)
    #static ss with relentless off CD
    matchImg = cv2.imread("./ss/pc/full.png")
    #static ss with relentless on CD and active
    # matchImg = cv2.imread("./ss/pc/bufffavss.png")
    relentless_offCD = matchMyTemplate(config.RELENTLESS_TEMPLATE, matchImg, True)

    if relentless_offCD is None:
        print("relentless_offCD not found, on CD?")

    print("Found:")
    print(relentless_offCD)
    # region_img = screenshot(example_region)

    if relentless_offCD:
        current_time = time.time()
        print(current_time)
        # recast_relentless()
    else:
        print("pretend this is holding alt")


    current_time = time.time()

    # test action every 5 seconds
    if current_time - last_action > 5:

        # send_key("THREE")
        
        last_action = current_time
    
    #reset pattern matching (copy later if need coords)
    relentless_offCD = None
    time.sleep(1)