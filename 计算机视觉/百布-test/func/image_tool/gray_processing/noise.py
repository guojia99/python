"""
    增噪
"""
from cv2 import cv2
import numpy as np
from imageio import imsave


class ImageNoise(object):
    @staticmethod
    def SaltPepper(path: str, outpath: str, percetage: float):
        img = cv2.imread(path)
        out = img.copy()
        salt_pepper = int(percetage * img.shape[0] * img.shape[1])
        for i in range(salt_pepper):
            randR = np.random.randint(0, img.shape[0] - 1)
            randG = np.random.randint(0, img.shape[1] - 1)
            randB = np.random.randint(0, 3)
            out[randR, randG, randB] = 255
            if np.random.randint(0, 1) == 0:
                out[randR, randG, randB] = 0
        im = np.array(out)
        imsave(outpath, im)

