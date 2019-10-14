#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    * @par Copyright (C): 2010-2019, hunan CLB Tech
    * @file         pixel_number
    * @version      V1.0
    * @details
    * @par History
    
    @author: zhulin
"""


import cv2
import numpy as np

from scipy.misc import imresize
from matplotlib import pyplot as plt

img=cv2.imread('tankCar.jpg',0)
img=imresize(img,(240,320))
#直方图计算函数， 通道0，没有使用掩膜
hist=cv2.calcHist([img],[0],None,[256],[0,256])

hist_max=np.where(hist==np.max(hist))
print(hist_max[0])

cv2.imshow('image',img)

plt.plot(hist)
plt.xlim([0,256])
plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows()
