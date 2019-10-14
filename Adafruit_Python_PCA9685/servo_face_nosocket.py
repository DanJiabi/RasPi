#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    * @par Copyright (C): 2010-2019, Hunan CLB Tech
    * @file        sevo_face_nosocket
    * @version      V1.0
    * @details
    * @par History
    @author: zhulin
"""
#和对颜色的操作大体相同
from __future__ import division
import cv2
import Adafruit_PCA9685
import time  
import numpy as np
import threading
#初始化PCA9685和舵机
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)
pwm.set_pwm(1,0,500)
pwm.set_pwm(2,0,500)
time.sleep(1)
#初始化摄像头并设置阙值
#如果觉得卡顿严重，请调整“1”处和“2”处 两处代码
cap = cv2.VideoCapture(0)
#“1”处，摄像头的分辨率，中心点为（160，240）

#cap.set(cv2.cv.CV_CAP_PROP_FOURCC,cv2.cv.CV_FOURCC('M','J','P','G'))
cap.set(3, 320)
cap.set(4, 240)
#引入分类器
face_cascade = cv2.CascadeClassifier( '123.xml' )
x=0
thisError_x=0
lastError_x=0
thisError_y=0
lastError_y=0

Y_P = 425
X_P = 425
flag=0
y=0
w=0
h=0
facebool = False

def xx():
    while True:
        CON=0
        if CON==0:
            pwm.set_pwm(1,0,650-X_P+200)
            #pwm.set_pwm(2,0,650-Y_P+200)
            CON+=1
        else:
            pwm.set_pwm(1,0,650-X_P)
            #pwm.set_pwm(2,0,650-Y_P)
    

tid=threading.Thread(target=xx)
tid.setDaemon(True)
tid.start()
    
while True:
    
    ret,frame = cap.read()
    
    #frame=cv2.GaussianBlur(frame,(5,5),0)
    gray= cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    #对灰度图进行.detectMultiScale()
    faces=face_cascade.detectMultiScale(gray)
    max_face=0
    value_x=0
    
    
    if len(faces)>0:
        #print('face found!')
        #temp = (x,y,w,h)
        (x,y,w,h) = faces[0]
        cv2.rectangle(frame,(x,y),(x+h,y+w),(0,255,0),2)
        result=(x,y,w,h)
        x=result[0]+w/2
        y=result[1]+h/2
        facebool = True
        '''
        
        for(x,y,w,h) in faces:
            #找到矩形的中心位置
            cv2.rectangle(frame,(x,y),(x+h,y+w),(0,255,0),2)
            result=(x,y,w,h)
            x=result[0]+w/2
            y=result[1]+h/2
            '''
    
        #“2”处 误差值
        
        
    #while facebool:    
        thisError_x=x-160
        thisError_y=y-120
        #if thisError_x > -20 and thisError_x < 20 and thisError_y > -20 and thisError_y < 20:
        #    facebool = False
        #自行对P和D两个值进行调整，检测两个值的变化对舵机稳定性的影响
        pwm_x = thisError_x*5+1*(thisError_x-lastError_x)
        pwm_y = thisError_y*5+1*(thisError_y-lastError_y)
        lastError_x = thisError_x
        lastError_y = thisError_y
        XP=pwm_x/100
        YP=pwm_y/100
        X_P=X_P+int(XP)
        Y_P=Y_P+int(YP)
        if X_P>670:
            X_P=650
        if X_P<0:
            X_P=0
        if Y_P>650:
            Y_P=650
        if X_P<0:
            Y_p=0
        
    
    
    #pwm.set_pwm(1,0,650-X_P)
    #pwm.set_pwm(2,0,650-Y_P)

    cv2.imshow("capture", frame)
    if cv2.waitKey(1)==119:
        break
    
cap.release()
cv2.destroyAllWindows()
