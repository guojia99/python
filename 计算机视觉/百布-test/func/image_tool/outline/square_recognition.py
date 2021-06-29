from cv2 import cv2 as cv
import numpy as np


def Get_angle_cos(p0, p1, p2: float) -> float:
    """
    三点两线，求夹角
    :return: 返回余弦值
    """
    d1 = (p0 - p1).astype('float')
    d2 = (p2 - p1).astype('float')
    return abs(np.dot(d1, d2) / np.sqrt(np.dot(d1, d1) * np.dot(d2, d2)))


class SquaresImage(object):

    @staticmethod
    def squares_1(image: np.ndarray, is_close: bool = True, closure_length: float = 0.04, max_cos: float = 0.3) -> list:
        """
        简单的高斯处理后通过canny获取图像中的矩形点的列表
        返回的列表为：[np.array{[x1,y1], [x2,y2], [x3,y3] ,[x4,y4]]
        """
        squares = []

        img = cv.GaussianBlur(image, (3, 3), 0)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        bins = cv.Canny(gray, 100, 200, apertureSize=3)
        contours, _ = cv.findContours(bins, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        index = 0
        for cnt in contours:
            cnt_len = cv.arcLength(cnt, True)
            cnt = cv.approxPolyDP(cnt, closure_length * cnt_len, is_close)

            if len(cnt) == 4 and cv.contourArea(cnt) and cv.isContourConvex(cnt):
                cnt = cnt.reshape(-1, 2)
                max_cos_v = np.max([Get_angle_cos(p0=cnt[i], p1=cnt[(i + 1) % 4], p2=cnt[(i + 2) % 4]) for i in range(4)])
                if max_cos_v <= max_cos:
                    # if True:
                    index += 1
                    squares.append(cnt)
        return squares
