from PIL import Image
from pylab import *
import numpy as np
from scipy.ndimage import filters

base_img = np.array(Image.open("../images/原始图片.jpeg").convert("L"))
img_vague = filters.gaussian_filter(base_img, 5)

figure()
gray()
img_vague_1 = contour(img_vague, origin='image')
show()
