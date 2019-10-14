#-*- encoding:utf-8 -*-
# @author: zhulin
# 绘制HSV颜色空间2D直方图

import cv2
import numpy as np
from scipy.misc import imresize
from matplotlib import pyplot as plt

# 基于轮廓定位QR位置
def find_ROI(img):
    
    # 高斯滤波
    blur = cv2.GaussianBlur(img,(5,5),0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 二值化
    ret,th = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # 形态学操作
    mask=cv2.erode(th,None,iterations=4)
    mask=cv2.dilate(mask,None,iterations=4)
    # 图像反色
    cv2.bitwise_not(mask, mask)

    # 寻找轮廓
    _,contours,hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
    # 寻找ROI的位置
    if len(contours)>0:
        cnt = max(contours, key=cv2.contourArea)
        x,y,w,h = cv2.boundingRect(cnt)
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
		
        img_ROI = img[y:y+h, x:x+w]
        '''
         寻找旋转的边界矩形
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = list(box)
        print box
        cv2.line(img,(box[0][0],box[0][1]),(box[1][0],box[1][1]),(0,0,255),3)
        cv2.line(img,(box[0][0],box[0][1]),(box[3][0],box[3][1]),(0,0,255),3)
        cv2.line(img,(box[1][0],box[1][1]),(box[2][0],box[2][1]),(0,0,255),3)
        cv2.line(img,(box[2][0],box[0][1]),(box[3][0],box[3][1]),(0,0,255),3)
        '''
       
    else:
        img_ROI = img

    return img_ROI


img = cv2.imread('pic/50.png',cv2.IMREAD_COLOR)
#img = find_ROI(img)
#img = imresize(img, (240,320))
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 生成2D直方图
hist = cv2.calcHist([hsv],[0, 1],None,[180, 256],[0, 180, 0, 256])

cv2.imshow('image', img)

# pyplot 绘图
plt.imshow(hist, interpolation = 'nearest') 
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
