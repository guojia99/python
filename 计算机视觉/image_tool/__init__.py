import os

import numpy as np
from cv2 import cv2
from PIL import Image
from imageio import imsave

from .gray_processing import GrayProcessing  # 灰度处理
from .enhance import Enhance  # 图像增强
from .outline import Outline  # 边缘识别


class ImageTool(GrayProcessing, Enhance, Outline):
    @staticmethod
    def get_img_list(path: str):
        return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg') or f.endswith('.png')]

    @staticmethod
    def img_screenshot(path: str, out_path: str, x1: int, y1: int, x2: int, y2: int):
        image = Image.open(path)
        img_tailoring = image.crop((x1, y1, x2, y2))
        im = np.array(img_tailoring)
        imsave(out_path, im)

    @staticmethod
    def get_image_var(path: str) -> float:
        image = cv2.imread(path)
        image2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.Laplacian(image2gray, cv2.CV_64F).var()
