# -*- coding: UTF-8 -*-
# find_contour.py
"""
    * @par Copyright (C): 2010-2019, Hunan CLB Tech
    * @file         RMB_recognition_nospeech.py
    * @version      V1.0
    * @details
    * @par History
    @author: zhulin 
"""
import cv2
import numpy as np

# 生成颜色直方图
def color_hist(img):
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    hist_mask = cv2.calcHist([hsv], [0], None, [180], [0, 180])
    
    #统计直方图识别颜色
    object_H = np.where(hist_mask==np.max(hist_mask)) # 获取直方图最大的值及其索引
    print (object_H[0])
    
    return object_H[0]

# 判断直方图H的值，实现颜色识别
# 实现RMB识别
# try except 捕获object_H存在多个值的异常
def color_distinguish(object_H):

    try:
        if object_H > 3 and object_H < 25: RMB = '20'
        elif object_H > 156 and object_H < 170: RMB = '100'
        elif object_H > 125 and object_H < 155: RMB = '5'
        elif object_H > 100 and object_H < 124: RMB = '10'
        elif object_H > 25 and object_H < 50: RMB = '1'
        elif object_H > 171 and object_H < 180: RMB = '50'
        else: RMB = 'None'
        print ('RMB:',RMB,object_H)
        return RMB
    except: pass


if __name__ == '__main__':
    img = cv2.imread('pic/20.png', 1)
    object_H = color_hist(img)
    rmb=color_distinguish(object_H)
    cv2.imshow('image', img)
    cv2.waitKey(0)

    
