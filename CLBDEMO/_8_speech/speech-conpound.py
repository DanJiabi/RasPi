#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    Created on Tue Nov  6 01:18:45 2018
    * @par Copyright (C): 2010-2019, hunan CLB Tech
    * @file        speech-conpound
    * @version      V1.0
    * @details
    * @par History
    
    @author: zhulin
"""
from aip import AipSpeech
import pygame
from time import time
import os
#请输入自己的id和密钥 （填入自己的信息，没有填入信息之前不能用） 
APP_ID='XXXX'
API_KEY='XXXX'
SECRET_KEY='XXXX'

aipSpeech=AipSpeech(APP_ID,API_KEY,SECRET_KEY)
#在可选的参数中对语速，音量，人声进行调整，个人感觉‘per’为0的女生最自然，最清晰
t=time()
result = aipSpeech.synthesis(text = '创乐博科技调用语音接口进行语音合成', 
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

t2=time()
print(t2-t)