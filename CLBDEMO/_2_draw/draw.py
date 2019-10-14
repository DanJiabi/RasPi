#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
* @par Copyright (C): 2010-2019, hunan CLB Tech
* @file         draw
* @version      V1.0
* @details
* @par History
* @author       zhulin
"""

import cv2
import numpy as np
img=np.zeros((512,512,3),dtype=np.uint8)
#图形的位置，周长，半径等等参数都是由参数控制的，希望小伙伴们尝试自行修改，便于理解
#画线
cv2.line(img,(0,0),(500,500),(255,0,0),5)
#画圆，填充圆，最后一个参数为-1
cv2.circle(img,(255,255),50,(0,255,0),-1)
#圆，轮廓
cv2.circle(img,(255,255),80,(255,255,0),5)
#矩形
cv2.rectangle(img,(170,170),(340,340),(0,0,255),2)

#文字
cv2.putText(img,'Learn OpenCV CLB',(20,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,255),2)
cv2.putText(img,'CLB technology',(80,450),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),2)

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
