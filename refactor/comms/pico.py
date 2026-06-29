import time
import threading
import serial
import config


class Pico:

    def __init__(self):
        self.serial = serial.Serial(
            config.PICO_PORT,
            config.BAUD_RATE,
            write_timeout=1.0
        )
        self._lock = threading.Lock()

        # CircuitPython time to reboot
        time.sleep(2)

    def _send(self, command):
        try:
            with self._lock:
                self.serial.write(f"{command}\n".encode())
            print("TX:", command)
        except serial.SerialTimeoutException:
            print(f"TX failed (timeout): {command}")
        except Exception as e:
            print(f"TX failed: {e}")

    def press(self, key):
        self._send(f"PRESS {key}")

    def release(self, key):
        self._send(f"RELEASE {key}")

    def tap(self, key):
        self._send(f"TAP {key}")

    def release_all(self):
        self._send("RELEASE_ALL")

    def close(self):
        try:
            self.serial.cancel_write()
        except Exception:
            pass
        try:
            self.serial.close()
        except Exception:
            pass