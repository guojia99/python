"""
    @ 郭泽嘉,zjguo
        - Density It is used to calculate the cloth density and add relevant test methods
            Note: if this method is called directly, the difference between radial and latitudinal directions should be noted
        - Density 用于计算布匹密度, 附加相关的测试方法, 注意: 本方法若直接调用,需注意径向纬向的区别
"""

import sys

import json
import numpy as np
from cv2 import cv2

from matplotlib import pyplot as plt
from scipy.signal import find_peaks, argrelextrema


def enhance_hist(image: np.ndarray) -> np.ndarray:
    """
    基于直方图均衡化，将一副图像的直方图分布变成近似均匀分布，从而增强图像的对比度。
    https://zhuanlan.zhihu.com/p/44918476
    """
    r, g, b = cv2.split(image)
    r1 = cv2.equalizeHist(r)
    g1 = cv2.equalizeHist(g)
    b1 = cv2.equalizeHist(b)
    image_equal_clo = cv2.merge([r1, g1, b1])
    return image_equal_clo


class Settings(object):
    def __init__(self):
        self.distance_symmetric: float = .25
        self.std: float = .5


class W(object):
    """
    `W`It is defined as two high and low peaks
    Define business rules. Only five values can be passed in,
    which are two low points and three high points。
    定义业务规则,只允许传入五个值，分别为两个低点，三个最高点：
            a1          a2          a3
              -       -   -       -
                -   -       -   -
                  b1          b2
    """

    def __init__(self):
        self.points: list = []
        self._highest_value: float = 0
        self._min_value: float = sys.maxsize
        # Average difference of three peak points and two valley points
        self._peaks_diff: float = 0
        self._valleys_diff: float = 0
        # 两个峰值之间的距离
        self._distance_1: float = 0
        self._distance_2: float = 0
        # 距离权重
        self._distance_w: float = sys.maxsize

    @property
    def peaks_diff(self):
        return float(self._peaks_diff)

    @property
    def valleys_diff(self):
        return float(self._valleys_diff)

    @property
    def distamce1(self):
        return float(self._distance_1)

    @property
    def distamce2(self):
        return float(self._distance_2)

    @property
    def distamce(self):
        return (self.distamce1 + self.distamce2) / 2

    @property
    def min_value(self):
        return float(self._min_value)

    @property
    def highest_value(self):
        return float(self._highest_value)

    @property
    def distance_w(self):
        return float(self._distance_w)

    def __str__(self) -> str:
        data = {
            "points": self.points,
            "extremum": (self.min_value, self.highest_value),
            "peaks_diff": self.peaks_diff,
            "valleys_diff": self.valleys_diff,
            "distance": (self.distamce1, self.distamce2)
        }
        return json.dumps(data)

    def __set_diffs(self):
        """
         The absolute value of the difference between the average of three peak points and two trough points,
         and the difference between the accumulated average and the original value。
         三个峰值点和两个谷底点平均差，累加平均值和原值之差的绝对值。
             3
             ∑  |(avg-yi)|
             i=1
        """
        ys = []
        for item in self.points:
            ys.append(item[1])
        ys = sorted(ys)
        peak_avg, valleys_avg = np.mean(ys[-3:]), np.mean(ys[:2])

        for item in ys[-3:]:
            self._peaks_diff += abs(item - peak_avg)

        for item in ys[:2]:
            self._valleys_diff += abs(item - valleys_avg)

    def __set_distance(self):
        ys = []
        for item in self.points:
            ys.append(item[0])
        """
        The sorting is based on horizontal coordinate, non value, 
        even if the value after sorting conforms to a high and low height。
        排序依据为横坐标，非值，即使得排序完的值符合一个高低高。
        """
        ys = sorted(ys)
        self._distance_1 = abs(ys[0] - ys[2])
        self._distance_2 = abs(ys[2] - ys[4])

    def _set(self):
        if len(self.points) < 5:
            return
        self.__set_diffs()
        self.__set_distance()

    def is_full(self):
        if len(self.points) >= 5:
            return True
        return False

    def is_distance_symmetric(self) -> bool:
        # Judge whether it is symmetrical or not
        self._distance_w = abs(self._distance_2 - self._distance_1) / (self._distance_1 + self._distance_2)
        if self._distance_w <= Settings().distance_symmetric:
            return True
        return False

    def add(self, point: (int, float)):
        self.points.append((float(point[0]), float(point[1])))
        x, y = point[0], point[1]
        if y >= self.highest_value:
            self._highest_value = y
        if y <= self.min_value:
            self._min_value = y
        self._set()


class Ws(object):
    def __init__(self):
        self.q = []

    def __len__(self):
        return len(self.q)

    def add(self, w: W):
        self.q.append(w)

    def set_init(self):
        self.avg = 0
        for i in self.q:
            self.avg += (i.distamce1 + i.distamce2) / 2
        self.avg = self.avg / len(self)

        std_list = np.zeros(len(self) * 2)
        num = 0
        for item in self.q:
            std_list[num] += item.distamce1
            std_list[num + 1] += item.distamce2
            num += 2
        self.std = np.std(std_list)
        self.big_std = self.std + self.avg

        new_ws = []
        for item in self.q:
            if item.distamce1 < self.big_std or item.distamce2 < self.big_std:
                new_ws.append(item)
        self.q = new_ws
        del new_ws

    def get_density(self) -> float:
        self.set_init()
        if self.std >= self.avg * Settings().std:
            return -1

        data = []
        for item in self.q:
            err = item.is_distance_symmetric
            if err:
                data.append(item)

        if len(data) <= 1:
            return -1
        data.sort(key=lambda dw: dw.distance_w)

        if len(data) > 10:
            data = data[:10]

        density = 0
        for i in data:
            density += i.distamce

        return density / float(len(data))


class Density(object):

    @staticmethod
    def __sma(data: np.ndarray, N: int = 5) -> np.ndarray:
        """
        :param data: 一维数据
        :param N: 权值，表示和前后多少位进行对比
        :return: 一个移动平均点函数
        """
        n = np.ones(N)
        weights = n / N
        sma = np.convolve(weights, data)[N - 1:-N + 1]
        return sma

    def __init__(self, image: np.ndarray):
        """
        :param image: 二维的行列式, 像素尽可能控制在50 * 120 以内, 为一个二值参，即灰度图
        """
        self.image: np.ndarray = image
        self.x: int = image.shape[1]
        self.y: int = image.shape[0]

        # 横坐标点
        self.xx = np.zeros(self.x)
        for item in range(self.x):
            self.xx[item] += item

        # 纵坐标点
        self.radial_count = np.zeros(self.x)
        for item in range(self.y):
            self.radial_count += self.image[item]

        self.avg = np.mean(self.radial_count)
        self.avg_list = self.avg * np.ones(self.x)

        # 峰值点
        self.peaks, _ = find_peaks(self.radial_count, height=0)

        # 峰谷点
        self.valleys = argrelextrema(-self.radial_count, np.greater)[0]
        if self.peaks[0] > self.valleys[0]:
            np.delete(self.valleys, 0)

    def __is_clear(self) -> bool:
        clear = cv2.Laplacian(self.image, cv2.CV_64F).var()
        if clear < 100:
            return False
        return True

    def write_2D(self, out_path: str):
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.x)

        # 原始数据
        ax.plot(self.xx, self.radial_count, lw=1, label=u"data")
        ax.plot(self.avg_list, "--", color="gray", lw=1)

        # 峰值点
        ax.plot(self.peaks, self.radial_count[self.peaks], "x", color="red", label='peaks')

        # 峰谷点
        ax.plot(self.valleys, self.radial_count[self.valleys], "+", color="green", label="valleys")

        # 移动平均
        N = 5
        sma = self.__sma(self.radial_count, N=N)
        ax.plot(self.xx[N - 1:], sma, lw=1, label=u"avg")

        miloc = plt.MultipleLocator(5)
        ax.xaxis.set_minor_locator(miloc)
        ax.grid(axis='x', which='minor')
        fig.savefig(out_path)

    def get(self) -> float:
        """
        get `W`
        """
        if not self.__is_clear():
            return -1
        ws: Ws = Ws()

        for num in range(len(self.peaks) - 2):
            w = W()
            if len(self.valleys) > num + 1:
                w.add(point=(self.valleys[num], self.radial_count[self.valleys[num]]))
                w.add(point=(self.valleys[num + 1], self.radial_count[self.valleys[num + 1]]))

            w.add(point=(self.peaks[num], self.radial_count[self.peaks[num]]))
            w.add(point=(self.peaks[num + 1], self.radial_count[self.peaks[num + 1]]))
            w.add(point=(self.peaks[num + 2], self.radial_count[self.peaks[num + 2]]))
            ws.add(w)
        data = ws.get_density()
        return data


class DensityTool(object):
    MAX_H = 40
    MAX_W = 120

    def __init__(self, image: np.ndarray, enhance: bool = False):
        """
        约定图像上下方向为经向，左右为纬向, 且像素值大于400 * 200
        image: np.ndarray = cv2.imread(path, 0)
        """
        if len(image.shape) >= 3:
            image = enhance_hist(image)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.image: np.ndarray = image
        self.image_rot: np.ndarray = np.rot90(self.image)
        self.meridians = -1
        self.broadwise = -1
        self.set_data()

    def __cut_image(self, image: np.ndarray) -> list:
        img_list = []
        x, y = image.shape[1], image.shape[0]

        if x < 400 or y < 200:
            raise ValueError("Image size is insufficient")

        w = int((x - self.MAX_W * 3) / 4)
        h = int((y - self.MAX_H * 3) / 4)

        for i in range(1, 4):
            for j in range(1, 4):
                img_list.append(image[h * j: h * j + self.MAX_H, w * i: w * i + self.MAX_W])

        return img_list

    def set_data(self):
        mer_cut = self.__cut_image(self.image)
        bro_cut = self.__cut_image(self.image_rot)

        self.mer_cut_data, self.bro_cut_data = [], []
        for item in mer_cut:
            data = Density(image=item).get()
            if data > 0:
                self.mer_cut_data.append(data)
            del data

        for item in bro_cut:
            data = Density(image=item).get()
            if data > 0:
                self.bro_cut_data.append(data)
            del data

        self.mer_cut_data = sorted(self.mer_cut_data)
        self.bro_cut_data = sorted(self.bro_cut_data)

        if len(self.mer_cut_data) >= 5:
            self.mer_cut_data = self.mer_cut_data[1: -2]

        if len(self.bro_cut_data) >= 5:
            self.bro_cut_data = self.bro_cut_data[1: -2]

        self.meridians = np.mean(self.mer_cut_data)
        self.broadwise = np.mean(self.bro_cut_data)

    def get(self) -> dict:
        data = {
            "meridians": self.meridians,
            "meridians_data": self.mer_cut_data,
            "meridians_std": np.std(self.mer_cut_data),
            "broadwise": self.broadwise,
            "broadwise_data": self.bro_cut_data,
            "broadwose_std": np.std(self.bro_cut_data),
        }
        return data


if __name__ == "__main__":
    path = "/Users/caime/Desktop/guojiafile/python/计算机视觉/百布-test/test.png"
    img = cv2.imread(path)
    d = DensityTool(image=img)
    print(d.get())

    # path = "test6/r1.png"
    # img: np.ndarray = cv2.imread(path)
    # cv2.imwrite("test6/yuantu.png", img)
    # img = enhance_hist(image=img)
    # cv2.imwrite("test6/ruihua.png", img)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # # img = np.rot90(img)
    #
    # d = DensityTool(imgae=img)
    # import json
    # data = d.get()
    # print(json.dumps(data, indent=4))
