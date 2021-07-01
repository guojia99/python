from cv2 import cv2
import numpy as np

a = cv2.imread("test5_gs/t0.png")
print(a.shape)

a = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
print(a.shape)

a = cv2.imread("test5_gs/t0.png", 0)
print(a.shape)

