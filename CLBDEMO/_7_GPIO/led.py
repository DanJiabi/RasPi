#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
    * @par Copyright (C): 2010-2019, hunan CLB Tech
    * @file         gpio
    * @version      V1.0
    * @details
    * @par History
    @author: zhulin
"""


import RPi.GPIO as GPIO

import time
#设置工作模式为bcm
GPIO.setmode(GPIO.BCM)
#找到将使用的引脚
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
#运行十次
for i in range(0,10):
    GPIO.output(5,True)
    time.sleep(0.5)
    GPIO.output(5,False)
    GPIO.output(6,True)
    time.sleep(0.5)
    GPIO.output(6,False)
GPIO.cleanup()

