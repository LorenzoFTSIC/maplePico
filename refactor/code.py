# Pi Pico controller
# Mimics the inputs received from the main controller

import time
import usb_cdc
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

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

while True:

    if serial.in_waiting > 0:

        command = serial.readline().decode().strip().upper()

        print("RX:", command)

        parts = command.split()

        if len(parts) == 1:

            if parts[0] == "RELEASE_ALL":
                kbd.release_all()

        elif len(parts) == 2:

            action = parts[0]
            key = parts[1]

            if key not in KEY_MAP:
                print("Unknown key:", key)
                continue

            keycode = KEY_MAP[key]

            if action == "PRESS":
                kbd.press(keycode)

            elif action == "RELEASE":
                kbd.release(keycode)

            elif action == "TAP":
                kbd.press(keycode)
                kbd.release(keycode)

            else:
                print("Unknown action:", action)

    time.sleep(0.01)