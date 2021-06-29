from PIL import Image
import pylab as plt
import numpy as np
from scipy.ndimage import filters

img = np.array(Image.open("../images/原始图片.jpeg"))
img2 = np.zeros(img.shape)

for i in range(3):
    img2[:, :, i] = filters.gaussian_filter(img[:, :, i], 5)

plt.imshow(img2)
plt.axis('off')
plt.savefig("./彩色模糊.jpg")
plt.show()