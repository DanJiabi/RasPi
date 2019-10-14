#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    * @par Copyright (C): 2010-2019, hunan CLB Tech
    * @file        socket server
    * @version      V1.0
    * @details
    * @par History
    
    @author: zhulin
"""
import cv2
import numpy as np

def nothing(x):
    
    pass
img=np.zeros((320,512,3),dtype=np.uint8)
cv2.namedWindow('image')
#创建三个trackcar，
#参数：“名字”，“目标窗口”，“初始化阙值”，“刻度”，“回调”
cv2.createTrackbar('R','image',0,255,nothing)
cv2.createTrackbar('G','image',0,255,nothing)
cv2.createTrackbar('B','image',0,255,nothing)

while True:
    cv2.imshow('image',img)
    r=cv2.getTrackbarPos('R','image')
    g=cv2.getTrackbarPos('G','image')
    b=cv2.getTrackbarPos('B','image')
    
    #随着拖动trackbar，修改窗口的颜色
    img[:]=[b,g,r]
    if cv2.waitKey(1)&0xFF==27:
        break
cv2.destroyAllWindows()
