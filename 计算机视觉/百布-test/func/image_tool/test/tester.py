from .. import ImageTool
from imageio import imsave
from scipy.ndimage import filters
import numpy as np


def test_img_screenshot():
    path1 = "原始图片.jpeg"
    out_path1 = "cut.jpg"
    ImageTool().img_screenshot(path=path1, out_path=out_path1, x1=0, y1=0, x2=200, y2=200)

def test_denoise():
    im = np.zeros((500, 500))
    im[100:400, 100:400] = 128
    im[200:300, 200:300] = 255
    im = im + 30 * np.random.standard_normal((500, 500))

    U, T = ImageTool().image_denoise(im, im)
    G = filters.gaussian_filter(im, 10)

    imsave('synth_rof.t.jpg', U)
    imsave('synth_gaussian.t.jpg', G)