'''
Description: OCR-模板匹配  参考：https://www.bilibili.com/video/BV1oJ411D71z?t=11&p=9
Author: HCQ
Company(School): UCAS
Email: 1756260160@qq.com
Date: 2021-01-23 11:12:41
LastEditTime: 2021-01-25 12:28:10
FilePath: /OpenCV/01项目实战-信用卡数字识别/template-matching-ocr/myutils.py
'''
import cv2
# 轮廓排序
def sort_contours(cnts, method="left-to-right"):
    reverse = False
    i = 0

    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True

    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1
    boundingBoxes = [cv2.boundingRect(c) for c in cnts] #用一个最小的矩形(外接矩形)，把找到的形状包起来x,y,h,w  根据x横坐标就可以排序
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes), # sorted
                                        key=lambda b: b[1][i], reverse=reverse)) # reverse

    return cnts, boundingBoxes

# resize 
def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    resized = cv2.resize(image, dim, interpolation=inter)
    return resized