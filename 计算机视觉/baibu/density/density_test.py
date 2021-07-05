from density import DensityTool
from cv2 import cv2
import pandas as pd
import os
import time
import numpy as np
import math


def enhance_hist(image: np.ndarray) -> np.ndarray:
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


def print_list(l: list, name: str):
    m = []
    for item in l:
        if item == np.nan:
            continue
        if item == math.nan:
            continue
        if item <= 0:
            continue
        if np.isnan(item):
            continue
        m.append(item)
    l = m
    print("*-" * 30)
    print(f"{name}->", l)
    print(f"{name}_avg ->", np.mean(l))
    print(f"{name}_sorted->{sorted(l)}")
    print(f"{name}_len ->", len(l))
    print(f"{name}_std->", np.std(l))


def function(path: str):
    paths = os.listdir(path)
    paths = [os.path.join(path, item) for item in paths if item[-4:] == ".jpg"]
    re_data = []
    meridians, broadwise = [], []
    for item in paths:
        ts = time.time()
        img = cv2.imread(item)
        img = enhance_hist(image=img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        d = DensityTool(image=img)
        try:
            data = d.get()
            m = data.get("meridians")
            b = data.get("broadwise")
            meridians.append(m)
            broadwise.append(b)
            print(f"[{time.time() - ts}][{item}]{data}")
            data.update({"cost_time": time.time() - ts, "path": item})
            re_data.append(data)
        except ValueError as e:
            print(f"\033[31m{e}\033[0m")

    print_list(meridians, "meridians")
    print_list(broadwise, "broadwise")

    csv_writer(re_data, f"{path}/water_data_{time.time()}.csv")


def check_data(data: list) -> dict:
    out: dict = {
        "meridians": [],
        "meridians_std": [],
        "broadwise": [],
        "broadwose_std": [],
        "path": [],
        "cost_time": [],
    }
    for d in data:
        out["meridians"].append(d.get("meridians"))
        out["meridians_std"].append(d.get("meridians_std"))
        out["broadwise"].append(d.get("broadwise"))
        out["broadwose_std"].append(d.get("broadwose_std"))
        out["path"].append(d.get("path"))
        out["cost_time"].append(d.get("cost_time"))
    return out


def csv_writer(list_dict, path_name: str):
    data: dict = check_data(list_dict)
    my_data = pd.DataFrame(data)
    my_data.to_csv(path_name)


if __name__ == "__main__":
    function("/Users/caime/Desktop/3110")
