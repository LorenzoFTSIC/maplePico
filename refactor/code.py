import time
import usb_cdc
import usb_hid
import board
import digitalio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# LED on GP16
led = digitalio.DigitalInOut(board.GP16)
led.direction = digitalio.Direction.OUTPUT

# Stop button on GP15
stopButton = digitalio.DigitalInOut(board.GP15)
stopButton.direction = digitalio.Direction.INPUT
stopButton.pull = digitalio.Pull.UP

# Pause button on GP14
pauseButton = digitalio.DigitalInOut(board.GP14)
pauseButton.direction = digitalio.Direction.INPUT
pauseButton.pull = digitalio.Pull.UP

kbd = Keyboard(usb_hid.devices)
serial = usb_cdc.data

KEY_MAP = {
    "A": Keycode.A,
    "B": Keycode.B,
    "THREE": Keycode.THREE,
    "FOUR": Keycode.FOUR,
    "SPACE": Keycode.SPACE,
    "RIGHT_ALT": Keycode.RIGHT_ALT,
}

stopButton_prev = True
pauseButton_prev = True
paused = False

while True:

    #  Stop button (falling edge) 
    stopButton_state = stopButton.value
    if not stopButton_state and stopButton_prev:
        kbd.release_all()
        serial.write(b"STOP\n")
        led.value = True
        time.sleep(0.5)
        led.value = False
    stopButton_prev = stopButton_state

    #  Pause button (falling edge toggles pause) 
    pauseButton_state = pauseButton.value
    if not pauseButton_state and pauseButton_prev:
        paused = not paused
        if paused:
            kbd.release_all()
            serial.write(b"PAUSE\n")
            led.value = True   # LED on while paused
        else:
            serial.write(b"RESUME\n")
            led.value = False
    pauseButton_prev = pauseButton_state

    #  serial commands 
    if serial.in_waiting > 0:
        command = serial.readline().decode().strip().upper()
        print("RX:", command)

        parts = command.split()

        if paused:
            pass
        else:
            led.value = True

            if len(parts) == 1:
                if parts[0] == "RELEASE_ALL":
                    kbd.release_all()

            elif len(parts) == 2:
                action = parts[0]
                key = parts[1]

                if key not in KEY_MAP:
                    print("Unknown key:", key)
                    led.value = False
                    continue

                keycode = KEY_MAP[key]

                if action == "PRESS":
                    kbd.press(keycode)
                elif action == "RELEASE":
                    kbd.release(keycode)
                elif action == "TAP":
                    kbd.press(keycode)
                    time.sleep(0.13)
                    kbd.release(keycode)
                else:
                    print("Unknown action:", action)

            led.value = False

    time.sleep(0.1)