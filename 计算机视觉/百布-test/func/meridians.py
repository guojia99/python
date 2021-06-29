from cv2 import cv2
import numpy as np
from matplotlib import pyplot as plt
import csv

class Meridians(object):
    def __init__(self, path: str):
        self.image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        self.shape = self.image.shape
        self.__set_zeros_xy()

    def __set_zeros_xy(self):
        self.xx, self.yy = np.zeros(self.shape[0]), np.zeros(self.shape[1])
        for item in range(self.shape[0]):
            self.xx[item] += item
        for item in range(self.shape[1]):
            self.yy[item] += item

        self.X, self.Y = np.meshgrid(self.xx, self.yy)

    def write_3D(self, out_path: str):
        plt.figure()
        ax3 = plt.axes(projection='3d')
        ax3.plot_surface(self.X, self.Y, self.image, rstride=1, cstride=1, cmap='rainbow')
        plt.savefig(out_path)

    def write_2D(self, out_path: str):
        w = 197
        h = 40
        fig, ax = plt.subplots()
        ax.set_xlim(0, w)

        xx = np.zeros(w)
        for item in range(w):
            xx[item] += item

        m = np.zeros(w)
        for item in range(h):
            m += self.image[item]
        ax.plot(xx, m)

        # with open('re13.csv', 'w') as f:
        #     for item in m:
        #         f.write(f"{item},")
        #     f.close()

        miloc = plt.MultipleLocator(1)
        ax.xaxis.set_minor_locator(miloc)
        ax.grid(axis='x', which='minor')
        fig.savefig(out_path)

    def write_2D_ww(self, out_path: str):
        m = np.zeros(self.shape[0])


if __name__ == "__main__":
    # m = Meridians(path="image/test3.png")
    # m.write_3D(out_path="image/test3-3D.png")
    m_r1 = Meridians(path="image/test-re-10-2.png")
    m_r1.write_2D(out_path="image/test_re10-2.png")
