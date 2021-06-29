"""
    @郭泽嘉
        - DensityMap 用于计算布匹密度, 附加相关的测试方法
        【注意】: 本方法若直接调用,需注意径向纬向的区别
"""
import sys
import json
import numpy as np
from cv2 import cv2
from matplotlib import pyplot as plt

from scipy.signal import find_peaks, argrelextrema


class W(object):

    def __init__(self):
        self.points: list = []
        # 最大值
        self.highest_value: int = 0
        self.min_value: int = sys.maxsize
        # 三个峰值点和两个谷底点平均差
        self._peaks_diff: float = 0
        self._valleys_diff: float = 0
        # 两个峰值之间的距离
        self.distance_1: int = 0
        self.distance_2: int = 0

    @property
    def peaks_diff(self):
        return self._peaks_diff

    @property
    def valleys_diff(self):
        return self._valleys_diff

    @property
    def distamce1(self):
        return self.distance_1

    @property
    def distamce2(self):
        return self.distance_2

    def __str__(self):
        data = {
            "points": self.points,
            "extremum": (float(self.min_value), float(self.highest_value)),
            "peaks_diff": float(self.peaks_diff),
            "valleys_diff": float(self.valleys_diff),
            "distance": (float(self.distance_1), float(self.distance_2))
        }
        return json.dumps(data, indent=4)

    def __set_diffs(self):
        """
         三个峰值点和两个谷底点平均差，累加平均值和原值之差的绝对值
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
        ys = sorted(ys)
        self.distance_1 = abs(ys[0] - ys[2])
        self.distance_2 = abs(ys[2] - ys[4])

    def _set(self):
        if len(self.points) < 5:
            return
        self.__set_diffs()
        self.__set_distance()

    def add(self, point: (int, float)):
        """
        定义业务规则,只允许传入五个值，分别为两个低点，三个最高点
        即：
            a1          a2          a3
              -       -   -       -
                -   -       -   -
                  b1          b2
        """
        self.points.append((float(point[0]), float(point[1])))
        x, y = point[0], point[1]
        if y >= self.highest_value:
            self.highest_value = y
        if y <= self.min_value:
            self.min_value = y

        self._set()

    def is_correct(self) -> bool:
        if len(self.points) >= 5:
            return True
        return False


class DensityMap(object):

    def __str__(self):
        return """计算密度的类,用于计算相关的二维图谱、差分计算"""

    def __init__(self, image: np.ndarray):
        """
        :param image: 二维的行列式, 像素尽可能控制在200 * 100 以内
        """
        self.image: np.ndarray = image
        self.x: int = image.shape[1]
        self.y: int = image.shape[0]
        self.__init()

    def __init(self):
        # xx 为一组一维数组，长度为图片横向宽度,内容为一组有序列表
        self.xx = np.zeros(self.x)
        for item in range(self.x):
            self.xx[item] += item

        # Radial 为一组一维数组，长度为图像的横向框度, 内容为径向方向的累加
        self.radial_count = np.zeros(self.x)
        for item in range(self.y):
            self.radial_count += self.image[item]

        self.avg = np.mean(self.radial_count)
        self.avg_list = self.avg * np.ones(self.x)

        # 峰值点
        self.peaks, _ = find_peaks(self.radial_count, height=0)
        # 峰谷点
        self.valleys = argrelextrema(-self.radial_count, np.greater)[0]

        # 滤波
        peaks, valleys = set(self.peaks), set(self.valleys)
        for p in self.peaks:
            if p-1 in valleys or p+1 in valleys:
                if ((self.radial_count[p] - self.radial_count[p-1]) / self.radial_count[p]) < 0.1:
                    peaks = peaks - {p}
                    valleys = valleys - {p-1}
                elif ((self.radial_count[p] - self.radial_count[p + 1]) / self.radial_count[p]) < 0.1:
                    peaks = peaks - {p}
                    valleys = valleys - {p + 1}

        self.peaks, self.valleys = np.array(sorted(peaks)), np.array(sorted(valleys))

    def __high_and_low_peaks(self) -> list:
        """
        寻找`W`
        """
        Ws: list = []
        w = W()
        peaks_num, valleys_num = 0, 0

        # valleys_data = self.radial_count[self.valleys]
        # peaks_data = self.radial_count[self.peaks]

        while peaks_num <= len(self.peaks) - 2 or valleys_num <= len(self.valleys) - 2:
            if w.is_correct():
                Ws.append(w)
                w = W()
            try:
                w.add(point=(self.peaks[peaks_num], self.radial_count[self.peaks[peaks_num]]))
                if peaks_num <= len(self.peaks) - 3:
                    w.add(point=(self.peaks[peaks_num + 1], self.radial_count[self.peaks[peaks_num + 1]]))
                    w.add(point=(self.peaks[peaks_num + 2], self.radial_count[self.peaks[peaks_num + 1]]))

                w.add(point=(self.valleys[valleys_num], self.radial_count[self.valleys[valleys_num]]))
                if valleys_num <= len(self.valleys) - 2:
                    w.add(point=(self.valleys[valleys_num + 1], self.radial_count[self.valleys[valleys_num + 1]]))
            except:
                pass
            valleys_num += 2
            peaks_num += 2
        return Ws

    def get_density(self):
        ws = self.__high_and_low_peaks()
        data = []

        distance_avg = 0
        for i in ws:
            distance_avg += (i.distamce1 + i.distamce2) / 2
        distance_avg = distance_avg / len(ws)
        print(distance_avg, "平均值")

        t = np.zeros(len(ws) * 2)
        num = 0
        for i in ws:
            t[num] += i.distamce1
            t[num+1] += i.distamce2
            num += 2
        print(np.std(t), "标准差")

        for i in ws:
            if distance_avg * 0.4 < i.distamce1 < distance_avg * 1.2 and distance_avg * 0.4 < i.distamce2 < distance_avg * 1.2:
                data.append({
                    "diff": i.peaks_diff + i.valleys_diff,
                    "distance": (i.distamce1 + i.distamce2) / 2,
                })

        data.sort(key=lambda distance: distance["distance"])
        data_len = len(data)

        data = data[int(data_len * .33): int(data_len - data_len * .33)]

        # data.sort(key=lambda diff: diff["diff"])

        density = 0
        for i in data:
            density += i["distance"]
        return density / len(data)


class DensityMapTool(DensityMap):
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

    def write_2D(self, out_path: str):
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.x)

        # 原始数据
        ax.plot(self.xx, self.radial_count, lw=1, label=u"data")
        ax.plot(self.avg_list, "--", color="gray", lw=1)

        # 峰值点
        ax.plot(self.peaks, self.radial_count[self.peaks], "x", color="red", label='peaks')

        # 峰谷点
        ax.plot(self.valleys, self.radial_count[self.valleys], "o", color="green", label="valleys")

        # 移动平均
        N = 5
        sma = self.__sma(self.radial_count, N=N)
        ax.plot(self.xx[N - 1:], sma, lw=1, label=u"avg")

        miloc = plt.MultipleLocator(5)
        ax.xaxis.set_minor_locator(miloc)
        ax.grid(axis='x', which='minor')
        fig.savefig(out_path)


if __name__ == "__main__":

    # for item in range(1, 5):
    #     print("-" * 20)
    #     path = f"test2/t2-{item}.png"
    #     img = cv2.imread(path, 0)
    #     a = DensityMapTool(image=img)
    #     a.write_2D(out_path=f"test2/t2-{item}-2D.png")
    #     print(path, ":", a.get_density())
    # for item in range(1, 7):
    #     print("-"*20)
    #     path = f"test2/t1-{item}.png"
    #     img = cv2.imread(path, 0)
    #     a = DensityMapTool(image=img)
    #     # a.write_2D(out_path=f"test2/t1-{item}-2D.png")
    #     print(path, ":", a.get_density())

    # path = "test_img/test-re-12.png"
    # # path = "test_img/test-re-8.png"
    # path = "test2/t1-1.png"
    # path = "test_img/test-re-10.png"
    path = "test3/t1.png"

    img = cv2.imread(path, 0)
    a = DensityMapTool(image=img)
    a.write_2D(out_path="test3/test-out.png")
    a.get_density()
