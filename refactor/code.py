# Pi pico controller
# mimics the inputs recieved from the main controller
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
    "SPACE": Keycode.SPACE,
}

while True:

    if serial.in_waiting > 0:

        command = serial.readline().decode().strip().upper()



        print("RX:", command)

        if command in KEY_MAP:
            kbd.press(KEY_MAP[command])
            kbd.release(KEY_MAP[command])

        if command == "RELEASE_ALL":
            kbd.release_all()

    time.sleep(0.01)