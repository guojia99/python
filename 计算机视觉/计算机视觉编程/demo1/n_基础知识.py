from PIL import Image
from ..images.settings import img_1

# 图像转灰度图
img_grayscale = img_1.convert("L")

# 创建缩略图, 将图片缩放为128 * 128
img_abbreviation = img_1.thumbnail((128, 128))

# 裁剪
img_tailoring = img_1.crop((100, 100, 400, 400))

# 粘贴区域, 把裁剪的区域旋转之后贴回去
img_region = img_tailoring.transpose(Image.ROTATE_180)
img_1.paste(img_region, (100, 100, 400, 400))

# 调整尺寸
adjust_img_size = img_1.resize((128, 128))

# 旋转
rotate = img_1.rotate(45)

