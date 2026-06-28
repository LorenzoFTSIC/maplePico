import mss
import numpy as np

sct = mss.mss()

def screenshot(region):
    return np.array(sct.grab(region))[:, :, :3]


