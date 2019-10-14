#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    * @par Copyright (C): 2010-2019, Hunan CLB Tech
    * @file         face_orgin_detected
    * @version      V1.0
    * @details
    * @par History
    
    @author: zhulin
"""
import cv2
import numpy as np
#两个xml比较器
face_cascade=cv2.CascadeClassifier('face.xml')
eye_cascade=cv2.CascadeClassifier('eye.xml')

#将被查询的目标文件的地址
filename='dai.jpg'
img=cv2.imread(filename)
#先找人脸，找到人脸后绘制人脸矩形
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
faces=face_cascade.detectMultiScale(gray,1.3,5)
for (x,y,w,h) in faces:
    print("found")
    #再找人眼。同样的方法
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    eyes=eye_cascade.detectMultiScale(img)
    for (ex,ey,ew,eh) in eyes:
        print("found")
        cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
cv2.imwrite('new.png',img)

    

