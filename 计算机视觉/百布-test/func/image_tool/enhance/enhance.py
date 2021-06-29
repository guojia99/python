from cv2 import cv2
import numpy as np


class ImageEnhance(object):
    """
        # image = cv2.imread("example.jpg")
    """
    @staticmethod
    def enhance_hist(image):
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

    @staticmethod
    def enhance_laplacian(image):
        """
        拉普拉斯算子,拉普拉斯算子是图像邻域内像素灰度差分计算的基础，通过二阶微分推导出的一种图像邻域增强算法。
        它的基本思想是当邻域的中心像素灰度低于它所在邻域内的其他像素的平均灰度时，此中心像素的灰度应该进一步降低；
        当高于时进一步提高中心像素的灰度，从而实现图像锐化处理。
        https://blog.csdn.net/weixin_42415138/article/details/108574657
        """
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        image_lap = cv2.filter2D(image, cv2.CV_8UC3, kernel)
        return image_lap

    @staticmethod
    def enhance_log(image):
        """
        对数变换，主要将用于图像的低灰度值部分拓展，高灰度值部分压缩，达到增强图像低灰度的目的。
        https://blog.csdn.net/D_turtle/article/details/79737873
        """
        image_log = np.uint8(np.log(np.array(image) + 1))
        cv2.normalize(image_log, image_log, 0, 255, cv2.NORM_MINMAX)
        # 转换成8bit图像显示
        cv2.convertScaleAbs(image_log, image_log)
        return image_log

    # 伽马变换
    @staticmethod
    def enhance_gamma(image):
        """
        伽马变换主要用于图像的校正，对灰度值过高（图像过亮）或者过低（图像过暗）的图像进行修正，增加图像的对比度，从而改善图像的显示效果。
        https://cloud.tencent.com/developer/article/1632433
        """
        fgamma = 2
        image_gamma = np.uint8(np.power((np.array(image) / 255.0), fgamma) * 255.0)
        cv2.normalize(image_gamma, image_gamma, 0, 255, cv2.NORM_MINMAX)
        cv2.convertScaleAbs(image_gamma, image_gamma)
        return image_gamma

    @staticmethod
    def enhance_clahe(image: np.ndarray) -> np.ndarray:
        """
        限制对比度自适应直方图均衡化CLAHE，普通的AHE往往会放大图像近恒定区域中的对比度，因为此类区域中的直方图高度集中。
        结果，AHE可能导致噪声在近恒定区域中被放大。对比度受限AHE（CLAHE）是自适应直方图均衡的一种变体，其中对比度放大受到限制，
        从而减少了这种噪声放大问题。
        https://blog.csdn.net/qq_43743037/article/details/107195117
        """
        b, g, r = cv2.split(image)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        b = clahe.apply(b)
        g = clahe.apply(g)
        r = clahe.apply(r)
        image_clahe = cv2.merge([b, g, r])
        return image_clahe


class ImageEnhanceRetinex(object):
    """
    Retinex 这个词由 Retina 和 Cortex 两个单词组成。在 Retinex 理论中，
    物体的颜色是由物体对长波、中波和短波光线的反射能力决定的，而不是由反射光强度的绝对值决定的，
    并且物体的色彩不受光照非均性的影响，具有一致性。
    https://www.jianshu.com/p/0723257de94f
    """

    @staticmethod
    def __replaceZeroes(data):
        min_nonzero = min(data[np.nonzero(data)])
        data[data == 0] = min_nonzero
        return data

    @staticmethod
    def __enhance_SSR(src_img, size):
        """
        SSR (Single Scale Retinex)即单尺度视网膜算法
        输入原始图像 I(x,y) 和滤波的半径范围 sigma;
        计算原始图像 I(x,y) 高斯滤波后的结果，得到 L(x,y);
        按照公式计算，得到 Log[R(x,y)]；
        将得到的结果量化为 [0, 255] 范围的像素值，然后输出结果图像。
        """
        L_blur = cv2.GaussianBlur(src_img, (size, size), 0)
        img = ImageEnhanceRetinex.__replaceZeroes(src_img)
        L_blur = ImageEnhanceRetinex.__replaceZeroes(L_blur)

        dst_Img = cv2.log(img / 255.0)
        dst_Lblur = cv2.log(L_blur / 255.0)
        dst_IxL = cv2.multiply(dst_Img, dst_Lblur)
        log_R = cv2.subtract(dst_Img, dst_IxL)

        dst_R = cv2.normalize(log_R, None, 0, 255, cv2.NORM_MINMAX)
        log_uint8 = cv2.convertScaleAbs(dst_R)
        return log_uint8

    @staticmethod
    def enhance_SSR_image(image):
        size = 3
        b_gray, g_gray, r_gray = cv2.split(image)
        b_gray = ImageEnhanceRetinex.__enhance_SSR(b_gray, size)
        g_gray = ImageEnhanceRetinex.__enhance_SSR(g_gray, size)
        r_gray = ImageEnhanceRetinex.__enhance_SSR(r_gray, size)
        result = cv2.merge([b_gray, g_gray, r_gray])
        return result

    # retinex MMR
    @staticmethod
    def __enhance_MSR(img, scales):
        """
        MSR (Multi-Scale Retinex)，即多尺度视网膜算法是在 SSR 算法的基础上提出的，采用多个不同的 sigma 值，
        然后将最后得到的不同结果进行加权取值
        """
        weight = 1 / 3.0
        scales_size = len(scales)
        h, w = img.shape[:2]
        log_R = np.zeros((h, w), dtype=np.float32)

        for i in range(scales_size):
            img = ImageEnhanceRetinex.__replaceZeroes(img)
            L_blur = cv2.GaussianBlur(img, (scales[i], scales[i]), 0)
            L_blur = ImageEnhanceRetinex.__replaceZeroes(L_blur)
            dst_Img = cv2.log(img / 255.0)
            dst_Lblur = cv2.log(L_blur / 255.0)
            dst_Ixl = cv2.multiply(dst_Img, dst_Lblur)
            log_R += weight * cv2.subtract(dst_Img, dst_Ixl)

        dst_R = cv2.normalize(log_R, None, 0, 255, cv2.NORM_MINMAX)
        log_uint8 = cv2.convertScaleAbs(dst_R)
        return log_uint8

    @staticmethod
    def enhance_MSR_image(image):
        scales = [15, 101, 301]
        b_gray, g_gray, r_gray = cv2.split(image)
        b_gray = ImageEnhanceRetinex.__enhance_MSR(b_gray, scales)
        g_gray = ImageEnhanceRetinex.__enhance_MSR(g_gray, scales)
        r_gray = ImageEnhanceRetinex.__enhance_MSR(r_gray, scales)
        result = cv2.merge([b_gray, g_gray, r_gray])
        return result


