from cv2 import cv2 as cv
from square_recognition import SquaresImage

Path = "./image/"
# Images = ["矩形卡3.png", "矩形卡2.png", "矩形卡22.png"]
Images = ["矩形卡22.png"]

def t_squares1():
    for item in Images:
        img = cv.imread(f"{Path}/{item}")
        squares, img = SquaresImage().squares_1(img)
        cv.drawContours(img, squares, -1, (0, 0, 255), 2)
        cv.imwrite(f"./image/t_squares1_{item}_test.png", img)
        print(f'Done {item}')


if __name__ == '__main__':
    t_squares1()
