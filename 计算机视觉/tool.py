import numpy as np
import os
from PIL import Image
from imageio import imsave
from scipy.ndimage import filters


class ImageTool(object):
    @staticmethod
    def get_img_list(path: str):
        return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]

    @staticmethod
    def image_denoise(img, U_init, tolerance=0.1, tau=0.125, tv_weight=100):
        """
        :param img: 灰度图像
        :param U_init: 返回图像的初始值
        :param tolerance: 停止条件
        :param tau: 步长
        :param tv_weight: tv正则项权值
        :return: 去噪和去除纹理的图像
        ROF (Rudin-Osher-Fatemi)去噪模型, 使处理后的图像更平滑，同 时保持图像边缘和结构信息
            @ 一幅(灰度)图像 I 的全变差(Total Variation，TV)定义为梯度范数之和
                J(I)=∫∣▽𝐼∣𝑑𝑥
              离散表示为：
                𝐽(𝐼)=∑𝑥∣▽𝐼∣
              在所有坐标x = [x, y]中取和
              模型中， 目标函数寻找降噪后的图像U，使得下列等式最小：
                𝑚𝑖𝑛(𝑈)‖𝐼−𝑈‖2+2𝜆𝐽(𝑈)
              其中范数|| I - U || 是去噪后图像 U 和原始图像 I 差异的度量
        """
        m, n = img.shape
        Px, Py, U, error = img, img, U_init, 1

        while error > tolerance:
            Uold = U
            # 变量U梯度的x分量，y分量
            GradUx = np.roll(U, -1, axis=1) - U
            GradUy = np.roll(U, -1, axis=0) - U

            # 更新x,y的对偶
            PxNew = Px + (tau / tv_weight) * GradUx
            PyNew = Py + (tau / tv_weight) * GradUy
            NormNew = np.maximum(1, np.sqrt(PxNew ** 2 + PyNew ** 2))

            Px, Py = PxNew / NormNew, PyNew / NormNew

            # 对分量分别向各自的右方向轴平移
            RxPx = np.roll(Px, 1, axis=1)
            RyPy = np.roll(Py, 1, axis=0)

            # 对偶的散度
            DivP = (Px - RxPx) + (Py - RyPy)
            U = img + tv_weight * DivP

            # 更新误差
            error = np.linalg.norm(U - Uold) / np.sqrt(n * m)

        return U, img - U


class ImageScreenshot(object):
    def __init__(self, path: str, out_path: str):
        self.out_path = out_path
        self.image = Image.open(path)

    def cut(self, x1: int, y1: int, x2: int, y2: int):
        img_tailoring = self.image.crop((x1, y1, x2, y2))
        im = np.array(img_tailoring)
        imsave(self.out_path, im)


def Test_denoise():
    im = np.zeros((500, 500))
    im[100:400, 100:400] = 128
    im[200:300, 200:300] = 255
    im = im + 30 * np.random.standard_normal((500, 500))

    U, T = ImageTool.image_denoise(im, im)
    G = filters.gaussian_filter(im, 10)

    imsave('synth_rof.t.jpg', U)
    imsave('synth_gaussian.t.jpg', G)


if __name__ == "__main__":
    # Test_denoise()
    # cut imgae
    path1 = "原始图片.jpeg"
    out_path1 = "cut.jpg"
    ImageScreenshot(path=path1, out_path=out_path1).cut(0, 0, 200, 200)