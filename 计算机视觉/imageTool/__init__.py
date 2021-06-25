import os

import numpy as np
from PIL import Image
from imageio import imsave

from .gray_processing import GrayProcessing
from .enhance import Enhance


class ImageTool(GrayProcessing, Enhance):
    @staticmethod
    def get_img_list(path: str):
        return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]

    @staticmethod
    def img_screenshot(path: str, out_path: str, x1: int, y1: int, x2: int, y2: int):
        image = Image.open(path)
        img_tailoring = image.crop((x1, y1, x2, y2))
        im = np.array(img_tailoring)
        imsave(out_path, im)
