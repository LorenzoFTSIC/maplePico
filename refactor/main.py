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

#cfg
PICO_PORT = None
BAUD_RATE = 115200

templateImg = "./ss/pc/relentless.png"
MATCH_THRESHOLD = 0.9

SCREEN_REGION = {
    "left": 0,
    "top": 0,
    "width": 2560,
    "height": 1440,
}

is_key_held = False
key_held = ""
sct = mss.mss()
last_action = 0

#serial stuff
# pico = serial.Serial(PICO_PORT, BAUD_RATE)
# time.sleep(2)

def send_key(key_name):
    pico.write(f"{key_name}\n".encode())
    print("TX:", key_name)



def screenshot(region):
    return np.array(sct.grab(region))[:, :, :3]


#template matching

def matchTemplate(templateImg, matchImg):

    template = cv2.imread(templateImg)
    if template is None:
        raise Exception(f"Could not load {templateImg}")


    result = cv2.matchTemplate(
        matchImg,
        template,
        cv2.TM_CCOEFF_NORMED
    )

    locations = np.where(result >= MATCH_THRESHOLD)

    matches = []

    h = template.shape[0]
    w = template.shape[1]

    for (x, y) in zip(locations[1], locations[0]):
        matches.append([int(x), int(y), int(w), int(h)])
        matches.append([int(x), int(y), int(w), int(h)])

    matches, weights = cv2.groupRectangles(matches, 1, 0.2)

    #for testing
    test_img = matchImg.copy()

    for (x, y, w, h) in matches:
        cv2.rectangle(
            test_img,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

    cv2.imshow("Template Match Debug", test_img)
    cv2.waitKey(0)  # 0 to hold 1 to update repeatedly?


    if len(matches) == 0:
        return None
    else:
        print(len(matches))
        print(matches)

    x, y, w, h = matches[0]

    return {
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "center_x": x + w // 2,
        "center_y": y + h // 2
    }

def jump_att(reps):
    for i in range(0, reps):
        print(f"rep{i}")

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
    # matchImg = screenshot(SCREEN_REGION)
    #static ss with relentless off CD
    matchImg = cv2.imread("./ss/pc/full.png")
    #static ss with relentless on CD and active
    # matchImg = cv2.imread("./ss/pc/bufffavss.png")
    relentless_offCD = matchTemplate(templateImg=templateImg, matchImg=matchImg)

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