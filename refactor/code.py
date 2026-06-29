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
button = digitalio.DigitalInOut(board.GP15)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP  # pressed = LOW

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

button_prev = True  # unpressed state (pull-up)

while True:

    # --- Button check ---
    button_state = button.value
    if not button_state and button_prev:  # falling edge = press
        kbd.release_all()
        serial.write(b"STOP\n")
        led.value = True
        time.sleep(0.5)
        led.value = False

    button_prev = button_state

    # --- Serial commands ---
    if serial.in_waiting > 0:

        command = serial.readline().decode().strip().upper()
        print("RX:", command)

        led.value = True

        parts = command.split()

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