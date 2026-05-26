import time
import board
import digitalio
import usb_hid
import random
import usb_cdc

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode



#functions
def run_rotation(elapsed):

    global holding_a

    # HOLD A: 0-5 seconds
    if 0 <= elapsed < breakpoints[0]:

        if not holding_a:
            kbd.press(Keycode.RIGHT_ALT)
            holding_a = True
        # print("holding ralt")

    # SPAM B: 5-6 seconds
    elif breakpoints[0] <= elapsed < breakpoints[1]:

        if holding_a:
            kbd.release_all()
            holding_a = False
        # print("pausing for lockout")

        #kbd.press(Keycode.B)
        #kbd.release_all()

        time.sleep(0.05)

    # HOLD A AGAIN: 6-10 seconds
    elif breakpoints[1] <= elapsed < breakpoints[2]:

        if not holding_a:
            kbd.press(Keycode.RIGHT_ALT)
            holding_a = True
        # print("holding ralt again")
            
    elif breakpoints[2] <= elapsed < breakpoints[3]:
        
        if holding_a:
            kbd.release_all()
            holding_a = False
        # print("recasting boundless")
            
        kbd.press(Keycode.THREE)
        kbd.release_all()
        time.sleep(0.05)

def randomBreakpoints(breakpoints):

    for i in range(0, len(breakpoints)):
        if i > 0:
            current = breakpoints[i]
            previous = breakpoints[i - 1]

            # Maximum downward movement allowed
            min_offset = (previous - current) + 0.07

            # Randomize while guaranteeing ordering
            offset = random.uniform(min_offset, 0.2)

            breakpoints[i] = current + offset
            #print("Breakpoint: " + str(i))
            #print(breakpoints[i])
        elif i == 0:
            breakpoints[i] = breakpoints[i] + random.uniform(-0.2, 0.2)
            #print("Breakpoint: " + str(i))
            #print(breakpoints[i])
        else:
            print("breakpoint index not found")

    return breakpoints
        
kbd = Keyboard(usb_hid.devices)
serial = usb_cdc.data

# start stop toggle button on GP15
toggleButton = digitalio.DigitalInOut(board.GP15)
toggleButton.direction = digitalio.Direction.INPUT
toggleButton.pull = digitalio.Pull.UP

# pause button on GP14
pauseButton = digitalio.DigitalInOut(board.GP14)
pauseButton.direction = digitalio.Direction.INPUT
pauseButton.pull = digitalio.Pull.UP

# LED on GP16
led = digitalio.DigitalInOut(board.GP16)
led.direction = digitalio.Direction.OUTPUT

# Farming toggle
farming = False

last_toggleButton = True

farm_start_time = 0
lastprint = -1

# track held state
holding_a = False

paused = False

last_pauseButton = True

pause_start_time = 0
total_paused_time = 0


# time breakpoints
base_breakpoints = [46, 46.2, 98, 101]
#testing breakpoint
#breakpoints = [5, 5.2, 10, 11]

last_elapsed = 0

breakpoints = randomBreakpoints(base_breakpoints.copy())


while True:
    # listen for serial commands
    if serial.in_waiting > 0:

        command = serial.readline().decode("utf-8", errors="ignore").strip().upper()

        print("RX:", command)

        if "TOGGLE" in command:
            farming = not farming
            print("FARMING:", farming)

            if farming:
                farm_start_time = time.monotonic()
                last_elapsed = 0
                breakpoints = randomBreakpoints(base_breakpoints.copy())
            else:
                kbd.release_all()
                holding_a = False

        elif "PAUSE" in command:
            paused = not paused
            print("PAUSE:", paused) 


    current_toggleButton = toggleButton.value
    
    current_pauseButton = pauseButton.value

    # detect new pause button press
    if last_pauseButton and not current_pauseButton and farming:

        paused = not paused

        time.sleep(0.2)

    last_pauseButton = current_pauseButton
    
    
    # detect new button press
    if last_toggleButton and not current_toggleButton:

        farming = not farming

        if farming:
            farm_start_time = time.monotonic()
            last_elapsed = 0

        else:
            # release everything when stopping
            kbd.release_all()
            holding_a = False

        time.sleep(0.2)

    last_toggleButton = current_toggleButton

    led.value = farming

    if farming and not paused:
        
        
        current_time = time.monotonic()
        elapsed = (current_time - farm_start_time) % breakpoints[3]

        # detect new cycle 
        if elapsed < last_elapsed:

            print("NEW ROTATION")
            breakpoints = randomBreakpoints(base_breakpoints.copy())
            print("New breakpoints:", breakpoints)
        
        last_elapsed = elapsed

        rounded = round(elapsed, 1)

        if rounded != lastprint:
            print("Rotation:", rounded)
            lastprint = rounded

        run_rotation(elapsed)
        # randomBreakpoints(breakpoints)

    time.sleep(0.01)