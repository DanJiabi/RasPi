#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    * @par Copyright (C): 2010-2019, Hunan CLB Tech
    * @file         socket_money.py
    * @version      V1.0
    * @details
    * @par History
    @author: zhulin 
"""
from __future__ import division
import time  
import socket
from aip import AipSpeech
import pygame
address = ('192.168.100.66',7782)#本主机IP
#完成标准的socket连接，绑定，监听，以树莓派为server
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(address)
#初始化baidu speech（填入自己的信息，没有填入信息之前不能用） 
APP_ID='XXXX'
API_KEY='XXXX'
SECRET_KEY='XXXX'

aipSpeech=AipSpeech(APP_ID,API_KEY,SECRET_KEY)

while 1:
    #进入舵机后马上进行套接字“收”
    data,addr=s.recvfrom(2048)
    if not data:
        break
    #print("got data from",addr)
    #socket通信的数据需要先解码
    x=data.decode()
    print(x)
    object_H=int(x)
    if object_H>11 and object_H<25: RMB=20
    elif object_H>35 and object_H<500: RMB=1
    elif object_H>50 and object_H<80: RMB=50 
    elif object_H>100 and object_H<124: RMB=10
    elif object_H>125 and object_H<155: RMB=5
    elif object_H>156 and object_H<180: RMB=100
    else: RMB='已经找到人民币,无法识别特征值, 请调整人民币位置或改变摄像头角度'
    print('RMB',RMB,'块')
    
    
    result = aipSpeech.synthesis(text = '已经找到人民币,但是,无法识别特征值, 请调整人民币位置或改变摄像头角度,already find RNB, but, the specific value cannot be identified, please abjust the position of RMB and the camera', 
                             options={'spd':5,'vol':9,'per':1,})
#将合成的语音写如文件
if not isinstance(result,dict):
    with open('audio.mp3','wb') as f:
        f.write(result)
        
else:print(result)
#我们利用树莓派自带的pygame
pygame.mixer.init()
pygame.mixer.music.load('/home/pi/CLBDEMO/_8_speech/audio.mp3')
pygame.mixer.music.play()
        
    

    time.sleep(0.02)
s.close()