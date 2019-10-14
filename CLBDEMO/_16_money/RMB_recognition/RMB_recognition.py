# -*- coding: UTF-8 -*-
# find_contour.py
"""
    * @par Copyright (C): 2010-2019, Hunan CLB Tech
    * @file         RMB_recognition.py
    * @version      V1.0
    * @details
    * @par History
    @author: zhulin 
"""
import cv2
import numpy as np
from aip import AipSpeech
import pygame

#APP_ID='xxxx'
#API_KEY='xxxx'
#SECRET_KEY='xxxx'

#初始化baidu speech（填入自己的信息，没有填入信息之前不能用） 
APP_ID='XXXX'
API_KEY='XXXX'
SECRET_KEY='XXXX'

aipSpeech=AipSpeech(APP_ID,API_KEY,SECRET_KEY)

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
    _,contours,hierarchy = cv2.findContours(
            mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
    # 寻找ROI的位置
    if len(contours)>0:
        cnt = max(contours, key=cv2.contourArea)
        x,y,w,h = cv2.boundingRect(cnt)
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
		
        img_ROI = img[y:y+h, x:x+w]
    else:
        img_ROI = img

    return img_ROI

# 生成颜色直方图
def color_hist(img):
    #构建掩膜
    #mask = np.zeros(img.shape[:2], np.uint8)
    #mask[70:170,250:370] = 255
    #生成HSV颜色空间 H 的直方图
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
    img = cv2.imread('pic/50.png', 1)
   # img_ROI = find_ROI(img)
    
    object_H = color_hist(img)
    
    rmb=color_distinguish(object_H)
    text=rmb+'元人民币,'+'hsv特征值为'+str(object_H[0])
    result = aipSpeech.synthesis(text = text, 
                             options={'spd':2,'vol':9,'per':1,})
    #将合成的语音写如文件
    if not isinstance(result,dict):
        with open('audio.mp3','wb') as f:
            f.write(result)
        
    else:print(result)
    #我们利用树莓派自带的pygame
    pygame.mixer.init()
    pygame.mixer.music.load('audio.mp3')
    pygame.mixer.music.play()

    cv2.imshow('image', img)

    cv2.waitKey(0)

    
