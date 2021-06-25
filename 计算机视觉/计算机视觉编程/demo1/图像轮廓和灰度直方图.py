from PIL import Image
from pylab import *

img_1 = Image.open("../images/原始图片.jpeg")

im = array(img_1.convert("L"))

figure()
gray()

contour(im, origin='image')
axis('equal')
axis('off')

figure()
hist(im.flatten(), 128)
show()

