import numpy as np
from cv2 import cv2 as cv

def GetMAD(data: list) -> (list, float, float):
    median = np.median(data)
    b = 1.4826

    mad = b * np.median(np.abs(data - median))

    lower = median - (3 * mad)
    upper = median + (3 * mad)

    out = []

    for i in range(len(data)):
        for rho, theta in data[i]:
            if lower <= theta <= upper:
                out.append(theta)
    return np.mean(out), lower, upper


def getMad(data: list) -> (list, float, float):
    return GetMAD(data)


def Get_angle_cos(p0, p1, p2: float) -> float:
    """
    三点两线，求夹角
    :return: 返回余弦值
    """
    d1 = (p0 - p1).astype('float')
    d2 = (p2 - p1).astype('float')
    return abs(np.dot(d1, d2) / np.sqrt(np.dot(d1, d1) * np.dot(d2, d2)))

def CalcDegree(Image: np.ndarray) -> float:
    """
    校正图像角度
    """
    mid_image = cv.cvtColor(Image, cv.COLOR_BGR2HSV)
    canny_image = cv.Canny(image=mid_image, threshold1=50, threshold2=200, edges=3, apertureSize=None, L2gradient=None)
    line_image = Image.copy()

    lines = cv.HoughLines(image=canny_image, rho=1, theta=np.pi / 180, threshold=200)

    theta_list = []
    for item in range(len(lines)):
        for rho, theta in lines[item]:
            theta_list.append(theta)
    theta_avg, lower, upper = getMad(theta_list)

    deviation = 0.01
    if (np.pi / 2 - deviation <= theta_avg <= np.pi / 2 + deviation) or (0 <= theta_avg <= deviation) or (
            np.pi - deviation <= theta_avg <= 180):
        return 0

    sums = 0
    for item in range(len(lines)):
        for rho, theta in lines[item]:
            if lower <= theta <= upper:
                a, b = np.cos(theta), np.sin(theta)
                x0, y0 = a * rho, b * rho

                x1, y1 = int(round(x0 + 1000 * (-b))), int(round(y0 + 1000 * a))
                x2, y2 = int(round(x0 - 1000 * (-b))), int(round(y0 - 1000 * a))
                sums += theta
                cv.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 1, cv.LINE_AA)

    res = (sums / len(lines)) / np.pi * 180
    angle = 90 + res
    if res < 45:
        angle = -90 + res
    return angle


