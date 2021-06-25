from PIL import Image
from numpy import *
from pylab import *


def histeq(im, nbr_bins=256):
    """ 对一幅灰度图像进行直方图均衡化 """
    # 计算图像的直方图
    imhist, bins = histogram(im.flatten(), nbr_bins, normed=True)
    cdf = imhist.cumsum()
    # cdf = 255 * cdf / cdf[-1] # 归一化
    im2 = interp(im.flatten(), bins[:-1], cdf)
    return im2.reshape(im.shape), cdf

img_2 = array(Image.open("../images/原始图片.jpeg").convert("L"))
im2, cdf = histeq(img_2)
figure()
gray()
contour(im2, origin='image')
axis('equal')
axis('off')
figure()
hist(im2.flatten(), 128)
show()