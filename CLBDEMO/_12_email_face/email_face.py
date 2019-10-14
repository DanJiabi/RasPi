#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    * @par Copyright (C): 2010-2019, Hunan CLB Tech
    * @file         email_face
    * @version      V1.0
    * @details
    * @par History
    
    @author: zhulin
"""

from __future__ import division
import cv2

import time  
import signal  
import sys
reload(sys)
sys.setdefaultencoding('utf8')
#-----------------------------------以上为控制编码方式-----------------------------------
import smtplib                                  #引入SMTP协议包
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart  #创建包含多个部分的邮件体
from email.mime.base import MIMEBase            #添加附件（附件内容并附加到根容器 ）
from email.mime.image import MIMEImage
import os.path                                  #分析路径
from email import Encoders

sendDate=0
sender = "XXXX@qq.com"                     #发送邮箱，qq邮箱
password = "XXXX"
receiver = "XXXX@qq.com"                  #目标邮箱
#--------------------邮件服务与端口信息----------------------------------------------------
smtp_server = "smtp.qq.com"
smtp_port = 465                                 #qq的SMTP端口465
msg = MIMEMultipart('related')                  #采用related定义内嵌资源的邮件体



cap = cv2.VideoCapture(0)
cap.set(3, 480)
cap.set(4, 320)
#比较器 xml的位置
face_cascade = cv2.CascadeClassifier( '123.xml' ) 

while True:  
    ret,frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale( gray )
    max_face = 0
    value_x = 0
    font=cv2.FONT_HERSHEY_SIMPLEX
    #记录拍摄的时间
    cv2.putText(frame,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),(20,20),font,0.8,(255,255,255),1)
    if len(faces)>0:
        print('face found!')
        currentDate=time.time()
        
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+h,y+w),(0,255,0),2)#0,255,0
            #max_face=w*h
            result = (x,y,w,h)
            x=result[0]
            y = result[1]
        
        #避免在短时间内重复拍摄，设置时间戳
        if currentDate-sendDate>600:            
            cv2.imwrite("out.png",frame)
            

            img_file = open('out.png',"rb")
            img_data = img_file.read()
            img_file.close()
            img = MIMEImage(img_data)
            img.add_header('Content-ID', '0')    #正常附件的header是不同的
            msg.attach(img)
            msg["From"] = Header("CLB", "utf-8")
            msg["To"] = Header(receiver, "utf-8")
            msg["Subject"] = Header("face detected", "utf-8")
            #-----------------将图片作为正文内容添加-------------------
            message = MIMEText("<p>careful!!!!!</p><p>human approach your device</p><img src='cid:0'/>","html","utf-8")    #plain表示纯文本
            msg.attach(message)
            contype = 'application/octet-stream'
            maintype, subtype = contype.split('/', 1)                  
            try:
                #qq必须要用.SMTP_SSL
                #其他服务器try:.SMTP
                smtpObject = smtplib.SMTP_SSL(smtp_server , smtp_port)
                smtpObject.login(sender , password)
                #message.as_string()是将MIMEText对象变成字符串
                smtpObject.sendmail(sender , [receiver] , msg.as_string())
                print ("发送成功")
            except smtplib.SMTPException :
                print ("发送失败！")
            smtpObject.quit()                
            sendDate=time.time()    
    cv2.imshow("capture", frame)
    if cv2.waitKey(1)==119:
        break
    
cap.release()
cv2.destroyAllWindows()
