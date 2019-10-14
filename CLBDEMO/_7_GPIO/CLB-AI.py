#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    Created on Tue Nov  6 01:18:45 2018
    * @par Copyright (C): 2010-2019, hunan CLB Tech
    * @file        CLB-AI
    * @version      V1.0
    * @details
    * @par History
    
    @author: zhulin
"""
import RPi.GPIO as GPIO
import time
#led由两个引脚控制，蜂鸣器由17引脚控制
R,G=5,6
Buzzer=17
GPIO.setmode(GPIO.BCM)

GPIO.setup(R, GPIO.OUT)
GPIO.setup(G, GPIO.OUT)
GPIO.setup(Buzzer, GPIO.OUT)
global Buzz						# Assign a global variable to replace GPIO.PWM
Buzz = GPIO.PWM(Buzzer, 440)	# 440 is initial frequency.
Buzz.start(50)	
#先让蜂鸣器停下来

#设置pwm的工作模式为pwm
pwmR = GPIO.PWM(R, 70)
pwmG = GPIO.PWM(G, 70)

pwmR.start(0)
pwmG.start(0)  
#写四种模式，实际可以由更多变化方式
try:
	t = 0.01
	while True:
            for i in range(0,71):
                pwmG.ChangeDutyCycle(70)
                Buzz.ChangeFrequency(500-i)
                pwmR.ChangeDutyCycle(70-i)
                print(i)
                time.sleep(t)
            for i in range(70,-1,-1):
                pwmG.ChangeDutyCycle(0)
                Buzz.ChangeFrequency(500+i)
                pwmR.ChangeDutyCycle(70-i)
                print(i-1000)
                time.sleep(t)

        
except KeyboardInterrupt:
	Buzz.ChangeFrequency(0)
pwmR.stop()
pwmG.stop()
GPIO.cleanup()
		