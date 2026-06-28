import time
import serial

import config


class Pico:

    def __init__(self):

        self.serial = serial.Serial(
            config.PICO_PORT,
            config.BAUD_RATE
        )

        # CircuitPython time to reboot
        time.sleep(2)

    def _send(self, command):

        self.serial.write(f"{command}\n".encode())

        print("TX:", command)

    def press(self, key):

        self._send(f"PRESS {key}")

    def release(self, key):

        self._send(f"RELEASE {key}")

    def tap(self, key):

        self.press(key)
        self.release(key)

    def release_all(self):

        self._send("RELEASE_ALL")

    def close(self):

        self.serial.close()