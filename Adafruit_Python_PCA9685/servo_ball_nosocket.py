#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    * @par Copyright (C): 2010-2019, Hunan CLB Tech
    * @file        sevo_ball_nosocket
    * @version      V1.0
    * @details
    * @par History
    @author: zhulin
"""
from __future__ import division
import cv2
import Adafruit_PCA9685

import time  
import numpy as np
import threading

#初始化PCA9685和舵机
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)
pwm.set_pwm(1,0,320)
pwm.set_pwm(2,0,240)
time.sleep(1)
#初始化摄像头并设置阙值
#如果觉得卡顿严重，请调整“1”处和“2”处 两处代码
cap = cv2.VideoCapture(0)
#“1”处，摄像头的分辨率，中心点为（320，240）
cap.set(3, 320)
cap.set(4, 240)
yellow_lower=np.array([9,135,231])
yellow_upper=np.array([31,255,255])
#每个自由度需要4个变量
x=0;
thisError_x=500       #当前误差值
lastError_x=100       #上一次误差值
thisError_y=500
lastError_y=100
Y_P=425
X_P = 425           #转动角度
flag=0
y=0
def xx(X_P,Y_P):
    pwm.set_pwm(1,0,650-X_P)
    pwm.set_pwm(2,0,650-Y_P)
while True:    
    ret,frame = cap.read()
    #高斯模糊
    frame=cv2.GaussianBlur(frame,(5,5),0)
    hsv= cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    #掩膜和形态学操作找到小球轮廓
    mask=cv2.inRange(hsv,yellow_lower,yellow_upper)
    mask=cv2.erode(mask,None,iterations=2)
    mask=cv2.dilate(mask,None,iterations=2)
    mask=cv2.GaussianBlur(mask,(3,3),0)
    res=cv2.bitwise_and(frame,frame,mask=mask)
    cnts=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    #当找到小球后
    if len(cnts)>0:
        #print('face found!')
        cnt=max(cnts,key=cv2.contourArea)
        (x,y),radius=cv2.minEnclosingCircle(cnt)
        cv2.circle(frame,(int(x),int(y)),int(radius),(255,0,255),2)
        #“2”处 误差值
        thisError_x=x-160
        thisError_y=y-120
        #PID控制
        pwm_x = thisError_x*3+1*(thisError_x-lastError_x)
        pwm_y = thisError_y*3+1*(thisError_y-lastError_y)
        #迭代两个误差值
        lastError_x = thisError_x
        lastError_y = thisError_y
        #Adafruit_PCA9685智能输入整数
        XP=pwm_x/100
        YP=pwm_y/100
        X_P=X_P+int(XP)
        Y_P=Y_P+int(YP)
        #将舵机转动脉冲保持在安全范围内
        if X_P>670:
            X_P=650
        if X_P<0:
            X_P=0
        if Y_P>650:
            Y_P=650
        if X_P<0:
            Y_p=0
        print('x',x,X_P);
    tid=threading.Thread(target=xx,args=(X_P,Y_P,))
    tid.setDaemon(True)
    tid.start()
    #舵机转动，不能直接通过pwm.set_pwm(1,0,X_P/Y_P)控制
    #pwm.set_pwm(1,0,650-X_P)
    #pwm.set_pwm(2,0,650-Y_P)

    cv2.imshow("capture", frame)
    if cv2.waitKey(1)==119:
        break
    
cap.release()
cv2.destroyAllWindows()
