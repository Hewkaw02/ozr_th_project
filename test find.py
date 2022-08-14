import cv as cv
from PIL import Image
import cv2
import numpy as np
from matplotlib import pyplot as plt
import re

x = 1280.00 / 3840.00
pixel_x = int(x * 3840)
print(x, pixel_x)

class testfind:
    def __init__(self):
        pass

def compare():
    img_rgb = cv.imread('testimages/322.jpg')
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread('testimages/312.jpg', 0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    cv.imwrite('res.jpg', img_rgb)

def Check_part():

    template = cv2.UMat(cv2.imread(image_for_check))
    use = cv2.UMat(cv2.imread(image_for_use))

    res = cv2.matchTemplate(use, template, cv2.TM_CCOEFF_NORMED)
    conf = res.max()

    print(conf)
    # for name in test:
    #     img = (cv2.imread(name, 0))
    #     print(f"Confidence for {name:}")
    #     # result =
    #     print(cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED).max())




# template = cv2.imread("template.png", 0)
# files = ["img1.png", "img2.png", "img3.png"]
#
# for name in files:
#     img = cv2.imread(name, 0)
#     print(f"Confidence for {name}:")
#     print(cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED).max())


def showimg(img):
    cv2.namedWindow("contours", 0);
    cv2.resizeWindow("contours", 1280, 720);
    cv2.imshow("contours", img)
    cv2.waitKey()

def img_resize_gray(imgorg):

    # imgorg = cv2.imread(imgname)
    crop = imgorg
    size = cv2.UMat.get(crop).shape
    # print size
    height = size[0]
    width = size[1]
    # 参数是根据3840调的
    height = int(height * 3840 * x / width)
    # print height
    crop = cv2.resize(crop, (int(3840 * x), height), cv2.INTER_CUBIC)
    return hist_equal(cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)), crop


def hist_equal(img):
    # clahe_size = 8
    # clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(clahe_size, clahe_size))
    # result = clahe.apply(img)
    # test

    # result = cv2.equalizeHist(img)

    image = img.get()  # UMat to Mat
    # result = cv2.equalizeHist(image)
    lut = np.zeros(256, dtype=image.dtype)  # 创建空的查找表
    # lut = np.zeros(256)
    hist = cv2.calcHist([image],  # 计算图像的直方图
                        [0],  # 使用的通道
                        None,  # 没有使用mask
                        [256],  # it is a 1D histogram
                        [0, 256])
    minBinNo, maxBinNo = 0, 255
    # 计算从左起第一个不为0的直方图柱的位置
    for binNo, binValue in enumerate(hist):
        if binValue != 0:
            minBinNo = binNo
            break
    # 计算从右起第一个不为0的直方图柱的位置
    for binNo, binValue in enumerate(reversed(hist)):
        if binValue != 0:
            maxBinNo = 255 - binNo
            break
    # print minBinNo, maxBinNo
    # 生成查找表
    for i, v in enumerate(lut):
        if i < minBinNo:
            lut[i] = 0
        elif i > maxBinNo:
            lut[i] = 255
        else:
            lut[i] = int(255.0 * (i - minBinNo) / (maxBinNo - minBinNo) + 0.5)
    # 计算,调用OpenCV cv2.LUT函数,参数 image --  输入图像，lut -- 查找表
    # print lut
    result = cv2.LUT(image, lut)
    # print type(result)
    # showimg(result)
    return cv2.UMat(result)


if __name__ == '__main__':

    img_data_gray, img_org = img_resize_gray(cv2.UMat(cv2.imread('testimages/112.jpg')))
    compare()