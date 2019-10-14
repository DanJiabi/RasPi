#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    * @par Copyright (C): 2010-2019, hunan CLB Tech
    * @file         hist_diagram
    * @version      V1.0
    * @details
    * @par History
    
    @author: zhulin
"""

import cv2
import numpy as np

from scipy.misc import imresize
from matplotlib import pyplot as plt

img=cv2.imread('tankCar.jpg',cv2.IMREAD_COLOR)


img=imresize(img,(240,320))
hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

#生成2d直方图
hist=cv2.calcHist([hsv],[0,1],None,[180,256],[0,180,0,256])

hist_max=np.where(hist==np.max(hist))
print(hist_max[0])

cv2.imshow('image',img)
#绘图
plt.imshow(hist,interpolation='nearest')
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
