# encoding:utf-8
import cv2

img = cv2.imread("./cat.jpg")
cv2.namedWindow("Image显示")
cv2.imshow("Image显示", img)
cv2.waitKey(0)
cv2.destroyAllWindows()


# https: // www.cnblogs.com/zangyu/p/5802142.html
