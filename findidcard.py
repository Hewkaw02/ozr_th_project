import numpy as np
import cv2
import time
import idcardocr
from matplotlib import pyplot as plt

class findidcard:
    def __init__(self):
        pass

    def find(self , image2_name):

        image_name = 'idcard_mask.jpg'
        MIN_MATCH_COUNT =  10
        img1 = cv2.UMat(cv2.imread(image_name, 0)) # Query Image in Gray
        img1 = self.img_resize(img1, 640)
        # self.showimg(img1)

        img2 = cv2.UMat(cv2.imread(image2_name, 0)) # Train Image in Gray
        # print(img2.get().shape)
        img2 = self.img_resize(img2, 1920)
        # self.showimg(img2)

        img_orc = cv2.UMat(cv2.imread(image2_name))
        img_orc = self.img_resize(img_orc, 1920)

        t1 = round(time.time() * 1000)

        sift = cv2.xfeatures2d.SIFT_create()
        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(img1, None)
        kp2, des2 = sift.detectAndCompute(img2, None)

        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=10)

        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)

        # store all the good matches as per Lowe's ratio test.
        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)
        # reshape(x,y)
        if len(good) > MIN_MATCH_COUNT:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            matchesMask = mask.ravel().tolist()

            h, w = cv2.UMat.get(img1).shape
            M_r = np.linalg.inv(M)
            im_r = cv2.warpPerspective(img_orc, M_r, (w, h))
            # self.showimg(im_r)
        else:
            print("Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT))
            matchesMask = None

        # draw_params = dict(matchColor = (0,255,0), # draw matches in green color
        #           singlePointColor = None,
        #           matchesMask = matchesMask, # draw only inliers
        #           flags = 2)
        # img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
        # plt.imshow(img3, 'gray'),plt.show()
        t2 = round(time.time() * 1000)
        print(u'ความหน่วงเวลาในการค้นหาภาพ :%s' % (t2 - t1))
        return im_r

    def showimg(self, img):
        cv2.namedWindow("contours", 0)
        # cv2.resizeWindow("contours", 1600, 1200);
        cv2.imshow("contours", img)
        cv2.waitKey()

    def img_resize(self, imggray, dwidth):
        # print 'dwidth:%s' % dwidth
        crop = imggray
        size = cv2.UMat.get(imggray).shape
        height = size[0]
        width = size[1]
        height = height * dwidth / width
        crop = cv2.resize(crop, (dwidth, int(height)), cv2.INTER_CUBIC)
        return crop


# Press the green button in the gutter to run the script.


def Check_part():

    template = cv2.imread('112.jpg')
    use = cv2.imread('332.jpg')
    print(f"Confidence for :")
    conf = cv2.matchTemplate(use, template, cv2.TM_CCOEFF_NORMED).max()
    print(conf)


if __name__ == '__main__':
    idfind = findidcard()
    result = idfind.find('testimages/3.jpg')

    cv2.imwrite('312.jpg', result)
    Check_part()
    # idfind.showimg(result)
