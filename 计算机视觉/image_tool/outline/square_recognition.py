from util.util import *


class SquaresImage(object):

    @staticmethod
    def squares_1(Image: np.ndarray) -> list:
        """
        简单的高斯处理后通过canny获取图像中的矩形点的列表
        返回的列表为：[np.array{[x1,y1], [x2,y2], [x3,y3] ,[x4,y4]]
        """
        squares = []

        img = cv.GaussianBlur(Image, (3, 3), 0)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        bins = cv.Canny(gray, 100, 200, apertureSize=3)
        contours, _ = cv.findContours(bins, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        index = 0
        for cnt in contours:
            cnt_len = cv.arcLength(cnt, True)
            cnt = cv.approxPolyDP(cnt, 0.04 * cnt_len, True)

            if len(cnt) == 4 and cv.contourArea(cnt) and cv.isContourConvex(cnt):
                cnt = cnt.reshape(-1, 2)
                max_cos = np.max([Get_angle_cos(p0=cnt[i], p1=cnt[(i + 1) % 4], p2=cnt[(i + 2) % 4]) for i in range(4)])
                if max_cos < 0.1:
                    index += 1
                    squares.append(cnt)
        return squares
