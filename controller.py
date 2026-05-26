import serial
import keyboard
import time
from serial.tools import list_ports

pico_port = None

# Find the Pico automatically
for port in list_ports.comports():

    print(port.device, port.description)

    if "CircuitPython CDC data" in port.description:
        pico_port = port.device
        break

if pico_port is None:
    raise Exception("Pico not found")

# Connect to Pico
pico = serial.Serial(pico_port, 115200)

# Give serial connection time to initialize
time.sleep(2)

print("Ready.")
print("Press [ to toggle farming")
print("Press ] to pause")


# Toggle farming
def toggle():
    pico.write(b"TOGGLE\n")
    print("Toggle sent")


# Pause farming
def pause():
    pico.write(b"PAUSE\n")
    print("Pause sent")


# Register hotkeys
keyboard.add_hotkey("[", toggle)
keyboard.add_hotkey("]", pause)

# Keep script alive forever
keyboard.wait()