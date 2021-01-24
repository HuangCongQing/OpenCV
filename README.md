# OpenCV

1. 人机互动 2、物体识别 3、图像分割 4、人脸识别 5、动作识别 6、运动跟踪 7、机器人 8、运动分析 9、机器视觉 10、结构分析 11、汽车安全驾驶

官网： [opencv](https://github.com/opencv)/**[opencv](https://github.com/opencv/opencv)**

环境dev：win7/Ubuntu18.04，python35/36 + opencv3.4/4.1 + VScode

**OpenCV在Python中导入名称是cv2**

## Installation

两种方法呢

* 直接pip命令安装-直接命令法
  `pip3 install opencv-python`
  `pip3 install opencv-contrib-python`
  `pip3 install pytesseract`
* 下载whl文件法
  1. 先去官网 https://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv，下载相应Python版本的OpenCV的whl文件，如本人下载的opencv_python‑3.4.1‑cp36‑cp36m‑win_amd64.whl，
  2. 然后在whl文件所在目录下，命令`pip install opencv_python‑3.4.1‑cp36‑cp36m‑win_amd64.whl` 进行安装即可

## 基于python的Opencv项目实战

* 视频：https://www.bilibili.com/video/BV1oJ411D71z
* 代码&笔记：[基于python的Opencv项目实战](基于python的Opencv项目实战)

  * [图像操作(图像读取  色彩空间转换 展示图像信息 读取视频  边界填充 数值计算 图像融合 )](基于python的Opencv项目实战/图像操作/图像基本操作.ipynb)
  * 图像处理
    * [图像阈值 图像平滑 形态学 图像梯度 边缘检测 图像金字塔 轮廓检测 傅里叶变换](基于python的Opencv项目实战/图像操作/图像处理.ipynb)
    * [直方图&模板匹配](基于python的Opencv项目实战/图像处理/图像处理-2(直方图&模板匹配).ipynb)
  * [01项目实战-信用卡数字识别/template-matching-ocr](01项目实战-信用卡数字识别/template-matching-ocr)
  * [02项目实战-文档扫描OCR识别](02项目实战-文档扫描OCR识别)

## License

Copyright (c) [双愚](https://github.com/HuangCongQing/OpenCV). All rights reserved.

Licensed under the [MIT](https://github.com/HuangCongQing/OpenCV/blob/master/LICENSE) License.
