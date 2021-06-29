from cv2 import cv2
import numpy as np


class Density(object):
    def __init__(self, path: str):
        self.image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        self.shape = self.image.shape

    def __calculation_area(self, area: np.ndarray) -> list:
        """
        处理与计算某个区块的波峰
        :param area: 二维矩阵，长宽一致
        :return: 波峰点列表
        """
        m = np.zeros(len(area))
        for item in range(len(m)):
            m += area[item]







    def get_density(self):
        pass


