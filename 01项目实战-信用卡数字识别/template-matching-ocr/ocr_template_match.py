'''
Description: OCR-模板匹配  参考：https://www.bilibili.com/video/BV1oJ411D71z?t=11&p=9
运行命令：  python ocr_template_match.py   -i   xxx    -t    xxx
运行命令：  python 01项目实战-信用卡数字识别/template-matching-ocr/ocr_template_match.py   -i   01项目实战-信用卡数字识别/template-matching-ocr/images/credit_card_01.png    -t    01项目实战-信用卡数字识别/template-matching-ocr/images/ocr_a_reference.png
Author: HCQ
Company(School): UCAS
Email: 1756260160@qq.com
Date: 2021-01-23 11:12:41
LastEditTime: 2021-01-25 14:07:18
FilePath: /OpenCV/01项目实战-信用卡数字识别/template-matching-ocr/ocr_template_match.py
'''
# 导入工具包
from imutils import contours
import numpy as np
import argparse
import cv2
import myutils

# 设置参数
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument("-t", "--template", required=True,
	help="path to template OCR-A image")
args = vars(ap.parse_args())

# 指定信用卡类型
FIRST_NUMBER = {
	"3": "American Express",
	"4": "Visa",
	"5": "MasterCard",
	"6": "Discover Card"
}
# 绘图展示
def cv_show(name,img):
	cv2.imshow(name, img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

# ==========================开始 1 处理模板图片========================================
# 读取一个模板图像
img = cv2.imread(args["template"]) # 参数  01项目实战-信用卡数字识别/template-matching-ocr/images/ocr_a_reference.png
cv_show('img',img)
# 灰度图
ref = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv_show('ref',ref)
# 二值图像
ref = cv2.threshold(ref, 10, 255, cv2.THRESH_BINARY_INV)[1]
cv_show('ref',ref)

# 计算轮廓
#cv2.findContours()函数接受的参数为二值图，即黑白的（不是灰度图）,cv2.RETR_EXTERNAL只检测外轮廓，cv2.CHAIN_APPROX_SIMPLE只保留终点坐标
#返回的list中每个元素都是图像中的一个轮廓

# 高版本没有第一个参数ref_了，只会返回后两个
# ref_, refCnts, hierarchy = cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) # 低版本
refCnts, hierarchy = cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) # 高版本

cv2.drawContours(img,refCnts,-1,(0,0,255),3) 
cv_show('img',img)
print (np.array(refCnts).shape) # 多少轮廓
refCnts = myutils.sort_contours(refCnts, method="left-to-right")[0] #排序，从左到右，从上到下
digits = {}

# 遍历每一个轮廓
for (i, c) in enumerate(refCnts):
	# 计算外接矩形并且resize成合适大小
	(x, y, w, h) = cv2.boundingRect(c)
	roi = ref[y:y + h, x:x + w] # x旋转区域
	roi = cv2.resize(roi, (57, 88)) # resize

	# 每一个数字对应每一个模板
	digits[i] = roi

# =======================2 处理信用卡图片================================
# 初始化卷积核
rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 3))
sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)) # 核大小  5x5

#读取输入图像，预处理
image = cv2.imread(args["image"]) # 参数
cv_show('image',image)
image = myutils.resize(image, width=300)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv_show('gray',gray)

#礼帽操作，突出更明亮的区域（字体区域）
tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, rectKernel)  # rectKernel初始化核
cv_show('tophat',tophat) 
# 
gradX = cv2.Sobel(tophat, ddepth=cv2.CV_32F, dx=1, dy=0, #ksize=-1相当于用3*3的
	ksize=-1)


gradX = np.absolute(gradX) # 只用x效果更好，随意没用xy梯度
(minVal, maxVal) = (np.min(gradX), np.max(gradX))
gradX = (255 * ((gradX - minVal) / (maxVal - minVal))) # 归一化
gradX = gradX.astype("uint8")

print (np.array(gradX).shape)
cv_show('gradX',gradX)

#通过闭操作（先膨胀，再腐蚀）将数字连在一起，形成四大块 背景也过滤了
gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel) 
cv_show('gradX',gradX)
#THRESH_OTSU会自动寻找合适的阈值，适合双峰，需把阈值参数设置为0
thresh = cv2.threshold(gradX, 0, 255,
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1] 
cv_show('thresh',thresh)

#再来一个闭操作

thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel) #再来一个闭操作
cv_show('thresh',thresh)

# 计算轮廓

# 高版本没有第一个参数thresh_了，只会返回后两个
# thresh_, threshCnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
# 	cv2.CHAIN_APPROX_SIMPLE)
threshCnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)

cnts = threshCnts # 最终轮廓
cur_img = image.copy()
cv2.drawContours(cur_img,cnts,-1,(0,0,255),3) 
cv_show('img',cur_img)
locs = [] # 有价值的区域

# 遍历轮廓
for (i, c) in enumerate(cnts):
	# 计算矩形
	(x, y, w, h) = cv2.boundingRect(c)
	ar = w / float(h) # 长宽比

	# 选择合适的区域，根据实际任务来，这里的基本都是四个数字一组
	if ar > 2.5 and ar < 4.0:

		if (w > 40 and w < 55) and (h > 10 and h < 20):
			#符合的留下来
			locs.append((x, y, w, h))

# 将符合的轮廓从左到右排序
locs = sorted(locs, key=lambda x:x[0])
output = []

# 遍历每一个轮廓中的数字（四个大轮廓，每个轮廓里面有4个数字）
for (i, (gX, gY, gW, gH)) in enumerate(locs):
	# initialize the list of group digits
	groupOutput = []

	# 根据坐标提取每一个组
	group = gray[gY - 5:gY + gH + 5, gX - 5:gX + gW + 5] # 往外扩大一点范围
	cv_show('group',group)
	# 预处理（二值化）
	group = cv2.threshold(group, 0, 255,
		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	cv_show('group',group)
	# 计算每一组的轮廓（4个数字，四个轮廓）
	# 高版本没有第一个参数group_了，只会返回后两个
	# group_,digitCnts,hierarchy = cv2.findContours(group.copy(), cv2.RETR_EXTERNAL,
	# 	cv2.CHAIN_APPROX_SIMPLE)
	digitCnts,hierarchy = cv2.findContours(group.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	digitCnts = contours.sort_contours(digitCnts,
		method="left-to-right")[0]

	# 计算每一组中的每一个数值
	for c in digitCnts:
		# 找到当前数值的轮廓，resize成合适的的大小
		(x, y, w, h) = cv2.boundingRect(c)
		roi = group[y:y + h, x:x + w]
		roi = cv2.resize(roi, (57, 88))
		cv_show('roi',roi)

		# 计算匹配得分
		scores = []

		# 在模板中计算每一个得分=============================================================================
		for (digit, digitROI) in digits.items():
			# 模板匹配（和模板中的10个数字匹配）
			result = cv2.matchTemplate(roi, digitROI,
				cv2.TM_CCOEFF)
			(_, score, _, _) = cv2.minMaxLoc(result)
			scores.append(score)

		# 得到最合适的数字
		groupOutput.append(str(np.argmax(scores))) # score最大的下标

	# 画出来
	cv2.rectangle(image, (gX - 5, gY - 5),
		(gX + gW + 5, gY + gH + 5), (0, 0, 255), 1)
	cv2.putText(image, "".join(groupOutput), (gX, gY - 15),
		cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)

	# 得到结果
	output.extend(groupOutput)

# 打印结果
print("Credit Card Type: {}".format(FIRST_NUMBER[output[0]]))
print("Credit Card #: {}".format("".join(output)))
cv2.imshow("Image", image)
cv2.waitKey(0)