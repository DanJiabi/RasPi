#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 02:46:14 2018

@author: pi
"""

from __future__ import division
import Adafruit_PCA9685
import time  
import socket

address = ('127.0.0.1',7789)#本主机IP

#完成标准的socket连接，绑定，监听，以树莓派为server
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

s.connect(address)

#初始化舵机
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)
pwm.set_pwm(1,0,400)
pwm.set_pwm(0,0,500)
time.sleep(1)
#初始化pid参数
x=0
y=0
thisError_x=0
lastError_x=0
thisError_y=0
lastError_y=0
X_P=425
Y_P=425
flag=0
y=0

while 1:
    #进入舵机后马上进行套接字“收”
    data,addr=s.recvfrom(2048)
    if not data:
        break
    #print("got data from",addr)
    #socket通信的数据需要先解码
    x=data.decode()
    print(x)
    #发送的是x，y两个值，实际以“，”作为标志位
    strX=str(x)
    arr=strX.split(',')
    #string类型直接转成int会报错，所以先转换成float类型
    intX=int(float(arr[0]))
    intY=int(float(arr[1]))
    print('x:',intX,'y:',intY)
    
    ############
    thisError_x=intX-320
    thisError_y=intY-240
    pwm_x=thisError_x*6+1*(thisError_x-lastError_x)
    pwm_y=thisError_y*6+1*(thisError_y-lastError_y)
    
    lastError_x=thisError_x
    lastError_y=thisError_y
    XP=pwm_x/100
    YP=pwm_y/100
    X_P=X_P+int(XP)
    Y_P=Y_P+int(YP)
    if X_P>670:
        X_P=650
    if X_P<0:
        X_P=0
    if Y_P>670:
        Y_P=650
    if Y_P<50:
        Y_P=0
    ###########
    print('**',X_P,Y_P)
    pwm.set_pwm(1,0,650-X_P)
    pwm.set_pwm(2,0,800-Y_P)
    

    time.sleep(0.02)
s.close()
