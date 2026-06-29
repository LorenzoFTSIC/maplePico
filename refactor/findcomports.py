from serial.tools import list_ports

for p in list_ports.comports():
    print("DEVICE:", p.device)
    print("DESC:", p.description)
    print("VID:", p.vid)
    print("PID:", p.pid)
    print("----")