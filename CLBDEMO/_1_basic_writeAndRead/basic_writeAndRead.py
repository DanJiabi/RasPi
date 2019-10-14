#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
* @par Copyright (C): 2010-2019, hunan CLB Tech
* @file         basic_writeAndrRead
* @version      V1.0
* @details
* @par History

@author: zhulin
"""

import cv2
img=cv2.imread('tankCar.jpg',cv2.IMREAD_COLOR)

cv2.imshow('image',img)

k=cv2.waitKey(0)

#当键盘输入“s”时保存图片到指定文件内
#当键盘输入“esc”时推出
if k==27:
    cv2.destroyAllWindows()
elif k==ord('s'):
    cv2.imwrite('car.jpg',img)
    print('save image successfully')
    cv2.destroyAllWindows()
