import mss
import numpy as np

def screenshot(region):
    with mss.mss() as sct:
        return np.array(sct.grab(region))[:, :, :3]