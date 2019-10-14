#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
* @par Copyright (C): 2010-2019, hunan CLB Tech
* @file         colorBlock.py
* @version      V1.0
* @details
* @par History
* @author       zhulin
"""

import cv2
import numpy as np

#创建图片和颜色块
img=np.ones((240,320,3),dtype=np.uint8)*255
img[100:140,140:180]=[0,0,255]
img[60:100,60:100]=[0,255,255]
img[60:100,220:260]=[255,0,0]
img[140:180,60:100]=[255,0,0]
img[140:180,220:260]=[0,255,255]

#黄红两色的hsv阙值
yellow_lower=np.array([26,43,46])
yellow_upper=np.array([34,255,255])
red_lower=np.array([0,43,46])
red_upper=np.array([10,255,255])

#颜色空间转换 bgr->hsv
hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

#构建掩膜，并用掩膜进行
mask_yellow=cv2.inRange(hsv,yellow_lower,yellow_upper)
mask_red=cv2.inRange(hsv,red_lower,red_upper)
mask=cv2.bitwise_or(mask_yellow,mask_red)
res=cv2.bitwise_and(img,img,mask=mask)

cv2.imshow('image',img)
cv2.imshow('mask',mask)
cv2.imshow('res',res)
cv2.waitKey(0)
cv2.destroyAllWindows()
