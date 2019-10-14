#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    * @par Copyright (C): 2010-2019, Hunan CLB Tech
    * @file        socket server
    * @version      V1.0
    * @details
    * @par History
    
    @author: zhulin
"""

from __future__ import division
import cv2
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os.path
import itchat
#自动登录，微信会自动生成二维码，可以在屏幕上弹出二维码
#设置hotreload为真，可以热启动，也就是说之后几次
itchat.auto_login(hotReload=True)
#摄像头操作
cap=cv2.VideoCapture(0)
cap.set(3,320)
cap.set(4,320)
face_cascade=cv2.CascadeClassifier('123.xml')
sendDate=0

while True:
    #人脸识别的模块
    ret,frame=cap.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(gray)
    max_face=0
    value_x=0
    font=cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),(20,20),font,0.8,(255,255,255),1)
    #找到人脸后进行一系列操作
    if len(faces)>0:
        #设置时间戳
        currentDate=time.time()
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+h,y+w),(0,255,0),2)
            result=(x,y,w,h)
            x=result[0]
            y=result[1]
        if currentDate-sendDate>600:
            #如果在10分钟内没有发送过图片，
            #将当前帧写入独立png中
            cv2.imwrite("out.png",frame)
            #先通过search_friend爬去friend1的数据
            #因为现在itchat不支持直接通过friend1发送消息，（这个地方写你要发送给谁的名字）
            account=itchat.search_friends(name='吴珍')
            print(account[0]['UserName'])
            #发送
            itchat.send("@img@%s"%'out.png',account[0]['UserName'])
            #记录时间
            sendDate=time.time()
    cv2.imshow("capture",frame)
    if cv2.waitKey(1)==119:
        break
cap.release()
cv2.destroyAllWindows()            
            
            
