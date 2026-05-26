import serial
import time

pico = serial.Serial("COM5", 115200, timeout=1)
time.sleep(2)

pico.write(b"TOGGLE\n")
print("sent")