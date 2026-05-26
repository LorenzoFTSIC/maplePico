import usb_cdc
import time

serial = usb_cdc.data

while True:
    if serial.in_waiting > 0:
        msg = serial.readline()
        print("GOT:", msg)

    time.sleep(0.1)