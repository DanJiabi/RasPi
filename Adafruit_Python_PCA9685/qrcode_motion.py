#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""

    * @par Copyright (C): 2010-2019, Hunan CLB Tech
    * @file       qrcode—motion
    * @version      V1.0
    * @details
    * @par History
    
    @author: zhulin
"""
from __future__ import division
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
import RPi.GPIO as GPIO
import Adafruit_PCA9685

#初始化gpio
GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
#初始化舵机
servo_updown=390
servo_rightleft=390
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)
pwm.set_pwm(0, 0, servo_rightleft)
pwm.set_pwm(1, 0, servo_updown)
#当舵机超过允许角度前进行报警，蜂鸣器
def warning():
    GPIO.setup(17,GPIO.OUT)
    GPIO.output(17,True)
    time.sleep(1)
    GPIO.output(17,False)
#流水灯    
def red_yellow_blue():
    for i in range(0,2):
        GPIO.output(5,True)
        time.sleep(0.1)
        GPIO.output(6,True)
        time.sleep(0.1)
        GPIO.output(11,True)
        time.sleep(0.1)
        GPIO.output(6,False)
        time.sleep(0.1)
        GPIO.output(5,False)
        time.sleep(0.1)
        GPIO.output(11,False)
#舵机两个自由度的转向
#这里我们用global控制舵机角度
def right():
    global servo_rightleft
    servo_rightleft-=50
    if servo_rightleft<=170 or servo_rightleft>=570:
        warning()
    else : 
        pwm.set_pwm(1, 0, servo_rightleft)        
def left():
    global servo_rightleft
    servo_rightleft+=50
    if servo_rightleft<=170 or servo_rightleft>=570:
        warning()
    else : 
        pwm.set_pwm(1, 0, servo_rightleft)   
def turn_down():
    global servo_updown
    servo_updown-=50
    if servo_updown<=170 or servo_updown>=570:
        warning()
    else:
        pwm.set_pwm(2,0,servo_updown)
def turn_up():
    global servo_updown
    servo_updown+=50
    if servo_updown<=70 or servo_updown>=570:
        warning()
    else:
        pwm.set_pwm(2,0,servo_updown)

ap=argparse.ArgumentParser()
#提供一个csv文件，这样，在最后不仅可以将二维码内容显示在屏幕上，还有专门的文件进行保存
ap.add_argument("-o","--output",type=str,default="content.csv",
                help="path to output csv file containing barcode")
args=vars(ap.parse_args())

print('starting video stream....')
#这是使用web摄像头的写法
vs=VideoStream(src=0).start()
#使用树莓派自带摄像头的写法是：
#vs=VideoStream(usePiCamera=True).start()
time.sleep(2.0)

#把内容写入csv
csv=open(args["output"],"w")
found=set()
#避免拥塞，多次处理
lastData=''
sendDate=0
while True:
    frame=vs.read()
    frame=imutils.resize(frame,width=400)
    barcodes=pyzbar.decode(frame)
    for barcode in barcodes:
        (x,y,w,h)=barcode.rect
        
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
        #对二维码内呢绒进行解码，输入时间，内容和类型
        barcodeData=barcode.data.decode("utf-8")
        barcodeType=barcode.type
        
        text="{}({})".format(barcodeData,barcodeType)
        
        cv2.putText(frame,text,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,
                    (0,0,255),2)
        
        newData=barcodeData
        currentDate=time.time()
        #识别，每三秒识别一次，将不正确的信息打印出来，
        #如果希望添加新的二维码，添加判断就可以了
        if (currentDate-sendDate>3):
            print('1')
            if newData=='red_yello_blue light up':
                red_yellow_blue()
                sendDate=time.time()
            elif newData=='right_left servo turn 0':
                left()          #less than 500
            elif newData=='right_left servo turn 180':
                right()
            elif newData=='turn down':
                turn_down()
            elif newData=='turn up':
                turn_up()
            else : print('incorrect data:',newData)
        else:
            continue
 
        if barcodeData not in found:
            csv.write("{},{}\n".format(datetime.datetime.now(),barcodeData))
            csv.flush()
            found.add(barcodeData)
    cv2.imshow("found_code",frame)
    key=cv2.waitKey(1)&0xFF
    if key==ord("q"):
        break


csv.close()
cv2.destroyAllWindows()
vs.stop()
        